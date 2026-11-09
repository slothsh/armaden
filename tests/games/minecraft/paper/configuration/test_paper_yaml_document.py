from __future__ import annotations

from pathlib import Path

from typing import cast

from returns.pipeline import is_successful
from armaden.framework.api.error import Error

from armaden.games.minecraft.paper.configuration.paper_yaml_document import (
    PaperYamlDocument,
    PaperYamlDocumentError,
    YamlMapping,
)
from tests.games.minecraft.paper.configuration.config_support import at
from tests.games.minecraft.paper.paper_reference import CONFIGURATION_URL

EXISTING_DOCUMENT = '''\
# top-level comment
settings:
  sample-count: 12  # inline comment
  restart-on-crash: true
  bungeecord: false
advancements:
  disable-saving: false
  disabled:
  - minecraft:story/disabled
  unknown-future-key: 'kept as-is'
messages:
  whitelist: You are not whitelisted on this server!
'''


def make_document(tmp_path: Path, name: str = 'config.yml', content: str | None = None) -> PaperYamlDocument:
    path = tmp_path / name

    if content is not None:
        _ = path.write_text(content, encoding='utf-8')

    return PaperYamlDocument(path)


def test_reference_url_is_recorded() -> None:
    assert CONFIGURATION_URL == 'https://docs.papermc.io/paper/reference/configuration/'


def test_read_returns_none_when_file_is_missing(tmp_path: Path) -> None:
    document = make_document(tmp_path)

    result = document.read()

    assert is_successful(result)
    assert result.unwrap() is None


def test_read_parses_nested_structure_and_scalars(tmp_path: Path) -> None:
    document = make_document(tmp_path, content=EXISTING_DOCUMENT)

    result = document.read()

    assert is_successful(result)
    tree = result.unwrap()
    assert tree is not None
    assert at(tree, ('settings', 'sample-count')) == 12
    assert at(tree, ('advancements', 'disabled')) == ['minecraft:story/disabled']
    assert at(tree, ('messages', 'whitelist')) == 'You are not whitelisted on this server!'


def test_read_rejects_invalid_yaml(tmp_path: Path) -> None:
    document = make_document(tmp_path, content=': : : not yaml [truthy')

    result = document.read()

    assert not is_successful(result)
    error = result.failure()
    assert cast(Error, error).context == PaperYamlDocumentError.INVALID_DOCUMENT.value


def test_read_rejects_non_mapping_roots(tmp_path: Path) -> None:
    document = make_document(tmp_path, content='- a\n- b\n')

    result = document.read()

    assert not is_successful(result)
    assert cast(Error, result.failure()).context == PaperYamlDocumentError.INVALID_DOCUMENT.value


def test_write_generates_a_new_file_with_nested_structure(tmp_path: Path) -> None:
    document = make_document(tmp_path)

    result = document.write({'world-settings': {'default': {'view-distance': 'default', 'growth': {'cactus-modifier': 100}}}})

    assert is_successful(result)
    text = (tmp_path / 'config.yml').read_text(encoding='utf-8')
    assert 'world-settings:' in text
    assert 'view-distance: default' in text
    assert 'cactus-modifier: 100' in text

    read_back = document.read()
    assert is_successful(read_back)
    assert read_back.unwrap() == {
        'world-settings': {'default': {'view-distance': 'default', 'growth': {'cactus-modifier': 100}}}
    }


def test_apply_updates_scalars_and_preserves_comments_and_unknown_keys(tmp_path: Path) -> None:
    document = make_document(tmp_path, content=EXISTING_DOCUMENT)

    result = document.apply({'settings': {'sample-count': 20}, 'messages': {'unknown-command': 'Nope!'}})

    assert is_successful(result)
    text = (tmp_path / 'config.yml').read_text(encoding='utf-8')
    assert '# top-level comment' in text
    assert 'sample-count: 20' in text and '# inline comment' in text
    assert 'sample-count: 12' not in text
    assert "unknown-future-key: 'kept as-is'" in text
    assert 'minecraft:story/disabled' in text
    assert 'unknown-command: Nope!' in text
    assert 'whitelist: You are not whitelisted on this server!' in text


