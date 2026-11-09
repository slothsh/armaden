from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path
from typing import ClassVar, final

from javaproperties.propfile import PropertiesFile
from returns.pipeline import is_successful
from returns.result import Failure, Success

from armaden.framework.api.error import Error
from armaden.framework.types.result import Result
from armaden.games.minecraft.minecraft_server_config import ServerPropertiesConfig


@final
@dataclass
class ServerPropertiesData:
    accept_transfers: bool | None = None
    allow_flight: bool | None = None
    broadcast_console_to_ops: bool | None = None
    broadcast_rcon_to_ops: bool | None = None
    bug_report_link: str | None = None
    chat_spam_threshold_seconds: int | None = None
    command_spam_threshold_seconds: int | None = None
    debug: bool | None = None
    difficulty: str | None = None
    enable_code_of_conduct: bool | None = None
    enable_jmx_monitoring: bool | None = None
    enable_query: bool | None = None
    enable_rcon: bool | None = None
    enable_status: bool | None = None
    enforce_secure_profile: bool | None = None
    enforce_whitelist: bool | None = None
    entity_broadcast_range_percentage: int | None = None
    force_gamemode: bool | None = None
    function_permission_level: int | None = None
    gamemode: str | None = None
    generate_structures: bool | None = None
    generator_settings: str | None = None
    hardcore: bool | None = None
    hide_online_players: bool | None = None
    initial_disabled_packs: str | None = None
    initial_enabled_packs: str | None = None
    level_name: str | None = None
    level_seed: str | None = None
    level_type: str | None = None
    log_ips: bool | None = None
    management_server_enabled: bool | None = None
    management_server_host: str | None = None
    management_server_port: int | None = None
    management_server_secret: str | None = None
    management_server_tls_enabled: bool | None = None
    management_server_tls_keystore: str | None = None
    management_server_tls_keystore_password: str | None = None
    max_chained_neighbor_updates: int | None = None
    max_players: int | None = None
    max_tick_time: int | None = None
    max_world_size: int | None = None
    motd: str | None = None
    network_compression_threshold: int | None = None
    online_mode: bool | None = None
    op_permission_level: int | None = None
    pause_when_empty_seconds: int | None = None
    player_idle_timeout: int | None = None
    prevent_proxy_connections: bool | None = None
    query_port: int | None = None
    rate_limit: int | None = None
    rcon_password: str | None = None
    rcon_port: int | None = None
    region_file_compression: str | None = None
    require_resource_pack: bool | None = None
    resource_pack: str | None = None
    resource_pack_id: str | None = None
    resource_pack_prompt: str | None = None
    resource_pack_sha1: str | None = None
    server_ip: str | None = None
    server_port: int | None = None
    simulation_distance: int | None = None
    spawn_protection: int | None = None
    status_heartbeat_interval: int | None = None
    sync_chunk_writes: bool | None = None
    text_filtering_config: str | None = None
    text_filtering_version: int | None = None
    use_native_transport: bool | None = None
    view_distance: int | None = None
    white_list: bool | None = None

    KEYS: ClassVar[dict[str, str]] = {
        'accept_transfers': 'accept-transfers',
        'allow_flight': 'allow-flight',
        'broadcast_console_to_ops': 'broadcast-console-to-ops',
        'broadcast_rcon_to_ops': 'broadcast-rcon-to-ops',
        'bug_report_link': 'bug-report-link',
        'chat_spam_threshold_seconds': 'chat-spam-threshold-seconds',
        'command_spam_threshold_seconds': 'command-spam-threshold-seconds',
        'debug': 'debug',
        'difficulty': 'difficulty',
        'enable_code_of_conduct': 'enable-code-of-conduct',
        'enable_jmx_monitoring': 'enable-jmx-monitoring',
        'enable_query': 'enable-query',
        'enable_rcon': 'enable-rcon',
        'enable_status': 'enable-status',
        'enforce_secure_profile': 'enforce-secure-profile',
        'enforce_whitelist': 'enforce-whitelist',
        'entity_broadcast_range_percentage': 'entity-broadcast-range-percentage',
        'force_gamemode': 'force-gamemode',
        'function_permission_level': 'function-permission-level',
        'gamemode': 'gamemode',
        'generate_structures': 'generate-structures',
        'generator_settings': 'generator-settings',
        'hardcore': 'hardcore',
        'hide_online_players': 'hide-online-players',
        'initial_disabled_packs': 'initial-disabled-packs',
        'initial_enabled_packs': 'initial-enabled-packs',
        'level_name': 'level-name',
        'level_seed': 'level-seed',
        'level_type': 'level-type',
        'log_ips': 'log-ips',
        'management_server_enabled': 'management-server-enabled',
        'management_server_host': 'management-server-host',
        'management_server_port': 'management-server-port',
        'management_server_secret': 'management-server-secret',
        'management_server_tls_enabled': 'management-server-tls-enabled',
        'management_server_tls_keystore': 'management-server-tls-keystore',
        'management_server_tls_keystore_password': 'management-server-tls-keystore-password',
        'max_chained_neighbor_updates': 'max-chained-neighbor-updates',
        'max_players': 'max-players',
        'max_tick_time': 'max-tick-time',
        'max_world_size': 'max-world-size',
        'motd': 'motd',
        'network_compression_threshold': 'network-compression-threshold',
        'online_mode': 'online-mode',
        'op_permission_level': 'op-permission-level',
        'pause_when_empty_seconds': 'pause-when-empty-seconds',
        'player_idle_timeout': 'player-idle-timeout',
        'prevent_proxy_connections': 'prevent-proxy-connections',
        'query_port': 'query.port',
        'rate_limit': 'rate-limit',
        'rcon_password': 'rcon.password',
        'rcon_port': 'rcon.port',
        'region_file_compression': 'region-file-compression',
        'require_resource_pack': 'require-resource-pack',
        'resource_pack': 'resource-pack',
        'resource_pack_id': 'resource-pack-id',
        'resource_pack_prompt': 'resource-pack-prompt',
        'resource_pack_sha1': 'resource-pack-sha1',
        'server_ip': 'server-ip',
        'server_port': 'server-port',
        'simulation_distance': 'simulation-distance',
        'spawn_protection': 'spawn-protection',
        'status_heartbeat_interval': 'status-heartbeat-interval',
        'sync_chunk_writes': 'sync-chunk-writes',
        'text_filtering_config': 'text-filtering-config',
        'text_filtering_version': 'text-filtering-version',
        'use_native_transport': 'use-native-transport',
        'view_distance': 'view-distance',
        'white_list': 'white-list',
    }

    INT_FIELDS: ClassVar[frozenset[str]] = frozenset({
        'chat_spam_threshold_seconds',
        'command_spam_threshold_seconds',
        'entity_broadcast_range_percentage',
        'function_permission_level',
        'management_server_port',
        'max_chained_neighbor_updates',
        'max_players',
        'max_tick_time',
        'max_world_size',
        'network_compression_threshold',
        'op_permission_level',
        'pause_when_empty_seconds',
        'player_idle_timeout',
        'query_port',
        'rate_limit',
        'rcon_port',
        'server_port',
        'simulation_distance',
        'spawn_protection',
        'status_heartbeat_interval',
        'text_filtering_version',
        'view_distance',
    })

    BOOL_FIELDS: ClassVar[frozenset[str]] = frozenset({
        'accept_transfers',
        'allow_flight',
        'broadcast_console_to_ops',
        'broadcast_rcon_to_ops',
        'debug',
        'enable_code_of_conduct',
        'enable_jmx_monitoring',
        'enable_query',
        'enable_rcon',
        'enable_status',
        'enforce_secure_profile',
        'enforce_whitelist',
        'force_gamemode',
        'generate_structures',
        'hardcore',
        'hide_online_players',
        'log_ips',
        'management_server_enabled',
        'management_server_tls_enabled',
        'online_mode',
        'prevent_proxy_connections',
        'require_resource_pack',
        'sync_chunk_writes',
        'use_native_transport',
        'white_list',
    })

    ALLOWED_VALUES: ClassVar[dict[str, frozenset[str]]] = {
        'difficulty': frozenset({'peaceful', 'easy', 'normal', 'hard'}),
        'gamemode': frozenset({'survival', 'creative', 'adventure', 'spectator'}),
        'level_type': frozenset({
            'normal',
            'flat',
            'large_biomes',
            'amplified',
            'single_biome_surface',
            'buffet',
            'default_1_1',
            'customized',
        }),
        'region_file_compression': frozenset({'deflate', 'lz4', 'none', 'gzip'}),
    }

    INT_RANGES: ClassVar[dict[str, tuple[int, int]]] = {
        'entity_broadcast_range_percentage': (10, 1000),
        'function_permission_level': (1, 4),
        'op_permission_level': (0, 4),
        'simulation_distance': (3, 32),
        'text_filtering_version': (0, 1),
        'view_distance': (3, 32),
    }

    PUBLIC_CONFIG_KEYS: ClassVar[dict[str, str]] = {
        'difficulty': 'difficulty',
        'gamemode': 'gamemode',
        'levelName': 'level_name',
        'levelSeed': 'level_seed',
        'maxPlayers': 'max_players',
        'motd': 'motd',
        'onlineMode': 'online_mode',
        'serverPort': 'server_port',
        'simulationDistance': 'simulation_distance',
        'viewDistance': 'view_distance',
        'whiteList': 'white_list',
    }

    @classmethod
    def defaults(cls) -> dict[str, str]:
        return {
            'accept-transfers': 'false',
            'allow-flight': 'false',
            'broadcast-console-to-ops': 'true',
            'broadcast-rcon-to-ops': 'true',
            'bug-report-link': '',
            'chat-spam-threshold-seconds': '10',
            'command-spam-threshold-seconds': '10',
            'debug': 'false',
            'difficulty': 'easy',
            'enable-code-of-conduct': 'false',
            'enable-jmx-monitoring': 'false',
            'enable-query': 'false',
            'enable-rcon': 'false',
            'enable-status': 'true',
            'enforce-secure-profile': 'true',
            'enforce-whitelist': 'false',
            'entity-broadcast-range-percentage': '100',
            'force-gamemode': 'false',
            'function-permission-level': '2',
            'gamemode': 'survival',
            'generate-structures': 'true',
            'generator-settings': '{}',
            'hardcore': 'false',
            'hide-online-players': 'false',
            'initial-disabled-packs': '',
            'initial-enabled-packs': 'vanilla',
            'level-name': 'world',
            'level-seed': '',
            'level-type': 'minecraft:normal',
            'log-ips': 'true',
            'management-server-enabled': 'false',
            'management-server-host': 'localhost',
            'management-server-port': '0',
            'management-server-secret': '',
            'management-server-tls-enabled': 'true',
            'management-server-tls-keystore': '',
            'management-server-tls-keystore-password': '',
            'max-chained-neighbor-updates': '1000000',
            'max-players': '20',
            'max-tick-time': '60000',
            'max-world-size': '29999984',
            'motd': 'A Minecraft Server',
            'network-compression-threshold': '256',
            'online-mode': 'true',
            'op-permission-level': '4',
            'pause-when-empty-seconds': '-1',
            'player-idle-timeout': '0',
            'prevent-proxy-connections': 'false',
            'query.port': '25565',
            'rate-limit': '0',
            'rcon.password': '',
            'rcon.port': '25575',
            'region-file-compression': 'deflate',
            'require-resource-pack': 'false',
            'resource-pack': '',
            'resource-pack-id': '',
            'resource-pack-prompt': '',
            'resource-pack-sha1': '',
            'server-ip': '',
            'server-port': '25565',
            'simulation-distance': '10',
            'spawn-protection': '16',
            'status-heartbeat-interval': '0',
            'sync-chunk-writes': 'true',
            'text-filtering-config': '',
            'text-filtering-version': '0',
            'use-native-transport': 'true',
            'view-distance': '10',
            'white-list': 'true',
        }

    @classmethod
    def from_server_config(cls, server: ServerPropertiesConfig) -> ServerPropertiesData:
        values = cls()

        for public_key, field_name in cls.PUBLIC_CONFIG_KEYS.items():
            configured = server.get(public_key)

            if configured is not None:
                setattr(values, field_name, configured)

        return values


