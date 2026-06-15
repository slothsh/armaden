"""Main entry point for the Arma Reforger dedicated server Docker image.

This module simply delegates to :class:`server.supervisor.Server`.
For available environment variables see :mod:`server.supervisor`.
"""

import asyncio
import logging

from returns.result import Failure, Success
from returns.pipeline import is_successful

from server.api import ApiServer
from server.arma import ArmaReforgerServer
from server.application import Application
from server.error import GenericError
from server.http.routes import api_routes
from server.lib import Result, Error, app, env, config
from server.supervisor import Supervisor

logger = logging.getLogger("server")


async def entrypoint() -> Result[None]:
    application = Application()
    logger.info("Application Name: %s", config('app.name'))
    logger.info("version: %s", app().version())
    logger.info("description: %s", config('app.description'))
    logger.info("environment: %s", env('APP_ENV'))

    # Prepare the supervisor
    logger.info('supervisor')
    supervisor = Supervisor()

    # Prepare the servers
    logger.info('api')
    api = (
        ApiServer()
        .with_supervisor(supervisor)
        .with_routes(api_routes)
        .build()
    )

    logger.info('arma')
    arma_reforger = (
        ArmaReforgerServer()
        .with_supervisor(supervisor)
        .build()
    )

    logger.info('with_servers')
    supervisor.with_servers([
        api,
        arma_reforger,
    ])

    # Begin the supervisor lifecycle
    logger.info('init')
    if not is_successful(result := await supervisor.initialize()):
        return result

    logger.info('run')
    if not is_successful(result := await supervisor.run()):
        return result

    return Success(None)


def main() -> Result[None]:
    try:
        return asyncio.run(entrypoint())
    except (KeyboardInterrupt, SystemExit):
        return Success(None)
    except Exception as exception:
        return Failure(Error(GenericError.EXCEPTION, details={
            'exception': exception
        }))
    except:
        return Failure(Error(GenericError.UNKNOWN))


if __name__ == "__main__":
    try:
        asyncio.run(entrypoint())
    except (KeyboardInterrupt, SystemExit):
        logger.info(Success(None))
    except Exception as exception:
        logger.error(Error(GenericError.EXCEPTION, details={
            'exception': exception
        }))
    except:
        logger.error(Failure(Error(GenericError.UNKNOWN)))
