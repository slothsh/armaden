from abc import ABC, abstractmethod
from typing import Any, Mapping
from returns.result import Success

from ..utils.types import Result


class ApplicationInterface(ABC):
    @abstractmethod
    def boot(self) -> Result[None]: ...

    @property
    def middleware(self) -> list[type]:
        return []

    @property
    def middleware_groups(self) -> dict[str, list[type]]:
        return {}

    def route_groups(self) -> dict[str, dict[str, Any]]:
        return {}

    async def status(self) -> Result[Mapping[str, Any]]:
        return Success({})
