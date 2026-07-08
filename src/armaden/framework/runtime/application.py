import asyncio
from pathlib import Path
from typing import Any, Dict, List, Optional
from enum import StrEnum
import logging
import os
import sys
from glob import glob

from dotenv import load_dotenv
from returns.pipeline import is_successful
from returns.result import Failure, Success

from armaden.framework.classes.instance_container import InstanceContainer
from armaden.framework.classes.service_provider import ServiceProvider
from armaden.framework.protocols.application import ApplicationInterface
from armaden.framework.protocols.supervisor import SupervisorInterface
from armaden.framework.utils.dictionary import Dictionary
from armaden.framework.utils.types import Result
from armaden.framework.enums.health_status import HealthStatus
from armaden.framework.errors import Error
from armaden.framework.runtime.supervisor import Supervisor
from armaden.framework.runtime.default_application import DefaultApplication
from armaden.framework.runtime.module_loader import ModuleLoader

logger = logging.getLogger('armaden.framework.runtime.application')


class CoreApplication:
    VERSION = '0.0.0'

    def __init__(self) -> None:
        self._container = InstanceContainer()
        self._container.instance(InstanceContainer, self._container)

        event_loop = asyncio.new_event_loop()
        self._container.instance('event_loop', event_loop)
        self._container.instance(asyncio.AbstractEventLoop, event_loop)

        self._container.instance('app', self)

        from armaden.framework.facades._registry import set_application
        set_application(self)

        self._app_env = 'local'
        self._config: Dict[str, Any] = {}
        self._providers: List[ServiceProvider] = []
        self._booted = False
        self._has_been_bootstrapped = False
        self._booting_callbacks: list = []
        self._booted_callbacks: list = []
        self._terminating_callbacks: list = []

        self.register_base_bindings()
        self.register_base_service_providers()
        self.register_core_container_aliases()

    def register_base_bindings(self) -> None:
        self._container.singleton(SupervisorInterface, Supervisor)

    def register_base_service_providers(self) -> None:
        from armaden.framework.runtime.providers.http_service_provider import HttpServiceProvider
        from armaden.framework.runtime.providers.console_service_provider import ConsoleServiceProvider

        self.register(self._make_provider(HttpServiceProvider))
        self.register(self._make_provider(ConsoleServiceProvider))

    def _make_provider(self, provider_class) -> ServiceProvider:
        return self._container.make(provider_class, {'container': self._container})

    def register_core_container_aliases(self) -> None:
        pass

    def bootstrap(self) -> Result[None]:
        self._has_been_bootstrapped = True

        if not is_successful(self._initialize_logging()):
            raise ApplicationException(
                'Could not successfully initialize logging during application bootstrap'
            )

        user_app_found = False
        if os.getenv('APP_DIR'):
            user_app_result = ModuleLoader.try_load_user_application()
            if is_successful(user_app_result) and (cls := user_app_result.unwrap()):
                if issubclass(cls, ApplicationInterface):
                    logger.info("Successfully loaded user application: %s", cls.__name__)
                    self._container.bind(ApplicationInterface, cls, shared=True)
                    user_app_found = True
                else:
                    logger.warning(
                        "User Application class %s does not implement ApplicationInterface; using DefaultApplication",
                        cls,
                    )
                    self._container.bind(ApplicationInterface, DefaultApplication, shared=True)
            elif not is_successful(user_app_result):
                logger.warning(user_app_result.failure())
                logger.warning("Using the default application as a fallback")
                self._container.bind(ApplicationInterface, DefaultApplication, shared=True)
            else:
                self._container.bind(ApplicationInterface, DefaultApplication, shared=True)
        else:
            self._container.bind(ApplicationInterface, DefaultApplication, shared=True)

        if not is_successful(self._initialize_environment()):
            logger.warning("The application's environment was not successfully initialized")
        if not is_successful(self._initialize_configs()):
            raise ApplicationException(
                "The application's configuration files could not be successfully initialized"
            )

        if user_app_found:
            from armaden.framework.runtime.providers.type_discovery_service_provider import (
                TypeDiscoveryServiceProvider,
            )

            discovery_result = self.register(self._make_provider(TypeDiscoveryServiceProvider))
            if not is_successful(discovery_result):
                raise ApplicationException(
                    f"Type discovery failed during application bootstrap: {discovery_result.failure()}"
                )

        self._register_providers(with_user_providers=user_app_found)

        logger.info('Application successfully bootstrapped')
        return Success(None)

    def register(self, provider: ServiceProvider) -> Result[None]:
        if provider.is_deferred():
            return self._register_deferred_provider(provider)
        self._register_provider_bindings(provider)
        result = provider.register()
        if not is_successful(result):
            logger.warning(
                "Provider registration failed for %s: %s",
                type(provider).__name__,
                result.failure(),
            )
            return result
        self._providers.append(provider)
        logger.info("Registered provider: %s", type(provider).__name__)
        return Success(None)

    def _register_deferred_provider(self, provider: ServiceProvider) -> Result[None]:
        provides = provider.provides()  # type: ignore[attr-defined]
        manifest = {abstract: type(provider) for abstract in provides}
        self._container.add_deferred_services(manifest)
        logger.info(
            "Deferred provider %s for bindings: %s",
            type(provider).__name__,
            provides,
        )
        return Success(None)

    def register_provider(self, provider: ServiceProvider) -> Result[None]:
        return self.register(provider)

    def boot(self) -> Result[None]:
        if self._booted:
            return Success(None)

        self._fire_app_callbacks(self._booting_callbacks)

        for provider in self._providers:
            result = self._container.call([provider, 'boot'])
            if not is_successful(result):
                logger.warning(
                    "Provider boot failed for %s: %s",
                    type(provider).__name__,
                    result.failure(),
                )
                return result
            logger.info("Booted provider: %s", type(provider).__name__)

        self._booted = True

        self._fire_app_callbacks(self._booted_callbacks)

        return Success(None)

    def booting(self, callback: callable) -> None:
        self._booting_callbacks.append(callback)

    def booted(self, callback: callable) -> None:
        self._booted_callbacks.append(callback)
        if self._booted:
            callback(self)

    def terminating(self, callback: callable) -> None:
        self._terminating_callbacks.append(callback)

    def terminate(self) -> Result[None]:
        for callback in self._terminating_callbacks:
            callback(self)
        return Success(None)

    @property
    def container(self) -> InstanceContainer:
        return self._container

    def make(self, abstract: Any, parameters: Optional[Dict[str, Any]] = None) -> Any:
        return self._container.make(abstract, parameters)

    def singleton(self, abstract: Any, concrete: Any = None) -> None:
        self._container.singleton(abstract, concrete)

    def bind(self, abstract: Any, concrete: Any = None, shared: bool = False) -> None:
        self._container.bind(abstract, concrete, shared)

    def instance(self, abstract: Any, instance: Any) -> Any:
        return self._container.instance(abstract, instance)

    @property
    def supervisor(self) -> SupervisorInterface:
        return self._container.make(SupervisorInterface)

    @property
    def event_loop(self) -> asyncio.AbstractEventLoop:
        return self._container.make('event_loop')

    def version(self) -> str:
        from importlib import metadata
        try:
            return metadata.version('armaden')
        except metadata.PackageNotFoundError:
            return '0.0.0'

    def config(self, key: str, default: Any | None = None) -> Any:
        value = self._config
        try:
            for k in key.split("."):
                value = value[k]
        except (KeyError, TypeError):
            return default
        if value is None:
            return default
        return value

    def environment(self) -> str:
        return self._app_env

    def is_local(self) -> bool:
        return self._app_env == 'local'

    def is_production(self) -> bool:
        return self._app_env == 'production'

    async def status(self) -> Result[Dict[str, Any]]:
        def handle_result(results: Dict[str, Result[Dict[str, Any]]]) -> Dict[str, Any]:
            status: Dict[str, Any] = {}
            for name, result in results.items():
                if not is_successful(result):
                    logger.warning(result.failure())
                    status[name] = {'status': HealthStatus.UNAVAILABLE}
                    continue
                status[name] = result.unwrap()
            return status

        async def wrap_provider_status(provider: ServiceProvider) -> Dict[str, Any]:
            return handle_result(await provider.status())

        provider_statuses = {
            provider.name: await wrap_provider_status(provider)
            for provider in self._providers
        }
        app_degraded = Dictionary.has(
            'status',
            lambda value: value != HealthStatus.OK,
            [*provider_statuses.values()],
        )

        user_app = self._container.make(ApplicationInterface)
        user_status_result = await user_app.status()
        if is_successful(user_status_result):
            user_status = user_status_result.unwrap()
        else:
            user_status = {}
            logger.warning(user_status_result.failure())

        return Success({
            'status': HealthStatus.DEGRADED if app_degraded else HealthStatus.OK,
            'providers': provider_statuses,
            **user_status,
        })

    @classmethod
    def _initialize_logging(cls) -> Result[None]:
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s [%(levelname)s][%(name)s][%(threadName)s]: %(message)s",
            stream=sys.stdout,
        )
        return Success(None)

    def _register_providers(self, with_user_providers: bool = False) -> None:
        if not with_user_providers:
            logger.debug("Skipping user provider discovery")
            return

        result = ModuleLoader.try_load_user_app_provider()
        if not is_successful(result):
            logger.warning("Failed to load user providers: %s", result.failure())
            return

        provider_list = result.unwrap()
        if not provider_list:
            logger.debug("No user providers module found in APP_DIR")
            return

        for provider_class in provider_list:
            try:
                provider = self._make_provider(provider_class)
                if provider.is_deferred():
                    self._register_deferred_provider(provider)
                    continue
                self._register_provider_bindings(provider)
                result = provider.register()
                if not is_successful(result):
                    logger.warning(
                        "Provider registration failed for %s: %s",
                        provider_class.__name__,
                        result.failure(),
                    )
                    continue
                self._providers.append(provider)
                logger.info("Registered provider: %s", provider_class.__name__)
            except Exception as e:
                logger.warning("Error during provider registration: %s", e)

    def _initialize_environment(self) -> Result[None]:
        if app_env := os.getenv('APP_ENV'):
            self._app_env = app_env

        if not self._app_env:
            return Failure(
                Error(ApplicationError.INVALID_DEFAULT_ENVIRONMENT)
            )

        logger.info("Loading environment configuration for `%s`", self._app_env)

        env_file_patterns = [
            f".env.{self._app_env}",
            f".env.*.{self._app_env}",
        ]

        found_explicit = False
        for pattern in env_file_patterns:
            paths = glob(pattern)
            if len(paths) > 0:
                found_explicit = True
            for path in paths:
                logger.info("Overlaying environment file: %s", path)
                load_dotenv(Path(path).absolute())

        if found_explicit:
            return Success(None)

        default_env = Path('.env').absolute()
        if default_env.is_file():
            logger.info("Loading environment file: %s", default_env)
            load_dotenv(default_env)
            return Success(None)

        return Failure(Error(ApplicationError.MISSING_DOTENV))

    def _initialize_configs(self) -> Result[None]:
        if not __package__:
            return Failure(Error(ApplicationError.INVALID_PACKAGE_NAME))

        config_directory = Path(__file__).absolute().parent / 'config'
        config_files = config_directory.glob('*.py')

        for file in [
            file for file in config_files
            if file.is_file() and not file.name.startswith(('.', '_'))
        ]:
            if not is_successful(
                result := ModuleLoader.try_import_module(
                    f"{__package__}.config.{file.stem}"
                )
            ):
                return result.map(lambda _: None)

            config = getattr(result.unwrap(), 'config')
            if callable(config):
                self._config[file.stem] = config()
            else:
                return Failure(
                    Error(
                        ApplicationError.CONFIG_MODULE_NOT_CALLABLE,
                        details={'directory': config_directory, 'file': file},
                    )
                )

        if not is_successful(result := ModuleLoader.try_load_user_config()):
            return result.map(lambda _: None)

        if not (result := result.unwrap()):
            return Success(None)

        for (key, config) in result:
            if key in self._config:
                self._config[key].update(config())
                continue
            self._config[key] = config()

        return Success(None)

    def _register_provider_bindings(self, provider: ServiceProvider) -> None:
        provider.register_bindings()

    def _fire_app_callbacks(self, callbacks: list) -> None:
        index = 0
        while index < len(callbacks):
            callbacks[index](self)
            index += 1


class ApplicationStatus(StrEnum):
    NOT_READY = 'NOT_READY'
    READY = 'READY'


class ApplicationException(Exception):
    pass


class ApplicationError(StrEnum):
    MISSING_DOTENV = 'no .env file was found in the working directory of the application'
    INVALID_DEFAULT_ENVIRONMENT = 'the application has no default environment configured'
    INVALID_PACKAGE_NAME = "the application's package name is not defined"
    CONFIG_MODULE_NOT_CALLABLE = "the imported configuration factory method is not callable"
