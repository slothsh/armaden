from __future__ import annotations

from pathlib import Path

from typing import cast

from returns.pipeline import is_successful
from armaden.framework.api.error import Error

from armaden.games.minecraft.paper.configuration.server_properties import (
    ServerPropertiesData,
    ServerPropertiesError,
    ServerPropertiesFile,
)
from tests.games.minecraft.paper.paper_reference import SERVER_PROPERTIES_SNAPSHOT, SERVER_PROPERTIES_URL

USER_FILE = '''\
#Minecraft server properties
#Sat Nov 07 14:00:00 CET 2026
motd=My & Server: The Best #1
server-port=25565
unknown-future-property=keep me
'''


def test_reference_snapshot_is_recorded() -> None:
    assert SERVER_PROPERTIES_URL == 'https://docs.papermc.io/paper/reference/server-properties/'
    assert SERVER_PROPERTIES_SNAPSHOT['commit'] == '09e1a6a'


def test_every_documented_property_is_modelled() -> None:
    assert len(ServerPropertiesData.KEYS) == 69
    assert set(ServerPropertiesData.KEYS) == {
        'accept_transfers', 'allow_flight', 'broadcast_console_to_ops', 'broadcast_rcon_to_ops',
        'bug_report_link', 'chat_spam_threshold_seconds', 'command_spam_threshold_seconds', 'debug',
        'difficulty', 'enable_code_of_conduct', 'enable_jmx_monitoring', 'enable_query',
        'enable_rcon', 'enable_status', 'enforce_secure_profile', 'enforce_whitelist',
        'entity_broadcast_range_percentage', 'force_gamemode', 'function_permission_level',
        'gamemode', 'generate_structures', 'generator_settings', 'hardcore', 'hide_online_players',
        'initial_disabled_packs', 'initial_enabled_packs', 'level_name', 'level_seed', 'level_type',
        'log_ips', 'management_server_enabled', 'management_server_host', 'management_server_port',
        'management_server_secret', 'management_server_tls_enabled', 'management_server_tls_keystore',
        'management_server_tls_keystore_password', 'max_chained_neighbor_updates', 'max_players',
        'max_tick_time', 'max_world_size', 'motd', 'network_compression_threshold', 'online_mode',
        'op_permission_level', 'pause_when_empty_seconds', 'player_idle_timeout',
        'prevent_proxy_connections', 'query_port', 'rate_limit', 'rcon_password', 'rcon_port',
        'region_file_compression', 'require_resource_pack', 'resource_pack', 'resource_pack_id',
        'resource_pack_prompt', 'resource_pack_sha1', 'server_ip', 'server_port',
        'simulation_distance', 'spawn_protection', 'status_heartbeat_interval', 'sync_chunk_writes',
        'text_filtering_config', 'text_filtering_version', 'use_native_transport',
        'view_distance', 'white_list',
    }


def test_documented_keys_preserve_paper_spelling() -> None:
    keys = ServerPropertiesData.KEYS

    assert keys['query_port'] == 'query.port'
    assert keys['rcon_password'] == 'rcon.password'
    assert keys['rcon_port'] == 'rcon.port'
    assert keys['enable_rcon'] == 'enable-rcon'
    assert keys['entity_broadcast_range_percentage'] == 'entity-broadcast-range-percentage'
    assert keys['pause_when_empty_seconds'] == 'pause-when-empty-seconds'


def test_defaults_match_the_documented_reference_values() -> None:
    defaults = ServerPropertiesData.defaults()

    assert len(defaults) == 69
    assert defaults['accept-transfers'] == 'false'
    assert defaults['difficulty'] == 'easy'
    assert defaults['gamemode'] == 'survival'
    assert defaults['level-name'] == 'world'
    assert defaults['level-type'] == 'minecraft:normal'
    assert defaults['max-players'] == '20'
    assert defaults['motd'] == 'A Minecraft Server'
    assert defaults['online-mode'] == 'true'
    assert defaults['query.port'] == '25565'
    assert defaults['rcon.port'] == '25575'
    assert defaults['region-file-compression'] == 'deflate'
    assert defaults['server-port'] == '25565'
    assert defaults['simulation-distance'] == '10'
    assert defaults['spawn-protection'] == '16'
    assert defaults['sync-chunk-writes'] == 'true'
    assert defaults['use-native-transport'] == 'true'
    assert defaults['view-distance'] == '10'
    assert defaults['white-list'] == 'true'
    assert defaults['management-server-tls-enabled'] == 'true'
    assert defaults['status-heartbeat-interval'] == '0'


def test_apply_writes_only_set_values_and_preserves_user_content(tmp_path: Path) -> None:
    path = tmp_path / 'server.properties'
    _ = path.write_text(USER_FILE, encoding='utf-8')
    store = ServerPropertiesFile(path)

    result = store.apply(ServerPropertiesData(motd='Brand New & Improved: yes', server_port=25599, online_mode=False))

    assert is_successful(result)
    text = path.read_text(encoding='utf-8')
    assert 'motd=Brand New & Improved\\: yes' in text
    assert 'server-port=25599' in text
    assert 'online-mode=false' in text
    assert '#Minecraft server properties' in text
    assert 'unknown-future-property=keep me' in text
    assert 'difficulty=easy' not in text


def test_absent_and_none_properties_never_overwrite_user_files(tmp_path: Path) -> None:
    path = tmp_path / 'server.properties'
    _ = path.write_text(USER_FILE, encoding='utf-8')
    store = ServerPropertiesFile(path)
    before = path.read_text(encoding='utf-8')

    result = store.apply(ServerPropertiesData())

    assert is_successful(result)
    assert path.read_text(encoding='utf-8') == before

    result = store.ensure(ServerPropertiesData())

    assert is_successful(result)
    assert path.read_text(encoding='utf-8') == before


