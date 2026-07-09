from abc import ABC, abstractmethod
from typing import Any, Mapping
from returns.result import Success

from ..utils.types import Result


class ApplicationInterface(ABC):
    @abstractmethod
    def boot(self) -> Result[None]: ...

    def route_groups(self) -> dict[str, dict[str, Any]]:
        return {}

    async def status(self) -> Result[Mapping[str, Any]]:
        return Success({})
