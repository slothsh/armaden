from __future__ import annotations

from pathlib import Path

from typing import cast

from returns.pipeline import is_successful

from armaden.framework.api.error import Error
from armaden.games.minecraft.paper.dto import PaperCliArgumentsData, PaperCliArgumentsError
from armaden.games.minecraft.paper.enums import PaperCliFlagError


def test_default_arguments_emit_no_tokens() -> None:
    result = PaperCliArgumentsData().to_tokens()

    assert is_successful(result)
    assert result.unwrap() == []


def test_boolean_flags_emit_one_token_only_when_enabled() -> None:
    arguments = PaperCliArgumentsData(demo=True, nogui=True, safe_mode=False)

    result = arguments.to_tokens()

    assert is_successful(result)
    assert result.unwrap() == ['--demo', '--nogui']


def test_value_flags_emit_flag_and_value_tokens() -> None:
    arguments = PaperCliArgumentsData(port=25565, online_mode=False, level_name='my world')

    result = arguments.to_tokens()

    assert is_successful(result)
    assert result.unwrap() == ['--level-name', 'my world', '--online-mode', 'false', '--port', '25565']


def test_repeatable_options_preserve_exact_ordering() -> None:
    arguments = PaperCliArgumentsData(
        add_plugin_dirs=['first-plugins', 'second-plugins'],
        add_plugin_jars=['a.jar', 'b.jar', 'c.jar'],
    )

    result = arguments.to_tokens()

    assert is_successful(result)
    assert result.unwrap() == [
        '--add-plugin-dir', 'first-plugins',
        '--add-plugin-dir', 'second-plugins',
        '--add-plugin', 'a.jar',
        '--add-plugin', 'b.jar',
        '--add-plugin', 'c.jar',
    ]


def test_repeatable_options_accept_multiple_occurrences_when_parsing() -> None:
    result = PaperCliArgumentsData.from_tokens([
        '--add-plugin-dir', 'one',
        '--add-extra-plugin-dir', 'two',
        '--add-plugin', 'a.jar',
        '--add-extra-plugin-jar', 'b.jar',
    ])

    assert is_successful(result)
    arguments = result.unwrap()
    assert arguments.add_plugin_dirs == ['one', 'two']
    assert arguments.add_plugin_jars == ['a.jar', 'b.jar']


def test_aliases_parse_into_one_canonical_setting() -> None:
    result = PaperCliArgumentsData.from_tokens([
        '-P', 'plug ins',
        '-W', 'worlds',
        '-o', 'true',
        '-p', '25599',
        '-s', '40',
        '-w', 'survival land',
        '-h', '10.0.0.1',
        '--paper', 'legacy.yml',
        '-C', 'my commands.yml',
        '--pidFile', 'server.pid',
    ])

    assert is_successful(result)
    arguments = result.unwrap()
    assert arguments.plugins == 'plug ins'
    assert arguments.universe == 'worlds'
    assert arguments.online_mode is True
    assert arguments.port == 25599
    assert arguments.max_players == 40
    assert arguments.level_name == 'survival land'
    assert arguments.host == '10.0.0.1'
    assert arguments.paper_settings == 'legacy.yml'
    assert arguments.commands_settings == 'my commands.yml'
    assert arguments.pid_file == 'server.pid'


def test_unknown_flag_is_rejected_when_parsing() -> None:
    result = PaperCliArgumentsData.from_tokens(['--made-up-flag', 'value'])

    assert not is_successful(result)
    error = cast(Error, result.failure())
    assert error.kind is PaperCliFlagError.UNKNOWN_FLAG
    assert error.details == {'token': '--made-up-flag'}


def test_missing_value_is_rejected_when_parsing() -> None:
    for tokens in (['-p'], ['--add-plugin-dir'], ['--nogui', '--port']):
        result = PaperCliArgumentsData.from_tokens(tokens)

        assert not is_successful(result)
        error = cast(Error, result.failure())
        assert error.kind is PaperCliArgumentsError.MISSING_VALUE


def test_duplicate_value_option_is_rejected_when_parsing() -> None:
    result = PaperCliArgumentsData.from_tokens(['-p', '25565', '--server-port', '25566'])

    assert not is_successful(result)
    error = cast(Error, result.failure())
    assert error.kind is PaperCliArgumentsError.DUPLICATE_OPTION
    assert error.details['flag'] == '--port'


