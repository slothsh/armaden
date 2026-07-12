from __future__ import annotations

import logging
from typing import Dict, List

from armaden.framework.protocols.rcon_command import RconCommandInterface

logger = logging.getLogger(__name__)


class RconCommandRepository:
    def __init__(self) -> None:
        self._commands: List[RconCommandInterface] = []
        self._by_name: Dict[str, RconCommandInterface] = {}
        self._by_registrar: Dict[type, List[RconCommandInterface]] = {}

    def register(
        self,
        command: RconCommandInterface,
        registrar: type | None = None,
    ) -> None:
        self._commands.append(command)
        self._by_name[command.command_name] = command
        if registrar is not None:
            self._by_registrar.setdefault(registrar, []).append(command)

    def get(self, key: str) -> RconCommandInterface | None:
        return self._by_name.get(key)

    def all(self) -> list[RconCommandInterface]:
        return list(self._commands)

    def by_class(self, registrar_cls: type) -> list[RconCommandInterface]:
        return list(self._by_registrar.get(registrar_cls, []))

    def remove(self, key: str) -> None:
        command = self._by_name.pop(key, None)
        if command is None:
            return
        self._commands = [c for c in self._commands if c is not command]
        for registrar, commands in self._by_registrar.items():
            self._by_registrar[registrar] = [c for c in commands if c is not command]
