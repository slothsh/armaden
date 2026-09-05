from __future__ import annotations

from typing import Protocol

from armaden.framework.protocols.http_middleware_protocol import HttpMiddlewareProtocol


class HttpMiddlewareKernelProtocol[M: HttpMiddlewareProtocol](Protocol):
    def bootstrap(self) -> None: ...

    def get_middleware(self) -> list[type[M]]: ...

    def get_middleware_groups(self) -> dict[str, list[str | type[M]]]: ...

    def get_route_middleware(self) -> dict[str, type[M]]: ...

    def resolve_middleware(self, middleware: str | type[M]) -> type[M]: ...

    def resolve_middleware_list(
        self,
        middleware: list[str | type[M]],
    ) -> list[type[M]]: ...
