from __future__ import annotations

from typing import Protocol

from armaden.framework.types.result import Result


class RconServerMessageHandlerProtocol(Protocol):
    name: str
    category: str
    description: str

    async def handle(self, server_message: str) -> Result[None]: ...
