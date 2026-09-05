from __future__ import annotations

from typing import Protocol

from armaden.framework.protocols.rcon_command_protocol import RconCommandProtocol


class RconCommandRepositoryProtocol(Protocol):
    def all(self) -> list[RconCommandProtocol]: ...

    def by_class(self, registrar_cls: type[object]) -> list[RconCommandProtocol]: ...

    def get(self, key: str) -> RconCommandProtocol | None: ...

    def register(
        self,
        command: RconCommandProtocol,
        registrar: type[object] | None = None,
    ) -> None: ...

    def remove(self, key: str) -> None: ...
