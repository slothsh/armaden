from __future__ import annotations

from typing import Protocol, runtime_checkable

from armaden.framework.protocols.rcon_command import RconCommandInterface, SendCommandProtocol


@runtime_checkable
class RegistersRconCommand(Protocol):
    @property
    def client(self) -> SendCommandProtocol:
        ...

    def register_rcon_command(self, command: RconCommandInterface) -> None:
        ...
