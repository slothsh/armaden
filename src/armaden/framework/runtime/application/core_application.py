from __future__ import annotations

import asyncio
from collections.abc import Callable
from typing import cast, override

from returns.pipeline import is_successful
from returns.result import Success

from armaden.framework.facades.facade import Facade
from armaden.framework.protocols.container_protocol import ContainerProtocol
from armaden.framework.protocols.core_application_protocol import (
    CoreApplicationProtocol,
)
from armaden.framework.protocols.deferrable_provider_protocol import (
    DeferrableProviderProtocol,
)
from armaden.framework.protocols.service_provider_protocol import ServiceProviderProtocol
from armaden.framework.protocols.supervisor_protocol import SupervisorProtocol
from armaden.framework.runtime.container.container import Container
from armaden.framework.runtime.supervisor.task.dto.task_graph_data import TaskGraphData
from armaden.framework.runtime.supervisor.supervisor import Supervisor
from armaden.framework.types.result import Result


class CoreApplication(CoreApplicationProtocol[TaskGraphData]):
    def __init__(
        self,
        container: ContainerProtocol | None = None,
        event_loop: asyncio.AbstractEventLoop | None = None,
    ) -> None:
        self._booted: bool = False
        self._booted_callbacks: list[Callable[..., object]] = []
        self._booting_callbacks: list[Callable[..., object]] = []
        self._container: ContainerProtocol = (
            container if container is not None else Container()
        )
        self._event_loop: asyncio.AbstractEventLoop = (
            event_loop if event_loop is not None else asyncio.new_event_loop()
        )
        self._providers: list[ServiceProviderProtocol] = []
        self._terminating_callbacks: list[Callable[..., object]] = []
        self._register_base_bindings()
        Facade.set_facade_application(self._container)


    def _create_supervisor(
        self,
        container: ContainerProtocol,
        parameters: dict[object, object],
    ) -> Supervisor:
        _ = container
        _ = parameters
        return Supervisor(self._event_loop, cast(Container, self._container))


    def _fire_callbacks(self, callbacks: list[Callable[..., object]]) -> None:
        for callback in callbacks:
            _ = callback(self)


    def _register_deferred_provider(self, provider: ServiceProviderProtocol) -> None:
        deferred_provider = cast(
            DeferrableProviderProtocol,
            cast(object, provider),
        )
        services = {
            abstract: type(provider)
            for abstract in deferred_provider.provides()
        }
        self._container.add_deferred_services(services)


    def _register_base_bindings(self) -> None:
        _ = self._container.instance(Container, self._container)
        _ = self._container.instance(ContainerProtocol, self._container)
        _ = self._container.instance(CoreApplicationProtocol, self)
        _ = self._container.instance(asyncio.AbstractEventLoop, self._event_loop)
        _ = self._container.instance('app', self)
        _ = self._container.instance('event_loop', self._event_loop)
        self._container.singleton(SupervisorProtocol, self._create_supervisor)


    @override
    def bind(
        self,
        abstract: object,
        concrete: object | None = None,
        shared: bool = False,
    ) -> None:
        self._container.bind(abstract, concrete, shared)


    @override
    def boot(self) -> Result[None]:
        if self._booted:
            return Success(None)

        self._fire_callbacks(self._booting_callbacks)
        for provider in self._providers:
            result = provider.boot()
            if not is_successful(result):
                return result
        self._booted = True
        self._fire_callbacks(self._booted_callbacks)
        return Success(None)


    @override
    def booted(self, callback: Callable[..., object]) -> None:
        self._booted_callbacks.append(callback)
        if self._booted:
            _ = callback(self)


    @override
    def booting(self, callback: Callable[..., object]) -> None:
        self._booting_callbacks.append(callback)


    @property
    @override
    def container(self) -> ContainerProtocol:
        return self._container


    @property
    @override
    def event_loop(self) -> asyncio.AbstractEventLoop:
        return self._event_loop


    @override
    def instance(self, abstract: object, instance: object) -> object:
        return self._container.instance(abstract, instance)


    @override
    def make(
        self,
        abstract: object,
        parameters: dict[object, object] | None = None,
    ) -> object:
        return self._container.make(abstract, parameters)


    @override
    def register(self, provider: ServiceProviderProtocol) -> Result[None]:
        if provider.is_deferred():
            self._register_deferred_provider(provider)
            return Success(None)

        provider.register_bindings()
        result = provider.register()
        if is_successful(result):
            self._providers.append(provider)
        return result


    @override
    def singleton(self, abstract: object, concrete: object | None = None) -> None:
        self._container.singleton(abstract, concrete)


    @property
    @override
    def supervisor(self) -> SupervisorProtocol[TaskGraphData]:
        return cast(
            SupervisorProtocol[TaskGraphData],
            self._container.make(SupervisorProtocol),
        )


    @override
    def terminate(self) -> Result[None]:
        self._fire_callbacks(self._terminating_callbacks)
        return Success(None)


    @override
    def terminating(self, callback: Callable[..., object]) -> None:
        self._terminating_callbacks.append(callback)