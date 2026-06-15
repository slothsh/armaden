from returns.result import Failure, Success
from returns.result import Failure, Success

from server.application import Application
from server.error import GenericError
from server.error.error import GenericError
from server.lib.types import Error, Result
from server.lib.types import Result, Error

import asyncio
import logging

logger = logging.getLogger("server.entry_point")


class EntryPoint:
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
