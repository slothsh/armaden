from __future__ import annotations

from typing import Protocol

from armaden.framework.protocols.rcon_command_protocol import RconCommandProtocol
from armaden.framework.protocols.rcon_send_command_protocol import RconSendCommandProtocol


class RegistersRconCommandProtocol(Protocol):
    @property
    def client(self) -> RconSendCommandProtocol: ...

    def register_rcon_command(self, command: RconCommandProtocol) -> None: ...
