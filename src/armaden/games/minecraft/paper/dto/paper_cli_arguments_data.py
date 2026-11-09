from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass, field
from enum import StrEnum
from pathlib import Path
from typing import ClassVar, final

from returns.pipeline import is_successful
from returns.result import Failure, Success

from armaden.framework.api.error import Error
from armaden.framework.types.result import Result
from armaden.games.minecraft.paper.enums import PaperCliFlag


def _parse_value(field_name: str, raw: str) -> Result[str | int | bool]:
    if field_name == 'online_mode':
        if raw == 'true':
            return Success(True)

        if raw == 'false':
            return Success(False)

        return Failure(Error(PaperCliArgumentsError.INVALID_VALUE, details={'field': field_name, 'value': raw}))

    if field_name in ('port', 'max_players'):
        try:
            return Success(int(raw))
        except ValueError:
            return Failure(Error(PaperCliArgumentsError.INVALID_VALUE, details={'field': field_name, 'value': raw}))

    if raw == '':
        return Failure(Error(PaperCliArgumentsError.INVALID_VALUE, details={'field': field_name, 'value': raw}))

    return Success(raw)


def _resolve_path(flag: PaperCliFlag, value: str, working_directory: Path | None) -> Result[str]:
    if working_directory is None or flag not in PaperCliFlag.path_flags() or Path(value).is_absolute():
        return Success(value)

    return Success(str(working_directory / value))


def _serialize_value(field_name: str, flag: PaperCliFlag, value: str | int | bool, working_directory: Path | None) -> Result[str]:
    if field_name == 'online_mode':
        return Success('true' if value is True else 'false')

    if field_name == 'port':
        if not isinstance(value, int) or not 1 <= value <= 65535:
            return Failure(Error(PaperCliArgumentsError.INVALID_VALUE, details={'field': field_name, 'value': value}))

        return Success(str(value))

    if field_name == 'max_players':
        if not isinstance(value, int) or value < 0:
            return Failure(Error(PaperCliArgumentsError.INVALID_VALUE, details={'field': field_name, 'value': value}))

        return Success(str(value))

    if value == '':
        return Failure(Error(PaperCliArgumentsError.INVALID_VALUE, details={'field': field_name, 'value': value}))

    return _resolve_path(flag, str(value), working_directory)


