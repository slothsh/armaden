from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Mapping
from returns.result import Success

if TYPE_CHECKING:
    from armaden.framework.classes.instance_container import InstanceContainer

from armaden.framework.utils.types import Result


class ServiceProvider(ABC):
    name: str = 'service_provider'

    def __init__(self, container: 'InstanceContainer') -> None:
        self._container = container

    @abstractmethod
    def register(self) -> Result[None]:
        raise NotImplementedError

    def boot(self) -> Result[None]:
        return Success(None)

    async def status(self) -> Result[Mapping[str, Any]]:
        from armaden.framework.enums.health_status import HealthStatus
        return Success({self.name: HealthStatus.OK})
