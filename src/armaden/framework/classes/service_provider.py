from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Mapping
from returns.result import Success

if TYPE_CHECKING:
    from armaden.framework.classes.instance_container import InstanceContainer

from armaden.framework.utils.types import Result


class DeferrableProvider(ABC):
    @abstractmethod
    def provides(self) -> list[Any]:
        raise NotImplementedError


class ServiceProvider(ABC):
    name: str = 'service_provider'

    bindings: dict = {}
    singletons: dict = {}

    def __init__(self, container: 'InstanceContainer') -> None:
        self._container = container

    @property
    def app(self) -> 'InstanceContainer':
        return self._container

    def is_deferred(self) -> bool:
        return isinstance(self, DeferrableProvider)

    def register_bindings(self) -> None:
        for abstract, concrete in self.bindings.items():
            self._container.bind(abstract, concrete)
        for abstract, concrete in self.singletons.items():
            self._container.singleton(abstract, concrete)

    @abstractmethod
    def register(self) -> Result[None]:
        raise NotImplementedError

    def boot(self) -> Result[None]:
        return Success(None)

    async def status(self) -> Result[Mapping[str, Any]]:
        from armaden.framework.enums.health_status import HealthStatus
        return Success({self.name: HealthStatus.OK})
