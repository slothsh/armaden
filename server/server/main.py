"""Main entry point for the Arma Reforger dedicated server Docker image.

This module simply delegates to :class:`server.supervisor.Server`.
For available environment variables see :mod:`server.supervisor`.
"""

import asyncio
import logging

from returns.result import Failure, Success
from returns.pipeline import is_successful

from server.bootstrap import Application, ApplicationException
from server.error import GenericError
from server.lib import Result
from server.api import ApiServer
from server.api.routes import api_routes
from server.lib.facades import app
from server.lib.types import Error
from server.supervisor import Supervisor

logger = logging.getLogger("server")


async def entrypoint() -> Result[None]:
    # Bootstrap the application
    Application.bootstrap()

    # Prepare the supervisor
    supervisor = Supervisor()

    logger.info(app().version())

    api = (
        ApiServer()
        .with_supervisor(supervisor)
        .with_routes(api_routes)
        .build()
    )

    supervisor.with_servers([
        api
    ])

    # Begin the supervisor lifecycle
    if not is_successful(result := await supervisor.initialize()):
        return result

    if not is_successful(result := await supervisor.run()):
        return result

    return Success(None)


def main() -> Result[None]:
    try:
        return asyncio.run(entrypoint())
    except (KeyboardInterrupt, SystemExit):
        return Success(None)
    except ApplicationException as exception:
        return Failure(Error(GenericError.APP_NOT_BOOTSTRAPPED, details={
            'exception': exception
        }))
    except:
        return Failure(Error(GenericError.UNKNOWN))


if __name__ == "__main__":
    try:
        asyncio.run(entrypoint())
    except (KeyboardInterrupt, SystemExit):
        logger.info(Success(None))
    except ApplicationException as exception:
        logger.error(Failure(Error(GenericError.APP_NOT_BOOTSTRAPPED, details={
            'exception': exception
        })))
    except:
        logger.error(Failure(Error(GenericError.UNKNOWN)))
