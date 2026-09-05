from __future__ import annotations

from dataclasses import dataclass


@dataclass
class RouteGroupStateData:
    middleware: list[str]
    namespace: str | None = None
    prefix: str = ''
