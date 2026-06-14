from pathlib import Path
from dotenv import load_dotenv
from enum import StrEnum
from threading import Lock
import logging
import os
import sys
from glob import glob

from returns.pipeline import is_successful
from returns.result import Failure, Success

from server.lib.types import Error, Result

logger = logging.getLogger('server.application')


# -- Global Handle ------------------------------------------------------------

APPLICATION: Application | None = None


# -- Application --------------------------------------------------------------

class Application:
    def __init__(self) -> None:
        self._lock = Lock()
        self._status = ApplicationStatus.NOT_READY
        self._app_env = 'production'


    def version(self) -> str:
        return '0.1.0'
    

    @classmethod
    def bootstrap(cls) -> None:
        global APPLICATION

        APPLICATION = Application()

        # Set some essential application flags
        if app_env := os.getenv(EnvVariableName.APP_ENV):
            APPLICATION._app_env = app_env

        # Initialize application facilities
        try:
            if not is_successful(APPLICATION._initialize_logging()):
                raise ApplicationException('Could not successfully initialize logging during application bootstrap')
            if not is_successful(APPLICATION._initialize_environment()):
                logger.warning("The application's environment was not successfully initialized, this is not an issue if you did not provide .env file for your application")
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


    # -- Initializers ---------------------------------------------------------

    def _initialize_environment(self) -> Result[None]:
        if not self._app_env:
            raise ApplicationException('Cannot initialize the app environment when no default environment is configured')

        # Check env files in order
        env_file_patterns = [
            f".env.{self._app_env}",
            f".env.*.{self._app_env}",
            '.env',
        ]

        for pattern in env_file_patterns:
            paths = glob(pattern)
            if len(paths) != 1:
                continue

            load_dotenv(Path(paths[0]).absolute())
            return Success(None)

        return Failure(Error(ApplicationError.MISSING_DOTENV))


    def _initialize_logging(self) -> Result[None]:
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s [%(levelname)s][%(name)s][%(threadName)s]: %(message)s",
            stream=sys.stdout,
        )

        return Success(None)


# -- Internal Types -----------------------------------------------------------

class ApplicationStatus(StrEnum):
    NOT_READY = 'NOT_READY'
    READY = 'READY'


class EnvVariableName(StrEnum):
    APP_ENV = 'APP_ENV'


class ApplicationException(Exception):
    pass


class ApplicationError(StrEnum):
    MISSING_DOTENV = 'no .env file was found in the working directory of the application'
