from __future__ import annotations

from collections.abc import Mapping
from typing import Protocol


class UrlGeneratorProtocol(Protocol):
    def current(self) -> str: ...

    def full(self) -> str: ...

    def has(self, name: str) -> bool: ...

    def previous(self, fallback: str = '/') -> str: ...

    def register(
        self,
        name: str,
        path: str,
        methods: list[str],
        parameters: Mapping[str, type[object]],
    ) -> None: ...

    def route(
        self,
        name: str,
        parameters: Mapping[str, object] | None = None,
        absolute: bool = True,
    ) -> str: ...

    def to(
        self,
        path: str,
        parameters: Mapping[str, object] | None = None,
        absolute: bool = True,
    ) -> str: ...
