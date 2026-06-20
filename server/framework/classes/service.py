from abc import ABC, abstractmethod
from typing import Any, Generic, Mapping, TypeVar

from returns.result import Success

from framework.enums.health_status import HealthStatus
from ..utils.types import Result

H = TypeVar("H", bound=Mapping[str, Any])

class Service(ABC, Generic[H]):
    name: str

    @abstractmethod
    def __call__(self, *args: Any, **kwargs: Any) -> Result[None]: ...


    async def status(self) -> Result[Mapping[str, Any]]:
        return Success({ self.name: HealthStatus.OK })
