from pathlib import Path
from typing import Any, Dict, Protocol
from dotenv import load_dotenv
from enum import StrEnum
from threading import Lock
import logging
import os
import sys
from glob import glob
from importlib import metadata, import_module

from returns.pipeline import is_successful
from returns.result import Failure, Success

from server.lib.types import Error, Result

logger = logging.getLogger('server.kernel')


# -- Global Handle ------------------------------------------------------------

HANDLE: ApplicationInterface | None = None


class Kernel:
    def __init__(self, handle: ApplicationInterface | None = None) -> None:
        global HANDLE
        HANDLE = handle

        self._lock = Lock()
        self._status = KernelStatus.NOT_READY
        self._app_env = 'production'
        self._config: Dict[str, Any] = {}
        self._package_name: str | None = None if not __package__ else __package__.split(".")[0]

        self.bootstrap()


    def version(self) -> str:
        if not self._package_name:
            return '0.0.0'
        return metadata.version(self._package_name)
    

    def bootstrap(self) -> None:
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


    def environment(self, name: str, default: str | None = None) -> str | None:
        if result := os.getenv(name):
            return result
        return default


    def config(self) -> Dict[str, Any]:
        return self._config


    @classmethod
    def instance(cls) -> ApplicationInterface:
        global HANDLE
        if not HANDLE:
            raise KernelException("The global application handle is not available. Did you bootstrap the application?")
        return HANDLE


    # -- Initializers ---------------------------------------------------------

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
        logger.info('One')
        if not self._package_name:
            return Failure(Error(KernelError.INVALID_PACKAGE_NAME))

        logger.info('Two')
        config_directory = Path(self._package_name) / 'config'
        config_files = config_directory.glob('*.py')

        logger.info('Three')
        for file in [file for file in config_files if file.is_file() and not file.name.startswith(('.', '_'))]:
            module = import_module(f"{self._package_name}.config.{file.stem}")
            config = getattr(module, 'config')
            self._config[file.stem] = config()

        return Success(None)


# -- Internal Types -----------------------------------------------------------

class KernelInterface(Protocol):
    def version(self) -> str: ...
    def bootstrap(self) -> None: ...
    def environment(self, name: str, default: str | None = None) -> str | None: ...
    def config(self) -> Dict[str, Any]: ...

    @classmethod
    def instance(cls) -> ApplicationInterface: ...


class ApplicationInterface(KernelInterface, Protocol):
    pass


class KernelStatus(StrEnum):
    NOT_READY = 'NOT_READY'
    READY = 'READY'


class KernelException(Exception):
    pass


class KernelError(StrEnum):
    MISSING_DOTENV = 'no .env file was found in the working directory of the application'
    INVALID_DEFAULT_ENVIRONMENT = 'the application has no default environment configured'
    INVALID_PACKAGE_NAME = "the application's package name is not defined"
