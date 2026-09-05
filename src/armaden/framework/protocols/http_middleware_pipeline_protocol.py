from __future__ import annotations

from typing import Protocol

from armaden.framework.protocols.http_request_protocol import HttpRequestProtocol


class HttpMiddlewarePipelineProtocol(Protocol):
    async def send(self, request: HttpRequestProtocol) -> object: ...

    async def terminate(self, request: HttpRequestProtocol, response: object) -> None: ...
