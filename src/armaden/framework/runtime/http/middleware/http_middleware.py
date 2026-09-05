from __future__ import annotations

from abc import ABC, abstractmethod
from typing import override

from armaden.framework.protocols.http_middleware_protocol import (
    HttpMiddlewareProtocol,
    NextCallable,
)
from armaden.framework.protocols.http_request_protocol import HttpRequestProtocol


class HttpMiddleware(HttpMiddlewareProtocol, ABC):
    def __init__(self) -> None:
        pass


    @abstractmethod
    @override
    async def handle(
        self,
        request: HttpRequestProtocol,
        next: NextCallable,
    ) -> object:
        raise NotImplementedError


    @override
    async def terminate(self, request: HttpRequestProtocol, response: object) -> None:
        _ = request
        _ = response
