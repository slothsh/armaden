from __future__ import annotations

from typing import Protocol

from armaden.framework.protocols.rcon_server_message_handler_protocol import RconServerMessageHandlerProtocol


class RegistersRconServerMessageHandlerProtocol(Protocol):
    def register_rcon_server_message_handler(self, handler: RconServerMessageHandlerProtocol) -> None: ...
