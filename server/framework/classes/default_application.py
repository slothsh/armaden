import traceback
import asyncio
import logging
from typing import Type
from returns.result import Success, Failure
from returns.pipeline import is_successful

from .kernel import Kernel
from .module_loader import ModuleLoader
from ..errors import GenericError, Error
from ..utils.types import Result

logger = logging.getLogger(__name__)


class DefaultApplication(Kernel):
    def __init__(self, handle: DefaultApplication | None = None):
        super().__init__(handle if handle else self, package_name='app')


    @staticmethod
    def main() -> Result[None]:
        try:
            user_application = ModuleLoader.try_load_user_application(Type[DefaultApplication])
            if not is_successful(user_application):
                print(user_application.failure())

            result = Kernel.bootstrap(
                default_application=DefaultApplication,
                user_application=user_application.value_or(None)
            )
            
            if not is_successful(result):
                return result.map(lambda _: None)

            application = result.unwrap()

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
