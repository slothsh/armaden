import asyncio
from pathlib import Path
from typing import Any, Dict, List, Self, Type, TypeVar, cast
from dotenv import load_dotenv
from enum import StrEnum
import logging
import os
import sys
from glob import glob
from importlib import import_module
from abc import ABC

from returns.pipeline import is_successful
from returns.result import Failure, Success

from framework.enums.health_status import HealthStatus
from framework.utils.dictionary import Dictionary

from .module_loader import ModuleLoader
from ..protocols import ServiceInterface, SupervisorInterface
from ..utils.types import Result
from ..errors import Error
from ..classes.supervisor import Supervisor

logger = logging.getLogger('framework.kernel')


# -- Global Handle ------------------------------------------------------------

HANDLE: Kernel | None = None
EVENT_LOOP: asyncio.AbstractEventLoop | None = None


class Kernel(ABC):
    def __init__(self, handle: Kernel | None = None, package_name: str | None = None) -> None:
        global HANDLE, EVENT_LOOP
        HANDLE = handle
        EVENT_LOOP = asyncio.new_event_loop()

        self._status = KernelStatus.NOT_READY
        self._app_env = 'production'
        self._config: Dict[str, Any] = {}
        self._package_name: str | None = package_name or (None if not __package__ else __package__.split(".")[0])

        self.services: List[ServiceInterface] = []
        self.supervisor: SupervisorInterface = Supervisor(EVENT_LOOP)


    @staticmethod
    def bootstrap(default_application: Type[T]) -> Result[T | U]:
        try:
            if not is_successful(Kernel._initialize_logging()):
                raise KernelException('Could not successfully initialize logging during application bootstrap')
        except KernelException as exception:
            raise exception
        except Exception as exception:
            raise KernelException(exception)

        user_application = ModuleLoader.try_load_user_application(cast(Type[U], default_application))
        if not is_successful(user_application):
            logger.warning(user_application.failure())
            logger.warning("Using the default application as a fallback")

        user_application = user_application.value_or(None)
        application = user_application if user_application else default_application

        app = cast(Kernel, application())

        # Set some essential application flags
        if app_env := os.getenv('APP_ENV'):
            app._app_env = app_env

        # Initialize application facilities
        try:
            if not is_successful(app._initialize_logging()):
                raise KernelException('Could not successfully initialize logging during application bootstrap')
            if not is_successful(app._initialize_environment()):
                logger.warning("The application's environment was not successfully initialized, this is not an issue if you did not provide .env file for your application")
            if not is_successful(app._initialize_configs()):
                raise KernelException("The application's configuration files could not be successfully initialized")
        except KernelException as exception:
            raise exception
        except Exception as exception:
            raise KernelException(exception)

        # Update application status
        app._status = KernelStatus.READY
        logger.info('Application successfully bootstrapped with status: %s', app._status)

        return Success(cast(T | U, app))


    def _boot(self) -> Result[None]:
        for service in self.services:
            if not is_successful(result := service()):
                return result

        return Success(None)


    async def __call__(self) -> Result[None]:
        if not is_successful(result := self._boot()):
            logger.error("Could not boot service %s", result.failure())
            return result

        if not is_successful(result := await self.supervisor.initialize()):
            return result

        if not is_successful(result := await self.supervisor.run()):
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


    async def status(self) -> Dict[str, Any]:
        def handle_result(results: Dict[str, Result[Dict[str, Any]]]) -> Dict[str, Any]:
            status: Dict[str, Any] = {}

            for name, result in results.items():
                if not is_successful(result):
                    logger.warning(result.failure())
                    status[name] = { 'status': HealthStatus.UNAVAILABLE }
                    continue

                status[name] = result.unwrap()

            return status

                
        service_statuses = { service.name: handle_result(result) for service in self.services for result in await service.status() }
        app_degraded = Dictionary.has('status', lambda value: value != HealthStatus.OK, [
            *service_statuses.values()
        ])

        return {
            'status': HealthStatus.DEGRADED if app_degraded else HealthStatus.OK,
            'services': service_statuses,
        }


    @classmethod
    def instance(cls) -> Self:
        global HANDLE
        if not HANDLE:
            raise KernelException("The global application handle is not available. Did you bootstrap the application?")
        return cast(Self, HANDLE)


    @classmethod
    def event_loop(cls) -> asyncio.AbstractEventLoop:
        global EVENT_LOOP
        if not EVENT_LOOP:
            raise KernelException("The global application event loop is not available. Did you bootstrap the application?")
        return EVENT_LOOP


    # -- Initializers ---------------------------------------------------------

    @classmethod
    def _initialize_logging(cls) -> Result[None]:
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s [%(levelname)s][%(name)s][%(threadName)s]: %(message)s",
            stream=sys.stdout,
        )

        return Success(None)


    def _initialize_environment(self) -> Result[None]:
        if not self._app_env:
            return Failure(Error(KernelError.INVALID_DEFAULT_ENVIRONMENT))

        # Check env files in order
        env_file_patterns = [
            '.env',
            f".env.{self._app_env}",
            f".env.*.{self._app_env}",
        ]

        for pattern in env_file_patterns:
            paths = glob(pattern)
            if len(paths) != 1:
                continue

            load_dotenv(Path(paths[0]).absolute())
            return Success(None)

        return Failure(Error(KernelError.MISSING_DOTENV))


    def _initialize_configs(self) -> Result[None]:
        if not self._package_name:
            return Failure(Error(KernelError.INVALID_PACKAGE_NAME))

        config_directory = Path(self._package_name) / 'config'
        config_files = config_directory.glob('*.py')

        for file in [file for file in config_files if file.is_file() and not file.name.startswith(('.', '_'))]:
            module = import_module(f"{self._package_name}.config.{file.stem}")
            config = getattr(module, 'config')
            self._config[file.stem] = config()

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
