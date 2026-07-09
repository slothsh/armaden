from typing import Any, Callable

from .middleware import Middleware, NextCallable
from ..request import Request


class MiddlewarePipeline:
    def __init__(
        self,
        middleware_classes: list[type[Middleware]],
        handler: Callable,
        container: Any = None,
    ) -> None:
        self._middleware_classes = middleware_classes
        self._handler = handler
        self._container = container
        self._instances: list[Middleware] = []

    async def send(self, request: Request) -> Any:
        if self._container is not None:
            self._instances = [self._container.make(cls) for cls in self._middleware_classes]
        else:
            self._instances = [cls() for cls in self._middleware_classes]
        return await self._build_chain(request, 0)

    async def terminate(self, request: Request, response: Any) -> None:
        for mw in reversed(self._instances):
            try:
                await mw.terminate(request, response)
            except Exception:
                pass

    async def _build_chain(self, request: Request, index: int) -> Any:
        if index >= len(self._instances):
            return await self._handler(request)
        current = self._instances[index]

        async def _next(req: Request) -> Any:
            return await self._build_chain(req, index + 1)

        return await current.handle(request, _next)
