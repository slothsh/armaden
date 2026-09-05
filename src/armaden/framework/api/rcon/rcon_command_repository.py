from __future__ import annotations

from typing import override

from armaden.framework.protocols.rcon_command_protocol import RconCommandProtocol
from armaden.framework.protocols.rcon_command_repository_protocol import (
    RconCommandRepositoryProtocol,
)


class RconCommandRepository(RconCommandRepositoryProtocol):
    def __init__(self) -> None:
        self._by_name: dict[str, RconCommandProtocol] = {}
        self._by_registrar: dict[type[object], list[RconCommandProtocol]] = {}
        self._commands: list[RconCommandProtocol] = []


    @override
    def all(self) -> list[RconCommandProtocol]:
        return list(self._commands)


    @override
    def by_class(self, registrar_cls: type[object]) -> list[RconCommandProtocol]:
        return list(self._by_registrar.get(registrar_cls, []))


    @override
    def get(self, key: str) -> RconCommandProtocol | None:
        return self._by_name.get(key)


    @override
    def register(
        self,
        command: RconCommandProtocol,
        registrar: type[object] | None = None,
    ) -> None:
        self._commands.append(command)
        self._by_name[command.command_name] = command
        if registrar is not None:
            self._by_registrar.setdefault(registrar, []).append(command)


    @override
    def remove(self, key: str) -> None:
        command = self._by_name.pop(key, None)
        if command is None:
            return
        self._commands = [candidate for candidate in self._commands if candidate is not command]
        for registrar, commands in self._by_registrar.items():
            self._by_registrar[registrar] = [
                candidate for candidate in commands if candidate is not command
            ]


__all__ = [
    'RconCommandRepository',
]
