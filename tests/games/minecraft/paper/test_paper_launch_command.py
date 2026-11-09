from __future__ import annotations

from typing import cast

from returns.pipeline import is_successful

from armaden.framework.api.error import Error
from armaden.games.minecraft import MinecraftServer, MinecraftServerConfig
from armaden.games.minecraft.paper.dto import (
    PaperCliArgumentsData,
    PaperJvmLaunchData,
    PaperLaunchConfigData,
)
from armaden.games.minecraft.paper.enums import PaperEnvironmentVariable, PaperSystemProperty
from armaden.games.minecraft.paper.paper_launch_command import (
    PaperLaunchCommand,
    PaperLaunchCommandError,
    resolve_cli_precedence,
)


def build_command(
    cli: PaperCliArgumentsData | None = None,
    jvm: PaperJvmLaunchData | None = None,
    environment: dict[PaperEnvironmentVariable, str] | None = None,
) -> PaperLaunchCommand:
    config = PaperLaunchConfigData(
        cli_arguments=cli or PaperCliArgumentsData(),
        environment=environment or {},
        jvm=jvm or PaperJvmLaunchData(),
    )

    return PaperLaunchCommand(
        config,
        java_executable='/usr/lib/jvm/java/bin/java',
        paper_jar='/srv/paper/paper.jar',
        working_directory='/srv/paper',
    )


def test_argv_places_jvm_tokens_before_the_jar_and_paper_tokens_after_it() -> None:
    command = build_command(
        cli=PaperCliArgumentsData(nogui=True, port=25599),
        jvm=PaperJvmLaunchData(
            initial_memory_mb=512,
            maximum_memory_mb=2048,
            options=['-XX:+UseG1GC', '-XX:MaxGCPauseMillis=200'],
            system_properties={PaperSystemProperty.MAX_SIGN_LENGTH: '100'},
        ),
    )

    result = command.argv()

    assert is_successful(result)
    assert result.unwrap() == [
        '/usr/lib/jvm/java/bin/java',
        '-Xms512M',
        '-Xmx2048M',
        '-XX:+UseG1GC',
        '-XX:MaxGCPauseMillis=200',
        '-DPaper.maxSignLength=100',
        '-jar',
        '/srv/paper/paper.jar',
        '--nogui',
        '--port',
        '25599',
    ]


def test_argv_omits_unset_defaults() -> None:
    command = build_command()

    result = command.argv()

    assert is_successful(result)
    assert result.unwrap() == [
        '/usr/lib/jvm/java/bin/java',
        '-jar',
        '/srv/paper/paper.jar',
    ]


def test_invalid_jvm_memory_fails_the_whole_command() -> None:
    command = build_command(jvm=PaperJvmLaunchData(maximum_memory_mb=0))

    assert not is_successful(command.argv())


def test_invalid_cli_value_fails_the_whole_command() -> None:
    command = build_command(cli=PaperCliArgumentsData(port=99999))

    assert not is_successful(command.argv())


def test_environment_variables_are_passed_as_environment_not_argv() -> None:
    command = build_command(
        environment={
            PaperEnvironmentVariable.VELOCITY_SECRET: 'shared-secret',
            PaperEnvironmentVariable.DEFAULT_CENTRAL_REPOSITORY: 'https://mirror.example.com/maven2',
        },
    )

    argv = command.argv()

    assert is_successful(argv)
    assert 'PAPER_VELOCITY_SECRET' not in argv.unwrap()
    assert command.environment() == {
        'PAPER_VELOCITY_SECRET': 'shared-secret',
        'PAPER_DEFAULT_CENTRAL_REPOSITORY': 'https://mirror.example.com/maven2',
    }


def test_from_server_config_uses_the_default_nogui_argument() -> None:
    config = MinecraftServer().config

    result = PaperLaunchCommand.from_server_config(
        config,
        paper_jar='paper.jar',
        java_executable='java',
    )

    assert is_successful(result)
    argv = result.unwrap().argv()
    assert is_successful(argv)
    assert argv.unwrap() == ['java', '-jar', 'paper.jar', '--nogui']