def _serialize(value: bool | int | str) -> str:
    if value is True:
        return 'true'

    if value is False:
        return 'false'

    return str(value)


def _validate(data: ServerPropertiesData) -> Result[None]:
    for field_name in data.ALLOWED_VALUES:
        value = getattr(data, field_name)

        if value is None:
            continue

        allowed = data.ALLOWED_VALUES[field_name]

        if value in allowed or value.removeprefix('minecraft:') in allowed:
            continue

        return Failure(
            Error(
                ServerPropertiesError.INVALID_VALUE,
                details={'field': field_name, 'value': value, 'allowed': sorted(allowed)},
            )
        )

    for field_name, (minimum, maximum) in data.INT_RANGES.items():
        value = getattr(data, field_name)

        if value is None or minimum <= value <= maximum:
            continue

        return Failure(
            Error(
                ServerPropertiesError.INVALID_VALUE,
                details={'field': field_name, 'value': value, 'range': [minimum, maximum]},
            )
        )

    return Success(None)


def _set_values(properties: PropertiesFile, values: ServerPropertiesData) -> None:
    for field_name, key in ServerPropertiesData.KEYS.items():
        value = getattr(values, field_name)

        if value is not None:
            properties[key] = _serialize(value)


def _parse_field(field_name: str, raw: str) -> Result[bool | int | str]:
    if field_name in ServerPropertiesData.INT_FIELDS:
        try:
            return Success(int(raw))
        except ValueError:
            return Failure(
                Error(ServerPropertiesError.INVALID_VALUE, details={'field': field_name, 'value': raw})
            )

    if field_name in ServerPropertiesData.BOOL_FIELDS:
        if raw == 'true':
            return Success(True)

        if raw == 'false':
            return Success(False)

        return Failure(
            Error(ServerPropertiesError.INVALID_VALUE, details={'field': field_name, 'value': raw})
        )

    return Success(raw)


