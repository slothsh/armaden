from __future__ import annotations

import asyncio
from collections.abc import Callable, Mapping
from typing import cast, overload, override

from armaden.framework.api.supervisor import TaskGraphData
from armaden.framework.facades.facade import Facade
from armaden.framework.protocols.application_protocol import ApplicationProtocol
from armaden.framework.protocols.configuration_protocol import ConfigurationProtocol
from armaden.framework.protocols.contextual_binding_builder_protocol import (
    ContextualBindingBuilderProtocol,
)
from armaden.framework.protocols.container_protocol import ContainerProtocol
from armaden.framework.protocols.core_application_protocol import CoreApplicationProtocol
from armaden.framework.protocols.environment_protocol import EnvironmentProtocol
from armaden.framework.protocols.service_provider_protocol import ServiceProviderProtocol
from armaden.framework.protocols.supervisor_protocol import SupervisorProtocol
from armaden.framework.types.result import Result


class AppFacade(Facade):
    @classmethod
    def alias(cls, abstract: object, alias: object) -> None:
        cls.container().alias(abstract, alias)


    @classmethod
    def application(cls) -> CoreApplicationProtocol[TaskGraphData]:
        return cast(
            CoreApplicationProtocol[TaskGraphData],
            cls.get_facade_root(),
        )


    @classmethod
    def bind(
        cls,
        abstract: object,
        concrete: object | None = None,
        shared: bool = False,
    ) -> None:
        cls.container().bind(abstract, concrete, shared)


    @classmethod
    def bind_if(
        cls,
        abstract: object,
        concrete: object | None = None,
        shared: bool = False,
    ) -> None:
        cls.container().bind_if(abstract, concrete, shared)


    @classmethod
    def boot(cls) -> Result[None]:
        return cls.application().boot()


    @classmethod
    def bootstrap(cls) -> Result[None]:
        return cls.application().bootstrap()


    @classmethod
    def bound(cls, abstract: object) -> bool:
        return cls.container().bound(abstract)


    @classmethod
    def call(
        cls,
        callback: Callable[..., object],
        parameters: dict[object, object] | None = None,
        default_method: str | None = None,
    ) -> object:
        return cls.container().call(callback, parameters, default_method)


    @classmethod
    def config(
        cls,
        key: str,
        default: object | None = None,
    ) -> object | None:
        return cls.application().config(key, default)


    @classmethod
    def configuration(cls) -> ConfigurationProtocol:
        return cls.application().configuration


    @classmethod
    def container(cls) -> ContainerProtocol:
        return cls.application().container


    @classmethod
    def environment(cls) -> EnvironmentProtocol:
        return cls.application().environment


    @classmethod
    def event_loop(cls) -> asyncio.AbstractEventLoop:
        return cls.application().event_loop


    @classmethod
    def extend(cls, abstract: object, closure: Callable[..., object]) -> None:
        cls.container().extend(abstract, closure)


    @classmethod
    def factory(cls, abstract: object) -> Callable[..., object]:
        return cls.container().factory(abstract)


    @classmethod
    def flush(cls) -> None:
        cls.container().flush()


    @classmethod
    def forget_instance(cls, abstract: object) -> None:
        cls.container().forget_instance(abstract)


    @classmethod
    def forget_instances(cls) -> None:
        cls.container().forget_instances()


    @classmethod
    def forget_scoped_instances(cls) -> None:
        cls.container().forget_scoped_instances()


    @classmethod
    def get(cls, id: str) -> object:
        return cls.container().get(id)


    @override
    @classmethod
    def get_facade_accessor(cls) -> object:
        return CoreApplicationProtocol


    @classmethod
    def has(cls, id: str) -> bool:
        return cls.container().has(id)


    @classmethod
    def instance[T](cls, abstract: object, instance: T) -> T:
        return cast(T, cls.container().instance(abstract, instance))


    @classmethod
    def is_alias(cls, name: object) -> bool:
        return cls.container().is_alias(name)


    @classmethod
    def is_local(cls) -> bool:
        return cls.application().is_local()


    @classmethod
    def is_production(cls) -> bool:
        return cls.application().is_production()


    @classmethod
    def is_shared(cls, abstract: object) -> bool:
        return cls.container().is_shared(abstract)


    @overload
    @classmethod
    def make[T](
        cls,
        abstract: type[T],
        parameters: dict[object, object] | None = None,
    ) -> T: ...

    @overload
    @classmethod
    def make(
        cls,
        abstract: object,
        parameters: dict[object, object] | None = None,
    ) -> object: ...

    @classmethod
    def make(
        cls,
        abstract: object,
        parameters: dict[object, object] | None = None,
    ) -> object:
        return cls.container().make(abstract, parameters)


    @overload
    @classmethod
    def make_with[T](
        cls,
        abstract: type[T],
        parameters: dict[object, object] | None = None,
    ) -> T: ...

    @overload
    @classmethod
    def make_with(
        cls,
        abstract: object,
        parameters: dict[object, object] | None = None,
    ) -> object: ...

    @classmethod
    def make_with(
        cls,
        abstract: object,
        parameters: dict[object, object] | None = None,
    ) -> object:
        return cls.container().make_with(abstract, parameters)


    @classmethod
    def rebinding(
        cls,
        abstract: object,
        callback: Callable[..., object],
    ) -> object | None:
        return cls.container().rebinding(abstract, callback)


    @classmethod
    def register(cls, provider: ServiceProviderProtocol) -> Result[None]:
        return cls.application().register(provider)


    @classmethod
    def resolved(cls, abstract: object) -> bool:
        return cls.container().resolved(abstract)


    @classmethod
    def scoped(
        cls,
        abstract: object,
        concrete: object | None = None,
    ) -> None:
        cls.container().scoped(abstract, concrete)


    @classmethod
    def scoped_if(
        cls,
        abstract: object,
        concrete: object | None = None,
    ) -> None:
        cls.container().scoped_if(abstract, concrete)


    @classmethod
    def singleton(cls, abstract: object, concrete: object | None = None) -> None:
        cls.container().singleton(abstract, concrete)


    @classmethod
    def singleton_if(
        cls,
        abstract: object,
        concrete: object | None = None,
    ) -> None:
        cls.container().singleton_if(abstract, concrete)


    @classmethod
    async def status(cls) -> Result[Mapping[str, object]]:
        application = cast(
            ApplicationProtocol[TaskGraphData],
            cls.application().make(ApplicationProtocol),
        )
        return await application.status()


    @classmethod
    def supervisor(cls) -> SupervisorProtocol[TaskGraphData]:
        return cls.application().supervisor


    @classmethod
    def tag(cls, abstracts: object, *tags: object) -> None:
        cls.container().tag(abstracts, *tags)


    @classmethod
    def tagged(cls, tag: str) -> list[object]:
        return cls.container().tagged(tag)


    @classmethod
    def terminate(cls) -> Result[None]:
        return cls.application().terminate()


    @classmethod
    def version(cls) -> str:
        return cls.application().version()


    @classmethod
    def when(cls, concrete: object) -> ContextualBindingBuilderProtocol:
        return cls.container().when(concrete)


    @classmethod
    def wrap(
        cls,
        callback: Callable[..., object],
        parameters: dict[object, object] | None = None,
    ) -> Callable[..., object]:
        return cls.container().wrap(callback, parameters)
