from __future__ import annotations

import asyncio
from collections.abc import Callable
from typing import Protocol

from armaden.framework.protocols.configuration_protocol import ConfigurationProtocol
from armaden.framework.protocols.container_protocol import ContainerProtocol
from armaden.framework.protocols.environment_protocol import EnvironmentProtocol
from armaden.framework.protocols.service_provider_protocol import ServiceProviderProtocol
from armaden.framework.protocols.supervisor_protocol import SupervisorProtocol
from armaden.framework.types.result import Result


class CoreApplicationProtocol[G](Protocol):
    def bind(
        self,
        abstract: object,
        concrete: object | None = None,
        shared: bool = False,
    ) -> None: ...

    def boot(self) -> Result[None]: ...

    def booted(self, callback: Callable[..., object]) -> None: ...

    def booting(self, callback: Callable[..., object]) -> None: ...

    def bootstrap(self) -> Result[None]: ...

    def config(self, key: str, default: object | None = None) -> object | None: ...

    @property
    def configuration(self) -> ConfigurationProtocol: ...

    @property
    def container(self) -> ContainerProtocol: ...

    @property
    def environment(self) -> EnvironmentProtocol: ...

    @property
    def event_loop(self) -> asyncio.AbstractEventLoop: ...

    def instance(self, abstract: object, instance: object) -> object: ...

    def is_local(self) -> bool: ...

    def is_production(self) -> bool: ...

    def make(
        self,
        abstract: object,
        parameters: dict[object, object] | None = None,
    ) -> object: ...

    def register(self, provider: ServiceProviderProtocol) -> Result[None]: ...

    def singleton(self, abstract: object, concrete: object | None = None) -> None: ...

    @property
    def supervisor(self) -> SupervisorProtocol[G]: ...

    def terminate(self) -> Result[None]: ...

    def terminating(self, callback: Callable[..., object]) -> None: ...

    def version(self) -> str: ...
