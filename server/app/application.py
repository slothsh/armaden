import asyncio
import logging

from returns.result import Failure, Success

from framework.kernel import Kernel
from framework.utils.types import Result
from framework.errors import Error, GenericError

from app.services.api_service import ApiService
from app.services.arma_reforger_service import ArmaReforgerService

logger = logging.getLogger('app.application')


class Application(Kernel):
    def __init__(self):
        super().__init__(self, package_name='app')

        logger.info("Application Name: %s", self.config('app.name'))
        logger.info("version: %s", self.version())
        logger.info("description: %s", self.config('app.description'))
        logger.info("environment: %s", self.environment('APP_ENV'))

        self.services.extend([
            ApiService(),
            ArmaReforgerService(),
        ])


    @staticmethod
    def main() -> Result[None]:
        try:
            application = Application()
            return asyncio.run(application())
        except (KeyboardInterrupt, SystemExit):
            return Success(None)
        except Exception as exception:
            return Failure(Error(GenericError.EXCEPTION, details={
                'exception': exception
            }))
        except:
            return Failure(Error(GenericError.UNKNOWN))


    def version(self) -> str:
        from importlib import metadata
        try:
            return metadata.version('server')
        except metadata.PackageNotFoundError:
            return '0.0.0'


# -- Internal Types -----------------------------------------------------------

class ApplicationException(Exception):
    pass
