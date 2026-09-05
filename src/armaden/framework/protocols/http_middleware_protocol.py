from __future__ import annotations

from collections.abc import Awaitable, Callable
from typing import Protocol

from armaden.framework.protocols.http_request_protocol import HttpRequestProtocol


type NextCallable = Callable[[HttpRequestProtocol], Awaitable[object]]


class HttpMiddlewareProtocol(Protocol):
    async def handle(
        self,
        request: HttpRequestProtocol,
        next: NextCallable,
    ) -> object: ...

    async def terminate(self, request: HttpRequestProtocol, response: object) -> None: ...