@final
@dataclass
class PaperCliArgumentsData:
    add_plugin_dirs: list[str] = field(default_factory=list)
    add_plugin_jars: list[str] = field(default_factory=list)
    bonus_chest: bool = False
    bukkit_settings: str | None = None
    commands_settings: str | None = None
    config: str | None = None
    demo: bool = False
    erase_cache: bool = False
    force_upgrade: bool = False
    help: bool = False
    host: str | None = None
    init_settings: bool = False
    jfr_profile: bool = False
    level_name: str | None = None
    max_players: int | None = None
    noconsole: bool = False
    nogui: bool = False
    nojline: bool = False
    online_mode: bool | None = None
    paper_dir: str | None = None
    paper_settings: str | None = None
    pid_file: str | None = None
    plugins: str | None = None
    port: int | None = None
    recreate_region_files: bool = False
    safe_mode: bool = False
    server_id: str | None = None
    server_name: str | None = None
    spigot_settings: str | None = None
    universe: str | None = None
    version: bool = False

    VALUE_FIELDS: ClassVar[dict[str, PaperCliFlag]] = {
        'bukkit_settings': PaperCliFlag.BUKKIT_SETTINGS,
        'commands_settings': PaperCliFlag.COMMANDS_SETTINGS,
        'config': PaperCliFlag.CONFIG,
        'host': PaperCliFlag.HOST,
        'level_name': PaperCliFlag.LEVEL_NAME,
        'max_players': PaperCliFlag.MAX_PLAYERS,
        'online_mode': PaperCliFlag.ONLINE_MODE,
        'paper_dir': PaperCliFlag.PAPER_DIR,
        'paper_settings': PaperCliFlag.PAPER_SETTINGS,
        'pid_file': PaperCliFlag.PID_FILE,
        'plugins': PaperCliFlag.PLUGINS,
        'port': PaperCliFlag.PORT,
        'server_id': PaperCliFlag.SERVER_ID,
        'server_name': PaperCliFlag.SERVER_NAME,
        'spigot_settings': PaperCliFlag.SPIGOT_SETTINGS,
        'universe': PaperCliFlag.UNIVERSE,
    }

    BOOL_FIELDS: ClassVar[dict[str, PaperCliFlag]] = {
        'bonus_chest': PaperCliFlag.BONUS_CHEST,
        'demo': PaperCliFlag.DEMO,
        'erase_cache': PaperCliFlag.ERASE_CACHE,
        'force_upgrade': PaperCliFlag.FORCE_UPGRADE,
        'help': PaperCliFlag.HELP,
        'init_settings': PaperCliFlag.INIT_SETTINGS,
        'jfr_profile': PaperCliFlag.JFR_PROFILE,
        'noconsole': PaperCliFlag.NOCONSOLE,
        'nogui': PaperCliFlag.NOGUI,
        'nojline': PaperCliFlag.NOJLINE,
        'recreate_region_files': PaperCliFlag.RECREATE_REGION_FILES,
        'safe_mode': PaperCliFlag.SAFE_MODE,
        'version': PaperCliFlag.VERSION,
    }

    REPEATABLE_FIELDS: ClassVar[dict[str, PaperCliFlag]] = {
        'add_plugin_dirs': PaperCliFlag.ADD_PLUGIN_DIR,
        'add_plugin_jars': PaperCliFlag.ADD_PLUGIN_JAR,
    }

    @classmethod
    def from_tokens(cls, tokens: Sequence[str]) -> Result[PaperCliArgumentsData]:
        arguments = cls()
        assigned: set[str] = set()
        index = 0

        while index < len(tokens):
            token = tokens[index]
            index += 1

            if not is_successful(flag_result := PaperCliFlag.from_token(token)):
                return flag_result.map(lambda _: arguments)

            flag = flag_result.unwrap()

            if flag in PaperCliFlag.repeatable_flags():
                if index >= len(tokens):
                    return Failure(Error(PaperCliArgumentsError.MISSING_VALUE, details={'flag': flag.value}))

                repeatable: list[str] = getattr(arguments, _REPEATABLE_FIELD_NAMES[flag])
                repeatable.append(tokens[index])
                index += 1
                continue

            if flag in PaperCliFlag.value_flags():
                if index >= len(tokens):
                    return Failure(Error(PaperCliArgumentsError.MISSING_VALUE, details={'flag': flag.value}))

                field_name = _VALUE_FIELD_NAMES[flag]

                if field_name in assigned:
                    return Failure(Error(PaperCliArgumentsError.DUPLICATE_OPTION, details={'flag': flag.value}))

                if not is_successful(value_result := _parse_value(field_name, tokens[index])):
                    return value_result.map(lambda _: arguments)

                setattr(arguments, field_name, value_result.unwrap())
                assigned.add(field_name)
                index += 1
                continue

            setattr(arguments, _BOOL_FIELD_NAMES[flag], True)

        return Success(arguments)


    def is_migration_only(self) -> bool:
        return self.paper_settings is not None


    def prevents_server_start(self) -> bool:
        return self.help or self.version


    def to_tokens(self, working_directory: Path | None = None) -> Result[list[str]]:
        tokens: list[str] = []

        for field_name, flag in self.REPEATABLE_FIELDS.items():
            for value in getattr(self, field_name):
                if not is_successful(resolved := _resolve_path(flag, value, working_directory)):
                    return resolved.map(lambda _: tokens)

                tokens.append(flag.value)
                tokens.append(resolved.unwrap())

        for field_name, flag in self.BOOL_FIELDS.items():
            if getattr(self, field_name) is True:
                tokens.append(flag.value)

        for field_name, flag in self.VALUE_FIELDS.items():
            value = getattr(self, field_name)

            if value is None:
                continue

            if not is_successful(serialized := _serialize_value(field_name, flag, value, working_directory)):
                return serialized.map(lambda _: tokens)

            tokens.append(flag.value)
            tokens.append(serialized.unwrap())

        return Success(tokens)


_VALUE_FIELD_NAMES: dict[PaperCliFlag, str] = {flag: name for name, flag in PaperCliArgumentsData.VALUE_FIELDS.items()}
_BOOL_FIELD_NAMES: dict[PaperCliFlag, str] = {flag: name for name, flag in PaperCliArgumentsData.BOOL_FIELDS.items()}
_REPEATABLE_FIELD_NAMES: dict[PaperCliFlag, str] = {flag: name for name, flag in PaperCliArgumentsData.REPEATABLE_FIELDS.items()}


# --- Internal Types ----------------------------------------------------------

class PaperCliArgumentsError(StrEnum):
    DUPLICATE_OPTION = 'the paper cli option does not accept being set more than once'
    INVALID_VALUE = 'the value provided for the paper cli argument is invalid'
    MISSING_VALUE = 'the value provided for the paper cli argument is missing'
