from __future__ import annotations

import asyncio
import logging
import sys
from collections.abc import Callable
from importlib import metadata
from typing import cast, override

from returns.pipeline import is_successful
from returns.result import Failure, Success

from armaden.framework.facades.facade import Facade
from armaden.framework.protocols.application_protocol import ApplicationProtocol
from armaden.framework.protocols.configuration_protocol import ConfigurationProtocol
from armaden.framework.protocols.container_protocol import ContainerProtocol
from armaden.framework.protocols.core_application_protocol import (
    CoreApplicationProtocol,
)
from armaden.framework.protocols.deferrable_service_provider_protocol import (
    DeferrableServiceProviderProtocol,
)
from armaden.framework.protocols.environment_protocol import EnvironmentProtocol
from armaden.framework.protocols.service_provider_protocol import ServiceProviderProtocol
from armaden.framework.protocols.supervisor_protocol import SupervisorProtocol
from armaden.framework.runtime.application.configuration import Configuration
from armaden.framework.runtime.application.default_application import DefaultApplication
from armaden.framework.runtime.application.environment import Environment
from armaden.framework.runtime.application.module_loader import ModuleLoader
from armaden.framework.runtime.container.container import Container
from armaden.framework.runtime.supervisor.task.dto.task_graph_data import TaskGraphData
from armaden.framework.runtime.supervisor.supervisor import Supervisor
from armaden.framework.types.result import Result

logger = logging.getLogger(__name__)


