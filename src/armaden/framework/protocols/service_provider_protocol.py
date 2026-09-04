from collections.abc import Mapping
from typing import Protocol

from armaden.framework.protocols.container_protocol import ContainerProtocol
from armaden.framework.types.result import Result


class ServiceProviderProtocol(Protocol):
    bindings: dict[object, object]
    name: str
    singletons: dict[object, object]

    @property
    def app(self) -> ContainerProtocol: ...

    def boot(self) -> Result[None]: ...

    def is_deferred(self) -> bool: ...

    def register(self) -> Result[None]: ...

    def register_bindings(self) -> None: ...

    async def status(self) -> Result[Mapping[str, object]]: ...