from __future__ import annotations

from collections.abc import Coroutine
from typing import Protocol

from armaden.framework.protocols.registers_rcon_command_protocol import (
    RegistersRconCommandProtocol,
)


class RegisteredRconClientProtocol(RegistersRconCommandProtocol, Protocol):
    async def connect(self) -> None: ...

    async def dispatch_command(
        self,
        coroutine: Coroutine[object, object, object],
    ) -> object: ...

    async def dispatch_registered_command(
        self,
        command_name: str,
        **kwargs: object,
    ) -> object: ...
