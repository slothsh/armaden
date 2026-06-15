from pathlib import Path
from typing import Any, Dict
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

logger = logging.getLogger('server.application')


# -- Global Handle ------------------------------------------------------------

APPLICATION: Application | None = None


# -- Application --------------------------------------------------------------

class Application:
    PACKAGE_NAME: str | None = None if not __package__ else __package__.split(".")[0]
    CONFIG: Dict[str, Any] = {}

    def __init__(self) -> None:
        self._lock = Lock()
        self._status = ApplicationStatus.NOT_READY
        self._app_env = 'production'


    def version(self) -> str:
        if not Application.PACKAGE_NAME:
            return '0.0.0'
        return metadata.version(Application.PACKAGE_NAME)
    

    @classmethod
    def bootstrap(cls) -> None:
        global APPLICATION

        APPLICATION = Application()

        # Set some essential application flags
        if app_env := os.getenv('APP_ENV'):
            APPLICATION._app_env = app_env

        # Initialize application facilities
        try:
            if not is_successful(APPLICATION._initialize_logging()):
                raise ApplicationException('Could not successfully initialize logging during application bootstrap')
            if not is_successful(APPLICATION._initialize_environment()):
                logger.warning("The application's environment was not successfully initialized, this is not an issue if you did not provide .env file for your application")
            if not is_successful(APPLICATION._initialize_configs()):
                raise ApplicationException("The application's configuration files could not be successfully initialized")
        except ApplicationException as exception:
            raise exception
        except Exception as exception:
            raise ApplicationException(exception)

        # Update application status
        APPLICATION._status = ApplicationStatus.READY
        logger.info('Application successfully bootstrapped with status: %s', APPLICATION._status)


    @classmethod
    def instance(cls) -> Application:
        if APPLICATION is None:
            raise ApplicationException(
                "Could not obtain handle to application. Has it been bootstrapped?"
            )
        return APPLICATION


    @classmethod
    def environment(cls, name: str, default: str | None = None) -> str | None:
        if APPLICATION is None:
            raise ApplicationException(
                "Could not obtain handle to application. Has it been bootstrapped?"
            )

        if result := os.getenv(name):
            return result

        return default


    @classmethod
    def config(cls) -> Dict[str, Any]:
        if APPLICATION is None:
            raise ApplicationException(
                "Could not obtain handle to application. Has it been bootstrapped?"
            )
        return APPLICATION.CONFIG


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
            return Failure(Error(ApplicationError.INVALID_DEFAULT_ENVIRONMENT))

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

        return Failure(Error(ApplicationError.MISSING_DOTENV))


    def _initialize_configs(self) -> Result[None]:
        if not Application.PACKAGE_NAME:
            return Failure(Error(ApplicationError.INVALID_PACKAGE_NAME))

        config_directory = Path(Application.PACKAGE_NAME) / 'config'
        config_files = config_directory.glob('*.py')

        for file in [file for file in config_files if file.is_file() and not file.name.startswith(('.', '_'))]:
            module = import_module(f"{Application.PACKAGE_NAME}.config.{file.stem}")
            config = getattr(module, 'config')
            Application.instance().CONFIG[file.stem] = config()

        return Success(None)


# -- Internal Types -----------------------------------------------------------

class ApplicationStatus(StrEnum):
    NOT_READY = 'NOT_READY'
    READY = 'READY'


class ApplicationException(Exception):
    pass


class ApplicationError(StrEnum):
    MISSING_DOTENV = 'no .env file was found in the working directory of the application'
    INVALID_DEFAULT_ENVIRONMENT = 'the application has no default environment configured'
    INVALID_PACKAGE_NAME = "the application's package name is not defined"
