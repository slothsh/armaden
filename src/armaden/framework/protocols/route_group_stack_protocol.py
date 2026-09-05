from __future__ import annotations

from typing import Protocol


class RouteGroupStackProtocol[S](Protocol):
    def current(self) -> S | None: ...

    @classmethod
    def get_instance(cls) -> RouteGroupStackProtocol[S]: ...

    def pop(self) -> None: ...

    def push(
        self,
        prefix: str = '',
        middleware: list[str] | None = None,
        namespace: str | None = None,
    ) -> None: ...

    def resolve_handler(self, handler: object) -> object: ...

    def resolve_middleware(self, middleware: list[str]) -> list[str]: ...

    def resolve_path(self, path: str) -> str: ...
