from __future__ import annotations

from typing import Protocol


class RouteParameterProtocol(Protocol):
    @classmethod
    def parse(cls, path: str) -> tuple[str, dict[str, type[object]]]: ...
