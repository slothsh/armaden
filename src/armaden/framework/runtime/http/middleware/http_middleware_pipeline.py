from __future__ import annotations

from collections.abc import Awaitable, Callable
from typing import cast, override

from armaden.framework.protocols.container_protocol import ContainerProtocol
from armaden.framework.protocols.http_middleware_pipeline_protocol import (
    HttpMiddlewarePipelineProtocol,
)
from armaden.framework.protocols.http_request_protocol import HttpRequestProtocol
from armaden.framework.runtime.http.middleware.http_middleware import HttpMiddleware


class HttpMiddlewarePipeline(HttpMiddlewarePipelineProtocol):
    def __init__(
        self,
        middleware_classes: list[type[HttpMiddleware]],
        handler: Callable[[HttpRequestProtocol], Awaitable[object]],
        container: ContainerProtocol | None = None,
    ) -> None:
        self._container: ContainerProtocol | None = container
        self._handler: Callable[[HttpRequestProtocol], Awaitable[object]] = handler
        self._instances: list[HttpMiddleware] = []
        self._middleware_classes: list[type[HttpMiddleware]] = middleware_classes


    async def _build_chain(self, request: HttpRequestProtocol, index: int) -> object:
        if index >= len(self._instances):
            return await self._handler(request)
        current = self._instances[index]

        async def next_handler(next_request: HttpRequestProtocol) -> object:
            return await self._build_chain(next_request, index + 1)

        return await current.handle(request, next_handler)


    @override
    async def send(self, request: HttpRequestProtocol) -> object:
        if self._container is None:
            self._instances = [middleware() for middleware in self._middleware_classes]
        else:
            self._instances = [
                cast(HttpMiddleware, self._container.make(middleware))
                for middleware in self._middleware_classes
            ]
        return await self._build_chain(request, 0)


    @override
    async def terminate(self, request: HttpRequestProtocol, response: object) -> None:
        for middleware in reversed(self._instances):
            try:
                await middleware.terminate(request, response)
            except Exception:
                continue
