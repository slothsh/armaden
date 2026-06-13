import sys
import logging
from enum import StrEnum
import threading
from threading import Lock

logger = logging.getLogger('server.application')


# -- Global Handle ------------------------------------------------------------

APPLICATION: Application | None = None


# -- Application --------------------------------------------------------------

class Application:
    def __init__(self) -> None:
        self._lock = Lock()
        self._status = ApplicationStatus.NOT_READY


    def version(self) -> str:
        return '0.1.0'
    

    @classmethod
    def bootstrap(cls) -> None:
        global APPLICATION
        cls._initialize_logging()
        APPLICATION = Application()
        APPLICATION._status = ApplicationStatus.READY
        logger.info('Application successfully bootstrapped: %s', APPLICATION._status)
        logger.info(APPLICATION)


    @classmethod
    def instance(cls) -> Application:
        if APPLICATION is None:
            raise ApplicationException(
                "Could not obtain handle to application. Has it been bootstrapped?"
            )
        return APPLICATION


    # -- Logging --------------------------------------------------------------

    @classmethod
    def _initialize_logging(cls) -> None:
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s [%(levelname)s][%(name)s][%(threadName)s]: %(message)s",
            stream=sys.stdout,
        )


# -- Internal Types -----------------------------------------------------------

class ApplicationStatus(StrEnum):
    NOT_READY = 'NOT_READY'
    READY = 'READY'


class ApplicationException(Exception):
    pass
