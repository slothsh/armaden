import asyncio

from returns.result import Failure, Success

from server.error.error import GenericError
from server.lib.types import Error, Result
import asyncio
import logging

from returns.result import Failure, Success
from returns.pipeline import is_successful

from server.api.api_server import ApiServer
from server.arma.reforger import ArmaReforgerServer
from server.application import Application
from server.error import GenericError
from server.http.routes import api_routes
from server.facades.app import app
from server.facades.env import env
from server.facades.config import config
from server.lib.types import Result, Error
from server.supervisor import Supervisor

logger = logging.getLogger("server.entry_point")


class EntryPoint:
    @staticmethod
    def main() -> Result[None]:
        async def main() -> Result[None]:
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

        try:
            Application()
            logger.info("Application Name: %s", config('app.name'))
            logger.info("version: %s", app().version())
            logger.info("description: %s", config('app.description'))
            logger.info("environment: %s", env('APP_ENV'))
            return asyncio.run(main())
        except (KeyboardInterrupt, SystemExit):
            return Success(None)
        except Exception as exception:
            return Failure(Error(GenericError.EXCEPTION, details={
                'exception': exception
            }))
        except:
            return Failure(Error(GenericError.UNKNOWN))