def test_invalid_values_are_rejected_when_parsing() -> None:
    for tokens, field in (
        (['-p', 'not-a-port'], 'port'),
        (['-s', 'twelve'], 'max_players'),
        (['-o', 'yes'], 'online_mode'),
        (['--server-name', ''], 'server_name'),
    ):
        result = PaperCliArgumentsData.from_tokens(tokens)

        assert not is_successful(result)
        error = cast(Error, result.failure())
        assert error.kind is PaperCliArgumentsError.INVALID_VALUE
        assert error.details['field'] == field


def test_invalid_values_are_rejected_when_serializing() -> None:
    for arguments in (
        PaperCliArgumentsData(port=0),
        PaperCliArgumentsData(port=70000),
        PaperCliArgumentsData(port=-1),
        PaperCliArgumentsData(max_players=-3),
        PaperCliArgumentsData(server_name=''),
        PaperCliArgumentsData(universe=''),
    ):
        assert not is_successful(arguments.to_tokens())


def test_paths_with_spaces_and_punctuation_survive_serialization() -> None:
    arguments = PaperCliArgumentsData(
        plugins='plugin folder (2026)',
        pid_file='pid file: #1.pid',
        universe='worlds & more',
        server_id='id-with.dots:42',
    )

    result = arguments.to_tokens()

    assert is_successful(result)
    assert result.unwrap() == [
        '--pidFile', 'pid file: #1.pid',
        '--plugins', 'plugin folder (2026)',
        '--serverId', 'id-with.dots:42',
        '--universe', 'worlds & more',
    ]


def test_relative_paths_resolve_against_the_working_directory() -> None:
    arguments = PaperCliArgumentsData(
        plugins='extra plugins',
        config='properties/server.properties',
        universe='worlds',
        host='localhost',
    )

    result = arguments.to_tokens(Path('/srv/paper'))

    assert is_successful(result)
    assert result.unwrap() == [
        '--config', '/srv/paper/properties/server.properties',
        '--host', 'localhost',
        '--plugins', '/srv/paper/extra plugins',
        '--universe', '/srv/paper/worlds',
    ]


def test_absolute_paths_are_left_untouched() -> None:
    arguments = PaperCliArgumentsData(plugins='/opt/plugins', config='/etc/paper/server.properties')

    result = arguments.to_tokens(Path('/srv/paper'))

    assert is_successful(result)
    assert result.unwrap() == [
        '--config', '/etc/paper/server.properties',
        '--plugins', '/opt/plugins',
    ]


def test_relative_paths_stay_relative_without_a_working_directory() -> None:
    arguments = PaperCliArgumentsData(plugins='plugins', config='server.properties')

    result = arguments.to_tokens()

    assert is_successful(result)
    assert result.unwrap() == ['--config', 'server.properties', '--plugins', 'plugins']


def test_parse_and_serialize_round_trip() -> None:
    original = PaperCliArgumentsData(
        add_plugin_dirs=['one', 'two'],
        add_plugin_jars=['a.jar'],
        demo=True,
        bonus_chest=True,
        erase_cache=True,
        force_upgrade=True,
        help=False,
        host='10.0.0.5',
        init_settings=True,
        jfr_profile=True,
        level_name='round trip',
        max_players=12,
        noconsole=True,
        nogui=True,
        nojline=True,
        online_mode=False,
        paper_dir='config',
        paper_settings='legacy.yml',
        pid_file='run/server.pid',
        plugins='plug ins',
        port=25599,
        recreate_region_files=True,
        safe_mode=True,
        server_id='server-id',
        server_name='A & B: test',
        spigot_settings='spigot settings.yml',
        universe='worlds',
        version=False,
    )

    serialized = original.to_tokens()
    assert is_successful(serialized)

    parsed = PaperCliArgumentsData.from_tokens(serialized.unwrap())
    assert is_successful(parsed)
    assert parsed.unwrap() == original


def test_help_and_version_prevent_server_start() -> None:
    assert PaperCliArgumentsData(help=True).prevents_server_start() is True
    assert PaperCliArgumentsData(version=True).prevents_server_start() is True
    assert PaperCliArgumentsData(nogui=True).prevents_server_start() is False


def test_legacy_paper_settings_is_migration_only() -> None:
    assert PaperCliArgumentsData(paper_settings='legacy.yml').is_migration_only() is True
    assert PaperCliArgumentsData(paper_dir='config').is_migration_only() is False
