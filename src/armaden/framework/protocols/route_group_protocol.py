from __future__ import annotations

from contextlib import AbstractContextManager
from typing import Protocol


class RouteGroupProtocol(AbstractContextManager[object], Protocol):

    def middleware(self, *middleware: str) -> RouteGroupProtocol: ...

    def namespace(self, namespace: str) -> RouteGroupProtocol: ...

    def prefix(self, prefix: str) -> RouteGroupProtocol: ...