def test_apply_is_idempotent(tmp_path: Path) -> None:
    path = tmp_path / 'server.properties'
    _ = path.write_text(USER_FILE, encoding='utf-8')
    store = ServerPropertiesFile(path)
    values = ServerPropertiesData(motd='Stable', server_port=25599)

    assert is_successful(store.apply(values))
    first = path.read_text(encoding='utf-8')
    assert is_successful(store.apply(values))

    assert path.read_text(encoding='utf-8') == first


def test_ensure_generates_the_documented_defaults_when_missing(tmp_path: Path) -> None:
    path = tmp_path / 'server.properties'
    store = ServerPropertiesFile(path)

    result = store.ensure(ServerPropertiesData(server_port=25599, motd='Configured'))

    assert is_successful(result)
    text = path.read_text(encoding='utf-8')
    assert 'server-port=25599' in text
    assert 'motd=Configured' in text
    assert 'difficulty=easy' in text
    assert 'white-list=true' in text

    tree = store.read()
    assert is_successful(tree)
    data = tree.unwrap()
    assert data.server_port == 25599
    assert data.motd == 'Configured'
    assert data.difficulty == 'easy'
    assert data.white_list is True


def test_read_parses_typed_values(tmp_path: Path) -> None:
    path = tmp_path / 'server.properties'
    _ = path.write_text(USER_FILE, encoding='utf-8')
    store = ServerPropertiesFile(path)

    result = store.read()

    assert is_successful(result)
    data = result.unwrap()
    assert data.motd == 'My & Server: The Best #1'
    assert data.server_port == 25565
    assert data.online_mode is None
    assert data.difficulty is None


def test_read_returns_unset_data_for_a_missing_file(tmp_path: Path) -> None:
    store = ServerPropertiesFile(tmp_path / 'server.properties')

    result = store.read()

    assert is_successful(result)
    assert result.unwrap() == ServerPropertiesData()


def test_documented_allowed_values_are_enforced(tmp_path: Path) -> None:
    store = ServerPropertiesFile(tmp_path / 'server.properties')

    for invalid in (
        ServerPropertiesData(difficulty='impossible'),
        ServerPropertiesData(gamemode='sandbox'),
        ServerPropertiesData(region_file_compression='brotli'),
    ):
        result = store.apply(invalid)

        assert not is_successful(result)
        assert cast(Error, result.failure()).context == ServerPropertiesError.INVALID_VALUE.value

    assert is_successful(store.apply(ServerPropertiesData(difficulty='hard')))
    assert is_successful(store.apply(ServerPropertiesData(level_type='minecraft:flat')))
    assert is_successful(store.apply(ServerPropertiesData(level_type='normal')))


def test_documented_ranges_are_enforced(tmp_path: Path) -> None:
    store = ServerPropertiesFile(tmp_path / 'server.properties')

    for invalid in (
        ServerPropertiesData(entity_broadcast_range_percentage=5),
        ServerPropertiesData(entity_broadcast_range_percentage=2000),
        ServerPropertiesData(function_permission_level=5),
        ServerPropertiesData(op_permission_level=-1),
        ServerPropertiesData(simulation_distance=2),
        ServerPropertiesData(view_distance=33),
        ServerPropertiesData(text_filtering_version=2),
    ):
        result = store.apply(invalid)

        assert not is_successful(result)
        assert cast(Error, result.failure()).context == ServerPropertiesError.INVALID_VALUE.value

    assert is_successful(store.apply(ServerPropertiesData(view_distance=32)))
    assert is_successful(store.apply(ServerPropertiesData(op_permission_level=0)))


def test_read_rejects_mistyped_document_values(tmp_path: Path) -> None:
    path = tmp_path / 'server.properties'
    _ = path.write_text('view-distance=very-far\n', encoding='utf-8')
    store = ServerPropertiesFile(path)

    result = store.read()

    assert not is_successful(result)
    assert cast(Error, result.failure()).context == ServerPropertiesError.INVALID_VALUE.value


def test_round_trip_through_write_and_read(tmp_path: Path) -> None:
    path = tmp_path / 'server.properties'
    store = ServerPropertiesFile(path)
    values = ServerPropertiesData(
        difficulty='hard',
        enable_rcon=True,
        level_name='round trip world',
        max_players=64,
        motd='A & B: round trip',
        online_mode=False,
        rcon_password='secret=with=equals',
        rcon_port=25580,
        white_list=True,
    )

    assert is_successful(store.apply(values))

    read_back = store.read()
    assert is_successful(read_back)
    assert read_back.unwrap() == values


def test_from_server_config_maps_the_public_server_group() -> None:
    data = ServerPropertiesData.from_server_config({
        'difficulty': 'hard',
        'gamemode': 'creative',
        'levelName': 'my world',
        'levelSeed': '12345',
        'maxPlayers': 5,
        'motd': 'Custom MOTD',
        'onlineMode': False,
        'pvp': True,
        'serverPort': 25599,
        'simulationDistance': 8,
        'viewDistance': 12,
        'whiteList': True,
    })

    assert data.difficulty == 'hard'
    assert data.gamemode == 'creative'
    assert data.level_name == 'my world'
    assert data.level_seed == '12345'
    assert data.max_players == 5
    assert data.motd == 'Custom MOTD'
    assert data.online_mode is False
    assert data.server_port == 25599
    assert data.simulation_distance == 8
    assert data.view_distance == 12
    assert data.white_list is True


def test_from_server_config_leaves_unmapped_keys_unset() -> None:
    data = ServerPropertiesData.from_server_config({'pvp': True})

    assert data == ServerPropertiesData()
