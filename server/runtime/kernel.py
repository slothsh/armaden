import asyncio
from pathlib import Path
from typing import Any, Dict, List, Self, TypeVar, cast
from framework.classes.service_provider import ServiceProvider
from dotenv import load_dotenv
from enum import StrEnum
import logging
import os
import sys
from glob import glob

from returns.pipeline import is_successful
from returns.result import Failure, Success

from framework.classes.instance_container import InstanceContainer
from framework.protocols import SupervisorInterface
from framework.protocols.application import ApplicationInterface
from framework.enums.health_status import HealthStatus
from framework.utils.dictionary import Dictionary
from framework.utils.types import Result
from framework.errors import Error, GenericError
from .default_application import DefaultApplication
from .module_loader import ModuleLoader
from .supervisor import Supervisor

logger = logging.getLogger('runtime.kernel')


class Kernel:
    _instance: 'Kernel | None' = None

    def __init__(self) -> None:
        self._container = InstanceContainer()
        self._container.instance(InstanceContainer, self._container)

        event_loop = asyncio.new_event_loop()
        self._container.instance('event_loop', event_loop)
        self._container.instance(asyncio.AbstractEventLoop, event_loop)

        self._container.instance('app', self)

        self._container.singleton(SupervisorInterface, Supervisor)

        self._status = KernelStatus.NOT_READY
        self._app_env = 'local'
        self._config: Dict[str, Any] = {}
        self._providers: List[ServiceProvider] = []


    @staticmethod
    def bootstrap() -> Result[None]:
        try:
            # Initialize essentials
            if not is_successful(Kernel._initialize_logging()):
                raise KernelException('Could not successfully initialize logging during application bootstrap')

            # Create the runtime engine
            kernel = Kernel()
            Kernel._instance = kernel
            from framework.facades._registry import set_kernel
            set_kernel(kernel)

            # Load the user application and bind it into the container
            user_app_found = False
            user_app_result = ModuleLoader.try_load_user_application()
            if is_successful(user_app_result) and (cls := user_app_result.unwrap()):
                if issubclass(cls, ApplicationInterface):
                    logger.info("Successfully loaded user application: %s", cls.__name__)
                    kernel._container.bind(ApplicationInterface, cls, shared=True)
                    user_app_found = True
                else:
                    logger.warning("User Application class %s does not implement ApplicationInterface; using DefaultApplication", cls)
                    kernel._container.bind(ApplicationInterface, DefaultApplication, shared=True)
            elif not is_successful(user_app_result):
                logger.warning(user_app_result.failure())
                logger.warning("Using the default application as a fallback")
                kernel._container.bind(ApplicationInterface, DefaultApplication, shared=True)
            else:
                kernel._container.bind(ApplicationInterface, DefaultApplication, shared=True)

            # Initialize everything else
            if not is_successful(kernel._initialize_environment()):
                logger.warning("The application's environment was not successfully initialized, this is not an issue if you did not provide .env file for your application")
            if not is_successful(kernel._initialize_configs()):
                raise KernelException("The application's configuration files could not be successfully initialized")

            kernel._register_providers(with_user_providers=user_app_found)

            # Update application status
            kernel._status = KernelStatus.READY
            logger.info('Application successfully bootstrapped with status: %s', kernel._status)

            return asyncio.run(kernel(), loop_factory=kernel.event_loop)
        except (KeyboardInterrupt, SystemExit):
            return Success(None)
        except Exception as exception:
            return Failure(Error(GenericError.EXCEPTION, details={ 'exception': exception }))
        except:
            return Failure(Error(GenericError.UNKNOWN))


    async def __call__(self) -> Result[None]:
        user_app = self._container.make(ApplicationInterface)

        if not is_successful(result := user_app.boot()):
            logger.error("Could not boot user application: %s", result.failure())
            return result

        if not is_successful(result := self._boot_providers()):
            return result

        supervisor = self._container.make(SupervisorInterface)
        if not is_successful(result := await supervisor.initialize()):
            return result

        if not is_successful(result := await supervisor.run()):
            return result

        return Success(None)


    def version(self) -> str:
        from importlib import metadata
        try:
            return metadata.version('server')
        except metadata.PackageNotFoundError:
            return '0.0.0'


    def config(self, key: str, default: Any | None = None) -> Any:
        value = self._config

        for key in key.split("."):
            value = value[key]

        if value is None:
            return default

        return value


    async def status(self) -> Result[Dict[str, Any]]:
        def handle_result(results: Dict[str, Result[Dict[str, Any]]]) -> Dict[str, Any]:
            status: Dict[str, Any] = {}

            for name, result in results.items():
                if not is_successful(result):
                    logger.warning(result.failure())
                    status[name] = { 'status': HealthStatus.UNAVAILABLE }
                    continue

                status[name] = result.unwrap()

            return status

        provider_statuses = { provider.name: handle_result(result) for provider in self._providers for result in await provider.status() }
        app_degraded = Dictionary.has('status', lambda value: value != HealthStatus.OK, [
            *provider_statuses.values()
        ])

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
    def instance(cls) -> Self:
        if cls._instance is None:
            raise KernelException("No kernel registered. Did you bootstrap the application?")
        return cast(Self, cls._instance)


    @classmethod
    def event_loop(cls) -> asyncio.AbstractEventLoop:
        return cls.instance()._container.make('event_loop')


    @property
    def supervisor(self) -> SupervisorInterface:
        return self._container.make(SupervisorInterface)


    @property
    def container(self) -> InstanceContainer:
        return self._container


    def register_provider(self, provider: ServiceProvider) -> Result[None]:
        result = provider.register()
        if not is_successful(result):
            logger.warning("Provider registration failed for %s: %s", type(provider).__name__, result.failure())
            return result
        self._providers.append(provider)
        logger.info("Registered provider: %s", type(provider).__name__)
        return Success(None)


    # -- Initializers ---------------------------------------------------------

    @classmethod
    def _initialize_logging(cls) -> Result[None]:
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s [%(levelname)s][%(name)s][%(threadName)s]: %(message)s",
            stream=sys.stdout,
        )

        return Success(None)


    def _register_providers(self, with_user_providers: bool = False) -> None:
        """Discover and register user-defined service providers."""
        if not with_user_providers:
            logger.debug("Skipping user provider discovery — no user application loaded")
            return

        try:
            from app.providers import AppServiceProvider
            provider = AppServiceProvider(self._container)
            result = provider.register()
            if not is_successful(result):
                logger.warning("Provider registration failed for %s: %s", AppServiceProvider.__name__, result.failure())
                return
            self._providers.append(provider)
            logger.info("Registered provider: %s", AppServiceProvider.__name__)
        except ModuleNotFoundError:
            logger.debug("No user providers module found at app.providers")
        except Exception as e:
            logger.warning("Error during provider registration: %s", e)


    def _boot_providers(self) -> Result[None]:
        """Boot all registered service providers after the container is fully configured."""
        for provider in self._providers:
            result = provider.boot()
            if not is_successful(result):
                logger.warning("Provider boot failed for %s: %s", type(provider).__name__, result.failure())
                return result
            logger.info("Booted provider: %s", type(provider).__name__)
        return Success(None)


    def _initialize_environment(self) -> Result[None]:
        if app_env := os.getenv('APP_ENV'):
            self._app_env = app_env

        if not self._app_env:
            return Failure(Error(KernelError.INVALID_DEFAULT_ENVIRONMENT))

        logger.info("Loading environment configuration for `%s`", self._app_env)

        # Check env files in order
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

        return Failure(Error(KernelError.MISSING_DOTENV))


    def _initialize_configs(self) -> Result[None]:
        if not __package__:
            return Failure(Error(KernelError.INVALID_PACKAGE_NAME))

        # Load default configuration first
        config_directory = Path(__file__).absolute().parent / 'config'
        config_files = config_directory.glob('*.py')

        for file in [file for file in config_files if file.is_file() and not file.name.startswith(('.', '_'))]:
            if not is_successful(result := ModuleLoader.try_import_module(f"{__package__}.config.{file.stem}")):
                return result.map(lambda _: None)

            config = getattr(result.unwrap(), 'config')
            if callable(config):
                self._config[file.stem] = config()
            else:
                return Failure(Error(KernelError.CONFIG_MODULE_NOT_CALLABLE, details={
                    'directory': config_directory,
                    'file': file,
                }))

        # Load user configuration
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


# -- Internal Types -----------------------------------------------------------

T = TypeVar("T", bound=Kernel)
U = TypeVar("U", bound=Kernel)


class KernelStatus(StrEnum):
    NOT_READY = 'NOT_READY'
    READY = 'READY'


class KernelException(Exception):
    pass


class KernelError(StrEnum):
    MISSING_DOTENV = 'no .env file was found in the working directory of the application'
    INVALID_DEFAULT_ENVIRONMENT = 'the application has no default environment configured'
    INVALID_PACKAGE_NAME = "the application's package name is not defined"
    CONFIG_MODULE_NOT_CALLABLE = "the imported configuration factory method is not callable"