class CoreApplication(CoreApplicationProtocol[TaskGraphData]):
    def __init__(
        self,
        container: ContainerProtocol | None = None,
        event_loop: asyncio.AbstractEventLoop | None = None,
    ) -> None:
        self._booted: bool = False
        self._booted_callbacks: list[Callable[..., object]] = []
        self._booting_callbacks: list[Callable[..., object]] = []
        self._application_type: type[object] | None = None
        self._configuration: Configuration = Configuration()
        self._container: ContainerProtocol = (
            container if container is not None else Container()
        )
        self._environment: Environment = Environment()
        self._event_loop: asyncio.AbstractEventLoop = (
            event_loop if event_loop is not None else asyncio.new_event_loop()
        )
        self._providers: list[ServiceProviderProtocol] = []
        self._terminating_callbacks: list[Callable[..., object]] = []
        self._bootstrapped: bool = False
        self._register_base_bindings()
        self._register_framework_providers()
        Facade.set_facade_application(self._container)


    def _create_application(
        self,
        container: ContainerProtocol,
        parameters: dict[object, object],
    ) -> ApplicationProtocol[TaskGraphData]:
        _ = container
        _ = parameters
        application_type = self._application_type
        if application_type is None:
            return DefaultApplication(self._container)
        application_factory = cast(
            Callable[[ContainerProtocol], ApplicationProtocol[TaskGraphData]],
            application_type,
        )
        return application_factory(self._container)


    def _create_default_application(
        self,
        container: ContainerProtocol,
        parameters: dict[object, object],
    ) -> DefaultApplication:
        _ = container
        _ = parameters
        return DefaultApplication(self._container)


    def _create_provider(
        self,
        provider_type: type[ServiceProviderProtocol],
    ) -> ServiceProviderProtocol:
        provider_factory = cast(
            Callable[[ContainerProtocol], ServiceProviderProtocol],
            provider_type,
        )
        return provider_factory(self._container)


    def _create_supervisor(
        self,
        container: ContainerProtocol,
        parameters: dict[object, object],
    ) -> Supervisor:
        _ = container
        _ = parameters
        return Supervisor(self._event_loop, cast(Container, self._container))


    def _fire_callbacks(self, callbacks: list[Callable[..., object]]) -> None:
        index = 0
        while index < len(callbacks):
            _ = callbacks[index](self)
            index += 1


    def _initialize_logging(self) -> None:
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s [%(levelname)s][%(name)s][%(threadName)s]: %(message)s',
            stream=sys.stdout,
        )


    def _register_deferred_provider(self, provider: ServiceProviderProtocol) -> None:
        deferred_provider = cast(
            DeferrableServiceProviderProtocol,
            cast(object, provider),
        )
        services = {
            abstract: type(provider)
            for abstract in deferred_provider.provides()
        }
        self._container.add_deferred_services(services)


    def _register_framework_providers(self) -> None:
        from armaden.framework.runtime.service_provider.filesystem_service_provider import FilesystemServiceProvider
        from armaden.framework.runtime.service_provider.http_service_provider import HttpServiceProvider

        filesystem_result = self.register(FilesystemServiceProvider(self._container))
        if isinstance(filesystem_result, Failure):
            logger.warning('Framework filesystem provider registration failed: %s', filesystem_result.failure())

        http_result = self.register(HttpServiceProvider(self._container))
        if isinstance(http_result, Failure):
            logger.warning('Framework HTTP provider registration failed: %s', http_result.failure())


    def _register_user_application(self) -> None:
        result = ModuleLoader.try_load_user_application()
        if isinstance(result, Failure):
            logger.warning('User application discovery failed: %s', result.failure())
            return
        application_type = result.unwrap()
        if application_type is None:
            return
        self._application_type = application_type
        self._container.singleton(ApplicationProtocol, self._create_application)


    def _register_user_providers(self) -> None:
        result = ModuleLoader.try_load_user_app_provider()
        if isinstance(result, Failure):
            logger.warning('User provider discovery failed: %s', result.failure())
            return
        provider_types = result.unwrap()
        if provider_types is None:
            return
        for provider_type in provider_types:
            try:
                result = self.register(self._create_provider(provider_type))
                if isinstance(result, Failure):
                    logger.warning(
                        'Provider registration failed for %s: %s',
                        provider_type,
                        result.failure(),
                    )
            except Exception as exception:
                logger.warning('Provider registration failed for %s: %s', provider_type, exception)


    def _register_base_bindings(self) -> None:
        _ = self._container.instance(ConfigurationProtocol, self._configuration)
        _ = self._container.instance(Container, self._container)
        _ = self._container.instance(ContainerProtocol, self._container)
        _ = self._container.instance(CoreApplicationProtocol, self)
        _ = self._container.instance(EnvironmentProtocol, self._environment)
        _ = self._container.instance(asyncio.AbstractEventLoop, self._event_loop)
        _ = self._container.instance('app', self)
        _ = self._container.instance('event_loop', self._event_loop)
        self._container.singleton(ApplicationProtocol, self._create_default_application)
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


    @override
    def bootstrap(self) -> Result[None]:
        if self._bootstrapped:
            return Success(None)
        self._initialize_logging()
        environment_result = self._environment.initialize()
        if isinstance(environment_result, Failure):
            logger.warning('Environment initialization failed: %s', environment_result.failure())
        configuration_result = self._configuration.load()
        if isinstance(configuration_result, Failure):
            return configuration_result
        self._register_user_application()
        self._register_user_providers()
        self._bootstrapped = True
        logger.info('Application successfully bootstrapped')
        return Success(None)


    @override
    def config(self, key: str, default: object | None = None) -> object | None:
        return self._configuration.get(key, default)


    @property
    @override
    def configuration(self) -> ConfigurationProtocol:
        return self._configuration


    @property
    @override
    def container(self) -> ContainerProtocol:
        return self._container


    @property
    @override
    def environment(self) -> EnvironmentProtocol:
        return self._environment


    @property
    @override
    def event_loop(self) -> asyncio.AbstractEventLoop:
        return self._event_loop


    @override
    def instance(self, abstract: object, instance: object) -> object:
        return self._container.instance(abstract, instance)


    @override
    def is_local(self) -> bool:
        return self._environment.environment == 'local'


    @override
    def is_production(self) -> bool:
        return self._environment.environment == 'production'


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


    @override
    def version(self) -> str:
        try:
            return metadata.version('armaden')
        except metadata.PackageNotFoundError:
            return '0.0.0'
