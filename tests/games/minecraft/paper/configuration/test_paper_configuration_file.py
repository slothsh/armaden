from __future__ import annotations

from pathlib import Path

from typing import cast

from returns.pipeline import is_successful
from armaden.framework.api.error import Error

from armaden.games.minecraft.paper.configuration.bukkit_configuration import (
    BukkitConfiguration,
)
from armaden.games.minecraft.paper.configuration.paper_configuration_file import (
    PaperConfigurationFileError,
)
from tests.games.minecraft.paper.configuration.config_support import at
from tests.games.minecraft.paper.paper_reference import BUKKIT_CONFIGURATION_URL

USER_FILE = '''\
# user-managed comment
settings:
  allow-end: true
  connection-throttle: 1234  # tuned
  unknown-future-key: kept
spawn-limits:
  monsters: 70
'''


def test_reference_url_is_recorded() -> None:
    assert BUKKIT_CONFIGURATION_URL == 'https://docs.papermc.io/paper/reference/bukkit-configuration/'


def test_file_name_matches_the_reference() -> None:
    assert BukkitConfiguration.FILE_NAME == 'bukkit.yml'


def test_defaults_match_the_reference_inventory() -> None:
    defaults = BukkitConfiguration.defaults()

    assert at(defaults, ('settings', 'allow-end')) is True
    assert at(defaults, ('settings', 'permissions-file')) == 'permissions.yml'
    assert at(defaults, ('settings', 'deprecated-verbose')) == 'default'
    assert at(defaults, ('settings', 'minimum-api')) == 'none'
    assert at(defaults, ('spawn-limits', 'monsters')) == 70
    assert at(defaults, ('spawn-limits', 'axolotls')) == 5
    assert at(defaults, ('chunk-gc', 'period-in-ticks')) == 600
    assert at(defaults, ('ticks-per', 'autosave')) == 6000
    assert at(defaults, ('aliases',)) == 'now-in-commands.yml'
    assert at(defaults, ('worlds',)) == {}


def test_read_returns_none_for_a_missing_file(tmp_path: Path) -> None:
    configuration = BukkitConfiguration(tmp_path / 'bukkit.yml')

    result = configuration.read()

    assert is_successful(result)
    assert result.unwrap() is None


def test_ensure_generates_defaults_when_the_file_is_missing(tmp_path: Path) -> None:
    path = tmp_path / 'bukkit.yml'
    configuration = BukkitConfiguration(path)

    result = configuration.ensure()

    assert is_successful(result)
    text = path.read_text(encoding='utf-8')
    assert 'allow-end: true' in text
    assert 'period-in-ticks: 600' in text
    tree = configuration.read()
    assert is_successful(tree)
    assert tree.unwrap() == BukkitConfiguration.defaults()


def test_ensure_generation_is_idempotent(tmp_path: Path) -> None:
    path = tmp_path / 'bukkit.yml'
    configuration = BukkitConfiguration(path)

    assert is_successful(configuration.ensure())
    first = path.read_text(encoding='utf-8')
    assert is_successful(configuration.ensure())
    second = path.read_text(encoding='utf-8')

    assert first == second


def test_ensure_merges_overrides_into_defaults_for_a_missing_file(tmp_path: Path) -> None:
    path = tmp_path / 'bukkit.yml'
    configuration = BukkitConfiguration(path)

    result = configuration.ensure({'spawn-limits': {'monsters': 5}})

    assert is_successful(result)
    tree = configuration.read()
    assert is_successful(tree)
    assert tree.unwrap() is not None
    assert at(tree.unwrap(), ('spawn-limits',)) == {
        'monsters': 5,
        'animals': 10,
        'water-animals': 5,
        'water-ambient': 20,
        'water-underground-creature': 5,
        'axolotls': 5,
        'ambient': 15,
    }


def test_ensure_patches_only_overrides_into_an_existing_user_file(tmp_path: Path) -> None:
    path = tmp_path / 'bukkit.yml'
    _ = path.write_text(USER_FILE, encoding='utf-8')
    configuration = BukkitConfiguration(path)

    result = configuration.ensure({'spawn-limits': {'monsters': 5}, 'settings': {'connection-throttle': 4000}})

    assert is_successful(result)
    text = path.read_text(encoding='utf-8')
    assert '# user-managed comment' in text
    assert 'connection-throttle: 4000' in text and '# tuned' in text
    assert 'unknown-future-key: kept' in text
    tree = configuration.read()
    assert is_successful(tree)
    assert tree.unwrap() is not None
    assert at(tree.unwrap(), ('settings', 'allow-end')) is True

    spawn_limits = configuration.mapping_value(('spawn-limits',)).unwrap()
    assert spawn_limits is not None
    assert spawn_limits.get('animals') is None


def test_apply_only_touches_requested_paths(tmp_path: Path) -> None:
    path = tmp_path / 'bukkit.yml'
    _ = path.write_text(USER_FILE, encoding='utf-8')
    configuration = BukkitConfiguration(path)

    result = configuration.apply({'spawn-limits': {'monsters': 99}})

    assert is_successful(result)
    tree = configuration.read()
    assert is_successful(tree)
    assert tree.unwrap() is not None
    assert at(tree.unwrap(), ('spawn-limits', 'monsters')) == 99
    assert at(tree.unwrap(), ('settings', 'connection-throttle')) == 1234
    assert at(tree.unwrap(), ('settings', 'unknown-future-key')) == 'kept'


def test_effective_falls_back_to_documented_defaults(tmp_path: Path) -> None:
    path = tmp_path / 'bukkit.yml'
    _ = path.write_text(USER_FILE, encoding='utf-8')
    configuration = BukkitConfiguration(path)

    from_file = configuration.effective(('settings', 'connection-throttle'))
    defaulted = configuration.effective(('spawn-limits', 'animals'))
    missing = configuration.effective(('not', 'documented'))

    assert is_successful(from_file) and from_file.unwrap() == 1234
    assert is_successful(defaulted) and defaulted.unwrap() == 10
    assert is_successful(missing) and missing.unwrap() is None


def test_typed_value_accessors_validate_types(tmp_path: Path) -> None:
    configuration = BukkitConfiguration(tmp_path / 'bukkit.yml')

    assert configuration.bool_value(('settings', 'allow-end')).unwrap() is True
    assert configuration.int_value(('chunk-gc', 'period-in-ticks')).unwrap() == 600
    assert configuration.float_value(('settings', 'connection-throttle')).unwrap() == 4000.0
    assert configuration.str_value(('settings', 'update-folder')).unwrap() == 'update'
    assert configuration.mapping_value(('spawn-limits',)).unwrap() == BukkitConfiguration.defaults()['spawn-limits']
    assert configuration.list_value(('not', 'present')).unwrap() is None

    wrong_type = configuration.bool_value(('chunk-gc', 'period-in-ticks'))

    assert not is_successful(wrong_type)
    assert cast(Error, wrong_type.failure()).context == PaperConfigurationFileError.INVALID_VALUE.value


def test_missing_values_stay_unset_and_never_overwrite(tmp_path: Path) -> None:
    path = tmp_path / 'bukkit.yml'
    _ = path.write_text(USER_FILE, encoding='utf-8')
    configuration = BukkitConfiguration(path)

    result = configuration.ensure()

    assert is_successful(result)
    tree = configuration.read()
    assert is_successful(tree)
    assert tree.unwrap() is not None
    assert at(tree.unwrap(), ('settings', 'connection-throttle')) == 1234
    settings = configuration.mapping_value(('settings',)).unwrap()
    assert settings is not None
    assert settings.get('allow-end') is True
    assert settings.get('minimum-api') is None
