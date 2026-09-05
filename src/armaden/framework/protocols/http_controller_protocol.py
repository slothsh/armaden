from __future__ import annotations

from collections.abc import Mapping
from typing import Protocol


class HttpControllerProtocol(Protocol):
    @classmethod
    def get_middleware(cls) -> dict[str, Mapping[str, object]]: ...

    @classmethod
    def get_middleware_for_method(cls, method_name: str) -> list[str]: ...