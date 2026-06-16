import asyncio
from pathlib import Path
from typing import Any, Dict, List, Self, cast
from dotenv import load_dotenv
from enum import StrEnum
import logging
import os
import sys
from glob import glob
from importlib import metadata, import_module
from abc import ABC

from returns.pipeline import is_successful
from returns.result import Failure, Success

from .protocols import ServiceInterface, ApplicationInterface, SupervisorInterface
from .utils.types import Result
from .errors import Error
from .classes.supervisor import Supervisor

logger = logging.getLogger('framework.kernel')


# -- Global Handle ------------------------------------------------------------

HANDLE: ApplicationInterface | None = None


class Kernel(ABC):
    def __init__(self, handle: ApplicationInterface | None = None, package_name: str | None = None) -> None:
        global HANDLE
        HANDLE = handle

        self._status = KernelStatus.NOT_READY
        self._app_env = 'production'
        self._config: Dict[str, Any] = {}
        self._package_name: str | None = package_name or (None if not __package__ else __package__.split(".")[0])

        self.services: List[ServiceInterface] = []
        self.supervisor: SupervisorInterface = Supervisor(asyncio.new_event_loop())

        self._bootstrap()


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
        if not self._package_name:
            return '0.0.0'
        return metadata.version(self._package_name)


    def environment(self, name: str, default: str | None = None) -> str | None:
        if result := os.getenv(name):
            return result
        return default


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
                    status[name] = None
                    continue

                status[name] = result.unwrap()

            return status

                
        return { service.name: handle_result(result) for service in self.services for result in await service.status()}


    @classmethod
    def instance(cls) -> Self:
        global HANDLE
        if not HANDLE:
            raise KernelException("The global application handle is not available. Did you bootstrap the application?")
        return cast(Self, HANDLE)


    # -- Initializers ---------------------------------------------------------

    def _bootstrap(self) -> None:
        # Set some essential application flags
        if app_env := os.getenv('APP_ENV'):
            self._app_env = app_env

        # Initialize application facilities
        try:
            if not is_successful(self._initialize_logging()):
                raise KernelException('Could not successfully initialize logging during application bootstrap')
            if not is_successful(self._initialize_environment()):
                logger.warning("The application's environment was not successfully initialized, this is not an issue if you did not provide .env file for your application")
            if not is_successful(self._initialize_configs()):
                raise KernelException("The application's configuration files could not be successfully initialized")
        except KernelException as exception:
            raise exception
        except Exception as exception:
            raise KernelException(exception)

        # Update application status
        self._status = KernelStatus.READY
        logger.info('Application successfully bootstrapped with status: %s', self._status)


    def _boot(self) -> Result[None]:
        for service in self.services:
            if not is_successful(result := service()):
                return result

        return Success(None)


    def _initialize_logging(self) -> Result[None]:
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

class KernelStatus(StrEnum):
    NOT_READY = 'NOT_READY'
    READY = 'READY'


class KernelException(Exception):
    pass


class KernelError(StrEnum):
    MISSING_DOTENV = 'no .env file was found in the working directory of the application'
    INVALID_DEFAULT_ENVIRONMENT = 'the application has no default environment configured'
    INVALID_PACKAGE_NAME = "the application's package name is not defined"