def test_apply_replaces_lists_in_place(tmp_path: Path) -> None:
    document = make_document(tmp_path, content=EXISTING_DOCUMENT)

    result = document.apply({'advancements': {'disabled': ['minecraft:story/root', 'minecraft:husbandry/root']}})

    assert is_successful(result)
    tree = document.read()
    assert is_successful(tree)
    assert tree.unwrap() is not None
    assert at(tree.unwrap(), ('advancements', 'disabled')) == ['minecraft:story/root', 'minecraft:husbandry/root']
    text = (tmp_path / 'config.yml').read_text(encoding='utf-8')
    assert 'minecraft:story/disabled' not in text


def test_apply_adds_new_nested_sections_without_touching_the_rest(tmp_path: Path) -> None:
    document = make_document(tmp_path, content=EXISTING_DOCUMENT)

    result = document.apply({'world-settings': {'default': {'growth': {'cactus-modifier': 150}}}})

    assert is_successful(result)
    tree = document.read()
    assert is_successful(tree)
    assert tree.unwrap() is not None
    assert at(tree.unwrap(), ('world-settings',)) == {'default': {'growth': {'cactus-modifier': 150}}}
    assert at(tree.unwrap(), ('settings', 'sample-count')) == 12


def test_apply_creates_a_sparse_file_when_missing(tmp_path: Path) -> None:
    document = make_document(tmp_path)

    result = document.apply({'messages': {'restart': 'Back soon!'}})

    assert is_successful(result)
    tree = document.read()
    assert is_successful(tree)
    assert tree.unwrap() == {'messages': {'restart': 'Back soon!'}}


def test_apply_is_idempotent(tmp_path: Path) -> None:
    document = make_document(tmp_path, content=EXISTING_DOCUMENT)

    assert is_successful(document.apply({'settings': {'sample-count': 20}}))
    first = (tmp_path / 'config.yml').read_text(encoding='utf-8')

    assert is_successful(document.apply({'settings': {'sample-count': 20}}))
    second = (tmp_path / 'config.yml').read_text(encoding='utf-8')

    assert first == second


def test_apply_values_with_special_characters_round_trip(tmp_path: Path) -> None:
    document = make_document(tmp_path, content=EXISTING_DOCUMENT)

    result = document.apply({
        'messages': {
            'whitelist': 'You are &cnot&r whitelisted: see #rules!',
            'punctuation': 'A & B: test (2026) - really',
        }
    })

    assert is_successful(result)
    tree = document.read()
    assert is_successful(tree)
    assert tree.unwrap() is not None
    assert at(tree.unwrap(), ('messages', 'whitelist')) == 'You are &cnot&r whitelisted: see #rules!'
    assert at(tree.unwrap(), ('messages', 'punctuation')) == 'A & B: test (2026) - really'


def test_apply_with_an_empty_mapping_is_a_no_op(tmp_path: Path) -> None:
    document = make_document(tmp_path, content=EXISTING_DOCUMENT)
    before = (tmp_path / 'config.yml').read_text(encoding='utf-8')

    result = document.apply({})

    assert is_successful(result)
    assert (tmp_path / 'config.yml').read_text(encoding='utf-8') == before


def test_write_and_read_round_trip_through_minmessage_and_lang_values(tmp_path: Path) -> None:
    document = make_document(tmp_path)

    tree: YamlMapping = {
        'messages': {
            'kick': {
                'flying-player': '<lang:multiplayer.disconnect.flying>',
                'no-permission': "<red>I'm sorry, but you do not have permission to perform this command.",
            }
        }
    }

    assert is_successful(document.write(tree))

    read_back = document.read()
    assert is_successful(read_back)
    assert read_back.unwrap() == tree
