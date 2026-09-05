from __future__ import annotations

from typing import Protocol


class RouteGroupProtocol(Protocol):
    def middleware(self, *middleware: str) -> RouteGroupProtocol: ...

    def namespace(self, namespace: str) -> RouteGroupProtocol: ...

    def prefix(self, prefix: str) -> RouteGroupProtocol: ...
