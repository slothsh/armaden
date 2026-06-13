"""Main entry point for the Arma Reforger dedicated server Docker image.

This module simply delegates to :class:`server.supervisor.Server`.
For available environment variables see :mod:`server.supervisor`.
"""

import asyncio

from returns.result import Failure, Success
from returns.pipeline import is_successful

from server.lib import Result
from server.api import ApiServer
from server.api.routes import api_routes
from server.supervisor import Supervisor

async def entrypoint() -> Result[None]:
    supervisor = Supervisor()

    api = (
        ApiServer()
        .with_supervisor(supervisor)
        .with_routes(api_routes)
        .build()
    )

    supervisor.with_servers([
        api
    ])

    if not is_successful(result := await supervisor.initialize()):
        return result
        
    if not is_successful(result := await supervisor.run()):
        return result

    if not is_successful(result := await supervisor.shutdown()):
        return result

    return Success(None)


def main() -> Result[None]:
    try:
        return asyncio.run(entrypoint())
    except (KeyboardInterrupt, SystemExit):
        return Success(None)


if __name__ == "__main__":
    try:
        asyncio.run(entrypoint())
    except (KeyboardInterrupt, SystemExit):
        Success(None)
