from abc import ABC, abstractmethod
from collections.abc import Mapping
from typing import override

from returns.result import Success

from armaden.framework.enums.health_status import HealthStatus
from armaden.framework.protocols.container_protocol import ContainerProtocol
from armaden.framework.protocols.service_provider_protocol import ServiceProviderProtocol
from armaden.framework.runtime.service_provider.deferrable_provider import (
    DeferrableProvider,
)
from armaden.framework.types.result import Result


class ServiceProvider(ServiceProviderProtocol, ABC):
    bindings: dict[object, object] = {}
    name: str = 'service_provider'
    singletons: dict[object, object] = {}

    def __init__(self, container: ContainerProtocol) -> None:
        self._container: ContainerProtocol = container


    @property
    @override
    def app(self) -> ContainerProtocol:
        return self._container


    @override
    def boot(self) -> Result[None]:
        return Success(None)


    @override
    def is_deferred(self) -> bool:
        return isinstance(self, DeferrableProvider)


    @override
    @abstractmethod
    def register(self) -> Result[None]:
        raise NotImplementedError


    @override
    def register_bindings(self) -> None:
        for abstract, concrete in self.bindings.items():
            _ = self._container.bind(abstract, concrete)
        for abstract, concrete in self.singletons.items():
            _ = self._container.singleton(abstract, concrete)


    @override
    async def status(self) -> Result[Mapping[str, object]]:
        return Success({self.name: HealthStatus.OK})