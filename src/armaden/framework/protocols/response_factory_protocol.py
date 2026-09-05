from __future__ import annotations

from collections.abc import Mapping
from typing import Protocol


class ResponseFactoryProtocol(Protocol):
    def json(
        self,
        data: object,
        status: int = 200,
        headers: Mapping[str, str] | None = None,
    ) -> object: ...

    def make(
        self,
        data: object,
        status: int = 200,
        headers: Mapping[str, str] | None = None,
    ) -> object: ...

    def no_content(self, headers: Mapping[str, str] | None = None) -> object: ...