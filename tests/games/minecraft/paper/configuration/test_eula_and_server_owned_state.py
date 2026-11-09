from __future__ import annotations

from pathlib import Path

from returns.pipeline import is_successful

from armaden.games.minecraft.paper.configuration.eula import EulaFile
from armaden.games.minecraft.paper.configuration.server_owned_state import (
    PaperServerOwnedFile,
    PaperServerOwnedState,
)


def test_write_accepts_the_eula(tmp_path: Path) -> None:
    path = tmp_path / 'eula.txt'
    store = EulaFile(path)

    result = store.write(True)

    assert is_successful(result)
    assert path.read_text(encoding='utf-8') == 'eula=true\n'
    assert store.read().unwrap() is True


def test_write_can_withhold_the_eula(tmp_path: Path) -> None:
    path = tmp_path / 'eula.txt'
    store = EulaFile(path)

    assert is_successful(store.write(False))

    assert path.read_text(encoding='utf-8') == 'eula=false\n'
    assert store.read().unwrap() is False


def test_write_preserves_user_comments_and_is_idempotent(tmp_path: Path) -> None:
    path = tmp_path / 'eula.txt'
    _ = path.write_text('#By changing the setting below to TRUE you indicate your agreement to our EULA.\neula=false\n', encoding='utf-8')
    store = EulaFile(path)

    assert is_successful(store.write(True))

    text = path.read_text(encoding='utf-8')
    assert '#By changing the setting below to TRUE you indicate your agreement to our EULA.' in text
    assert 'eula=true' in text

    assert is_successful(store.write(True))
    assert path.read_text(encoding='utf-8') == text


def test_read_returns_none_when_file_is_missing(tmp_path: Path) -> None:
    store = EulaFile(tmp_path / 'eula.txt')

    result = store.read()

    assert is_successful(result)
    assert result.unwrap() is None


def test_read_returns_none_without_an_eula_entry(tmp_path: Path) -> None:
    path = tmp_path / 'eula.txt'
    _ = path.write_text('# a file without consent state\n', encoding='utf-8')
    store = EulaFile(path)

    result = store.read()

    assert is_successful(result)
    assert result.unwrap() is None


def test_server_owned_files_are_classified_as_state_not_configuration() -> None:
    assert {member.value for member in PaperServerOwnedFile} == {
        'banned-ips.json',
        'banned-players.json',
        'ops.json',
        'usercache.json',
        'whitelist.json',
    }


def test_server_owned_files_are_detected_by_name() -> None:
    for name in ('banned-ips.json', 'banned-players.json', 'ops.json', 'usercache.json', 'whitelist.json'):
        assert PaperServerOwnedState.is_owned_file(Path('/srv/paper') / name) is True

    for name in ('server.properties', 'bukkit.yml', 'eula.txt', 'spigot.yml'):
        assert PaperServerOwnedState.is_owned_file(Path('/srv/paper') / name) is False


def test_managed_locations_are_never_treated_as_configuration() -> None:
    for name in ('logs', 'plugins', '.paper-remapped', 'bStats', 'spark', 'world', 'world_nether', 'world_the_end'):
        assert PaperServerOwnedState.is_managed_location(name) is True

    for name in ('config', 'libraries', 'downloads'):
        assert PaperServerOwnedState.is_managed_location(name) is False
