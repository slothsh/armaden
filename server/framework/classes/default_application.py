import traceback
import asyncio
import logging
from returns.result import Success, Failure
from returns.pipeline import is_successful

from .kernel import Kernel
from ..errors import GenericError, Error
from ..utils.types import Result

logger = logging.getLogger(__name__)


class DefaultApplication(Kernel):
    def __init__(self, handle: DefaultApplication | None = None):
        super().__init__(handle if handle else self, package_name='app')


    @staticmethod
    def main() -> Result[None]:
        try:
            application = Kernel.bootstrap(DefaultApplication)
            
            if not is_successful(application):
                return application.map(lambda _: None)

            application = application.unwrap()

            return asyncio.run(application(), loop_factory=application.event_loop)
        except (KeyboardInterrupt, SystemExit):
            return Success(None)
        except Exception as exception:
            traceback.print_exception(type(exception), exception, exception.__traceback__)
            return Failure(Error(GenericError.EXCEPTION, details={
                'exception': exception
            }))
        except:
            return Failure(Error(GenericError.UNKNOWN))
