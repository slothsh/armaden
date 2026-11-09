from __future__ import annotations

from pathlib import Path

from returns.pipeline import is_successful

from armaden.games.minecraft.paper.configuration.server_properties import (
    ServerPropertiesData,
    ServerPropertiesFile,
)
from armaden.games.minecraft.paper.dto import (
    PaperCliArgumentsData,
    PaperJvmLaunchData,
    PaperLaunchConfigData,
)
from armaden.games.minecraft.paper.enums import PaperSystemProperty
from armaden.games.minecraft.paper.paper_launch_command import (
    PaperLaunchCommand,
    resolve_cli_precedence,
)


def test_configuration_writing_is_independent_from_cli_overrides(tmp_path: Path) -> None:
    path = tmp_path / 'server.properties'
    store = ServerPropertiesFile(path)

    launch = PaperLaunchCommand(
        PaperLaunchConfigData(
            cli_arguments=PaperCliArgumentsData(port=25599, online_mode=False),
            jvm=PaperJvmLaunchData(system_properties={PaperSystemProperty.EULA_AGREE: True}),
        ),
        java_executable='java',
        paper_jar='paper.jar',
    )

    result = store.ensure(ServerPropertiesData.from_server_config({'serverPort': 25565, 'onlineMode': True}))

    assert is_successful(result)
    assert is_successful(launch.argv())

    text = path.read_text(encoding='utf-8')
    assert 'server-port=25565' in text
    assert 'online-mode=true' in text

    argv = launch.argv().unwrap()
    assert '--port' in argv and '25599' in argv
    assert '--online-mode' in argv and 'false' in argv
    assert '-Dcom.mojang.eula.agree=true' in argv


def test_cli_arguments_never_materialize_in_configuration_files(tmp_path: Path) -> None:
    path = tmp_path / 'server.properties'
    _ = path.write_text('server-port=25565\nonline-mode=true\n', encoding='utf-8')
    store = ServerPropertiesFile(path)

    launch = PaperLaunchCommand(
        PaperLaunchConfigData(cli_arguments=PaperCliArgumentsData(port=25599, server_name='CLI side')),
        java_executable='java',
        paper_jar='paper.jar',
    )

    assert is_successful(store.apply(ServerPropertiesData()))

    text = path.read_text(encoding='utf-8')
    assert 'server-port=25565' in text
    assert 'online-mode=true' in text
    assert '--port' not in text
    assert '--server-name' not in text
    assert 'CLI side' not in text

    argv = launch.argv().unwrap()
    assert '--port' in argv and '--server-name' in argv


def test_documented_cli_precedence_applies_when_both_surfaces_are_configured() -> None:
    assert resolve_cli_precedence(25599, 25565) == 25599
    assert resolve_cli_precedence(False, True) is False
    assert resolve_cli_precedence(None, 25565) == 25565