def test_from_server_config_maps_jvm_memory_and_options() -> None:
    config = MinecraftServer(config={'jvm': {
        'initialMemoryMb': 1024,
        'maximumMemoryMb': 4096,
        'options': ['-XX:+UseG1GC'],
    }}).config

    result = PaperLaunchCommand.from_server_config(
        config,
        paper_jar='paper.jar',
        java_executable='/opt/java/bin/java',
    )

    assert is_successful(result)
    argv = result.unwrap().argv()
    assert is_successful(argv)
    assert argv.unwrap() == [
        '/opt/java/bin/java',
        '-Xms1024M',
        '-Xmx4096M',
        '-XX:+UseG1GC',
        '-jar',
        'paper.jar',
        '--nogui',
    ]


def test_from_server_config_parses_extra_arguments_into_typed_flags() -> None:
    config: MinecraftServerConfig = {
        'arguments': {'nogui': True, 'extra': ['--server-port', '25599', '--safeMode', '--add-plugin', 'extra.jar']},
    }

    result = PaperLaunchCommand.from_server_config(
        config,
        paper_jar='paper.jar',
        java_executable='java',
    )

    assert is_successful(result)
    argv = result.unwrap().argv()
    assert is_successful(argv)
    assert argv.unwrap() == [
        'java',
        '-jar',
        'paper.jar',
        '--add-plugin',
        'extra.jar',
        '--nogui',
        '--safeMode',
        '--port',
        '25599',
    ]


def test_from_server_config_rejects_unknown_extra_arguments() -> None:
    config: MinecraftServerConfig = {
        'arguments': {'nogui': True, 'extra': ['--definitely-not-paper']},
    }

    result = PaperLaunchCommand.from_server_config(
        config,
        paper_jar='paper.jar',
        java_executable='java',
    )

    assert not is_successful(result)


def test_from_server_config_uses_the_configured_java_executable() -> None:
    config: MinecraftServerConfig = {'java': {'executable': '/configured/java', 'version': 25}}

    result = PaperLaunchCommand.from_server_config(config, paper_jar='paper.jar')

    assert is_successful(result)
    argv = result.unwrap().argv()
    assert is_successful(argv)
    assert argv.unwrap()[0] == '/configured/java'


def test_from_server_config_requires_a_java_executable() -> None:
    config: MinecraftServerConfig = {}

    result = PaperLaunchCommand.from_server_config(config, paper_jar='paper.jar')

    assert not is_successful(result)
    error = cast(Error, result.failure())
    assert error.kind is PaperLaunchCommandError.MISSING_JAVA_EXECUTABLE


def test_from_server_config_keeps_server_properties_out_of_the_cli_arguments() -> None:
    config: MinecraftServerConfig = {
        'server': {'onlineMode': False, 'serverPort': 25565, 'maxPlayers': 10, 'levelName': 'world'},
    }

    result = PaperLaunchCommand.from_server_config(
        config,
        paper_jar='paper.jar',
        java_executable='java',
    )

    assert is_successful(result)
    argv = result.unwrap().argv()
    assert is_successful(argv)
    tokens = argv.unwrap()
    assert '--online-mode' not in tokens
    assert '--server-port' not in tokens
    assert '--max-players' not in tokens
    assert '--level-name' not in tokens


def test_cli_values_take_precedence_over_server_properties_values() -> None:
    assert resolve_cli_precedence(False, True) is False
    assert resolve_cli_precedence(25599, 25565) == 25599

    assert resolve_cli_precedence(None, True) is True
    assert resolve_cli_precedence(None, 25565) == 25565

    assert resolve_cli_precedence(None, None) is None


def test_cli_precedence_matches_the_documented_server_properties_counterparts() -> None:
    cli_values: dict[str, int | str | bool] = {
        '--online-mode': False,
        '--server-port': 25599,
        '--max-players': 40,
        '--level-name': 'cli world',
    }
    properties_values: dict[str, int | str | bool] = {
        'online-mode': True,
        'server-port': 25565,
        'max-players': 20,
        'level-name': 'properties world',
    }

    for cli_flag, cli_value in cli_values.items():
        properties_key = cli_flag.removeprefix('--')
        assert resolve_cli_precedence(cli_value, properties_values[properties_key]) == cli_value

    assert resolve_cli_precedence(None, properties_values['server-port']) == 25565
    assert resolve_cli_precedence(None, properties_values['level-name']) == 'properties world'
