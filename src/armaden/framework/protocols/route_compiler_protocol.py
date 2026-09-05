from __future__ import annotations

from typing import Protocol


class RouteCompilerProtocol[R, T](Protocol):
    def compile(self, routes: list[R], router: T | None = None) -> None: ...