@final
class ServerPropertiesFile:
    FILE_NAME: ClassVar[str] = 'server.properties'

    def __init__(self, path: Path) -> None:
        self._path: Path = path


    def apply(self, values: ServerPropertiesData) -> Result[None]:
        if not is_successful(validation := _validate(values)):
            return validation

        if not is_successful(properties := self._load_or_empty()):
            return properties.map(lambda _: None)

        _set_values(properties.unwrap(), values)
        return self._write(properties.unwrap().dumps())


    def ensure(self, values: ServerPropertiesData) -> Result[None]:
        if self._path.exists():
            return self.apply(values)

        if not is_successful(validation := _validate(values)):
            return validation

        properties = PropertiesFile(ServerPropertiesData.defaults())
        _set_values(properties, values)
        return self._write(properties.dumps())


    def read(self) -> Result[ServerPropertiesData]:
        if not self._path.exists():
            return Success(ServerPropertiesData())

        if not is_successful(raw := self._read_text()):
            return Failure(raw.failure())

        if not is_successful(properties := self._parse(raw.unwrap())):
            return Failure(properties.failure())

        parsed = ServerPropertiesData()

        for field_name, key in ServerPropertiesData.KEYS.items():
            raw_value = properties.unwrap().get(key)

            if raw_value is None:
                continue

            if not is_successful(value := _parse_field(field_name, raw_value)):
                return Failure(value.failure())

            setattr(parsed, field_name, value.unwrap())

        return Success(parsed)


    def _parse(self, raw: str) -> Result[PropertiesFile]:
        try:
            return Success(PropertiesFile.loads(raw))
        except ValueError as failure:
            return Failure(
                Error(
                    ServerPropertiesError.INVALID_DOCUMENT,
                    details={'path': str(self._path), 'error': str(failure)},
                )
            )


    def _load_or_empty(self) -> Result[PropertiesFile]:
        if not self._path.exists():
            return Success(PropertiesFile())

        if not is_successful(raw := self._read_text()):
            return Failure(raw.failure())

        return self._parse(raw.unwrap())


    def _read_text(self) -> Result[str]:
        try:
            return Success(self._path.read_text(encoding='utf-8'))
        except OSError as failure:
            return Failure(
                Error(
                    ServerPropertiesError.READ_FAILED,
                    details={'path': str(self._path), 'error': str(failure)},
                )
            )


    def _write(self, text: str) -> Result[None]:
        try:
            _ = self._path.parent.mkdir(parents=True, exist_ok=True)
            _ = self._path.write_text(text, encoding='utf-8')
        except OSError as failure:
            return Failure(
                Error(
                    ServerPropertiesError.WRITE_FAILED,
                    details={'path': str(self._path), 'error': str(failure)},
                )
            )

        return Success(None)


# --- Internal Types ----------------------------------------------------------

class ServerPropertiesError(StrEnum):
    INVALID_DOCUMENT = 'the server.properties file could not be parsed'
    INVALID_VALUE = 'the server.properties value is invalid for its documented type or range'
    READ_FAILED = 'the server.properties file could not be read'
    WRITE_FAILED = 'the server.properties file could not be written'
