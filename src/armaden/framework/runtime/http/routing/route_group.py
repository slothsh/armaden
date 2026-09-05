from __future__ import annotations

from typing import override

from armaden.framework.protocols.route_group_protocol import RouteGroupProtocol
from armaden.framework.runtime.http.routing.route_group_stack import RouteGroupStack


class RouteGroup(RouteGroupProtocol):
    def __init__(
        self,
        prefix: str = '',
        middleware: list[str] | None = None,
        namespace: str | None = None,
    ) -> None:
        self._middleware: list[str] = list(middleware or [])
        self._namespace: str | None = namespace
        self._prefix: str = prefix


    def __enter__(self) -> RouteGroup:
        RouteGroupStack.get_instance().push(
            prefix=self._prefix,
            middleware=self._middleware,
            namespace=self._namespace,
        )
        return self


    def __exit__(self, *args: object) -> None:
        _ = args
        RouteGroupStack.get_instance().pop()


    @override
    def middleware(self, *middleware: str) -> RouteGroup:
        self._middleware = list(middleware)
        return self


    @override
    def namespace(self, namespace: str) -> RouteGroup:
        self._namespace = namespace
        return self


    @override
    def prefix(self, prefix: str) -> RouteGroup:
        self._prefix = prefix
        return self
