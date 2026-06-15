import logging

from returns.result import Success

from server.application.kernel import Kernel
from server.lib.types import Result
from server.services.api_service import ApiService
from server.services.arma_reforger_service import ArmaReforgerService

logger = logging.getLogger('server.application')


class Application(Kernel):
    def __init__(self):
        super().__init__(self)

        logger.info("Application Name: %s", self.config('app.name'))
        logger.info("version: %s", self.version())
        logger.info("description: %s", self.config('app.description'))
        logger.info("environment: %s", self.environment('APP_ENV'))

        self.services.extend([
            ApiService(),
            ArmaReforgerService(),
        ])


# -- Internal Types -----------------------------------------------------------

class ApplicationException(Exception):
    pass
