from enum import StrEnum
from typing import Any, Dict
import logging
import uvicorn
from returns.result import Failure, Success
from fastapi import FastAPI

from framework.facades import config
from framework.classes.server import Server
from framework.enums.health_status import HealthStatus
from framework.utils.types import Result
from framework.errors import Error

logger = logging.getLogger(__name__)


class DefaultApi(Server):
    def __init__(self) -> None:
        self._app = FastAPI(
            title="Public HTTP API"
        )


    # --- Server Interface ----------------------------------------------------

    async def initialize(self) -> Result[None]:
        try:
            server_config = uvicorn.Config(
                app=self._app,
                host=config('api.address'),
                port=config('api.port'),
                loop="none",
                log_config=None,
            )
            self._uvicorn_server = uvicorn.Server(config=server_config)
            return Success(None)
        except Exception as exception:
            return Failure(Error(DefaultApiError.INITIALIZATION_FAILED, {
                'exception': exception
            }))


    async def run(self) -> Result[None]:
        if not self._uvicorn_server:
            return Failure(Error(DefaultApiError.RUN_FAILED, details={
                'message': 'uvicorn server must be initialized before running the api server'
            }))

        try:
            await self._uvicorn_server.serve()
            return Success(None)
        except Exception as exception:
            return Failure(Error(DefaultApiError.RUN_FAILED, details={
                'exception': exception
            }))


    async def shutdown(self) -> Result[None]:
        if self._uvicorn_server and self._uvicorn_server.started:
            self._uvicorn_server.should_exit = True

        return Success(None)


    async def status(self) -> Result[Dict[str, Any]]:
        return Success({
            'status': HealthStatus.OK,
        })


    @property
    def app(self) -> FastAPI:
        return self._app


# --- Internal Types ----------------------------------------------------------


class DefaultApiError(StrEnum):
    INITIALIZATION_FAILED = "an error occurred while initializing the api server"
    RUN_FAILED = "an error occurred while trying to run the api server"
