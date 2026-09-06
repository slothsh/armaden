from __future__ import annotations

from abc import ABC

from armaden.framework.protocols.rcon_server_message_handler_protocol import RconServerMessageHandlerProtocol


class RconServerMessageHandler(RconServerMessageHandlerProtocol, ABC):
    pass


__all__ = [
    'RconServerMessageHandler',
]
