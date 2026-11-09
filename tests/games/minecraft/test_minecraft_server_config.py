from __future__ import annotations

from typing import cast

from armaden.games.minecraft import (
    DEFAULT_MINECRAFT_SERVER_CONFIG,
    MinecraftServer,
    MinecraftServerBackend,
    MinecraftServerConfig,
)


def test_default_config_selects_paper_backend() -> None:
    assert DEFAULT_MINECRAFT_SERVER_CONFIG.get('backend') == MinecraftServerBackend.PAPER


def test_default_config_prefers_java_25_without_executable_override() -> None:
    java = DEFAULT_MINECRAFT_SERVER_CONFIG.get('java')
    assert java is not None
    assert java.get('executable') is None
    assert java.get('version') == 25


def test_default_config_accepts_eula_by_default() -> None:
    eula = DEFAULT_MINECRAFT_SERVER_CONFIG.get('eula')
    assert eula is not None
    assert eula.get('accepted') is True


def test_default_config_leaves_server_properties_unset() -> None:
    assert DEFAULT_MINECRAFT_SERVER_CONFIG.get('server') is None


def test_default_config_leaves_paper_version_and_build_unpinned() -> None:
    paper = DEFAULT_MINECRAFT_SERVER_CONFIG.get('paper')
    assert paper is not None
    assert paper.get('version') is None
    assert paper.get('build') is None


def test_default_config_is_a_complete_typed_config() -> None:
    config: MinecraftServerConfig = MinecraftServerConfig(
        **DEFAULT_MINECRAFT_SERVER_CONFIG
    )
    assert config == DEFAULT_MINECRAFT_SERVER_CONFIG


def test_server_without_config_uses_default_configuration() -> None:
    server = MinecraftServer()
    assert server.config == DEFAULT_MINECRAFT_SERVER_CONFIG


def test_server_merges_deep_partial_overrides() -> None:
    server = MinecraftServer(
        config={'server': {'motd': 'Custom MOTD', 'maxPlayers': 5}}
    )

    server_properties = server.config.get('server')
    assert server_properties is not None
    assert server_properties.get('motd') == 'Custom MOTD'
    assert server_properties.get('maxPlayers') == 5
    assert server_properties.get('difficulty') is None
    assert server_properties.get('serverPort') is None

    java = server.config.get('java')
    assert java is not None
    assert java.get('version') == 25


def test_partial_server_properties_remain_unset() -> None:
    server = MinecraftServer(config={'server': {'motd': 'Custom MOTD'}})

    server_properties = server.config.get('server')
    assert server_properties is not None
    assert server_properties == {'motd': 'Custom MOTD'}
    assert server_properties.get('onlineMode') is None
    assert server_properties.get('levelName') is None


def test_server_merge_replaces_scalars_but_preserves_unspecified_groups() -> None:
    server = MinecraftServer(
        config={
            'backend': MinecraftServerBackend.PAPER,
            'paper': {'version': '1.21.4', 'build': 130},
        }
    )

    paper = server.config.get('paper')
    assert paper is not None
    assert paper.get('version') == '1.21.4'
    assert paper.get('build') == 130

    assert server.config.get('arguments') == DEFAULT_MINECRAFT_SERVER_CONFIG.get(
        'arguments'
    )
    assert server.config.get('jvm') == DEFAULT_MINECRAFT_SERVER_CONFIG.get('jvm')


def test_server_none_overrides_keep_default_values() -> None:
    server = MinecraftServer(
        config={
            'backend': None,
            'eula': None,
            'installation': None,
            'java': {'executable': None, 'version': None},
            'paper': {'build': None, 'version': None},
        }
    )

    assert server.config.get('backend') == MinecraftServerBackend.PAPER
    assert server.config.get('eula') == DEFAULT_MINECRAFT_SERVER_CONFIG.get('eula')
    assert server.config.get('java') == DEFAULT_MINECRAFT_SERVER_CONFIG.get('java')


def test_server_none_cannot_clear_non_none_default() -> None:
    server = MinecraftServer(
        config={'arguments': {'nogui': None}, 'java': {'version': None}}
    )

    arguments = server.config.get('arguments')
    assert arguments is not None
    assert arguments.get('nogui') is True

    java = server.config.get('java')
    assert java is not None
    assert java.get('version') == 25


def test_server_filters_unknown_top_level_keys() -> None:
    raw_config: object = {'unknown': 'value'}
    server = MinecraftServer(
        config=cast(MinecraftServerConfig, cast(object, raw_config))
    )

    assert 'unknown' not in server.config
    assert server.config.get('backend') == MinecraftServerBackend.PAPER


def test_server_instances_do_not_share_nested_configuration() -> None:
    first = MinecraftServer()
    second = MinecraftServer()

    first_java = first.config.get('java')
    assert first_java is not None
    first_java['version'] = 17

    first_jvm = first.config.get('jvm')
    assert first_jvm is not None
    first_options = first_jvm.get('options')
    assert first_options is not None
    first_options.append('-Xss1M')

    second_java = second.config.get('java')
    assert second_java is not None
    assert second_java.get('version') == 25

    second_jvm = second.config.get('jvm')
    assert second_jvm is not None
    second_options = second_jvm.get('options')
    assert second_options is not None
    assert second_options == []


def test_server_mutation_cannot_affect_exported_defaults() -> None:
    server = MinecraftServer()

    server_java = server.config.get('java')
    assert server_java is not None
    server_java['version'] = 17

    server_jvm = server.config.get('jvm')
    assert server_jvm is not None
    server_options = server_jvm.get('options')
    assert server_options is not None
    server_options.append('-Xss1M')

    default_java = DEFAULT_MINECRAFT_SERVER_CONFIG.get('java')
    assert default_java is not None
    assert default_java.get('version') == 25

    default_jvm = DEFAULT_MINECRAFT_SERVER_CONFIG.get('jvm')
    assert default_jvm is not None
    default_options = default_jvm.get('options')
    assert default_options is not None
    assert default_options == []


def test_caller_nested_configuration_is_copied() -> None:
    caller: object = {
        'server': {'motd': 'Original'},
        'jvm': {'options': ['-Xmx2G']},
    }
    server = MinecraftServer(config=cast(MinecraftServerConfig, cast(object, caller)))

    caller_config = cast(dict[str, object], cast(object, caller))
    caller_server = cast(dict[str, object], caller_config['server'])
    caller_server['motd'] = 'Mutated'
    caller_server['levelName'] = 'injected'

    caller_jvm = cast(dict[str, object], caller_config['jvm'])
    caller_options = cast(list[object], caller_jvm['options'])
    caller_options.append('-Xss1M')

    server_properties = server.config.get('server')
    assert server_properties is not None
    assert server_properties.get('motd') == 'Original'
    assert server_properties.get('levelName') is None

    server_jvm = server.config.get('jvm')
    assert server_jvm is not None
    server_options = server_jvm.get('options')
    assert server_options == ['-Xmx2G']