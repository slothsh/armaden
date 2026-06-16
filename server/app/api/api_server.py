from enum import StrEnum
from typing import Any, Dict, List, Self, Tuple
from collections.abc import Callable
import logging
import uvicorn
from returns.result import Failure, Success
from fastapi import FastAPI
from contextlib import asynccontextmanager

from framework.classes.server import Server
from framework.enums.health_status import HealthStatus
from framework.utils.types import Result
from framework.errors import Error
from framework.classes.rcon_client import RconClient
from framework.facades import config

logger = logging.getLogger("app.api_server")


class ApiServer(Server):
    def __init__(self) -> None:
        self.app = FastAPI(
            title="Arma Reforger Server public HTTP API"
        )

        self._rcon_clients = RconContainer()


    # --- Builder Methods -----------------------------------------------------

    def with_rcon_clients(self, rcon_clients: List[Tuple[str, RconClient]]) -> Self:
        for (name, client) in rcon_clients:
            setattr(self._rcon_clients, name, client)
        return self


    def with_routes(self, routes: Callable[[FastAPI], None]) -> Self:
        routes(self.app)
        return self


    def build(self) -> Self:
        @asynccontextmanager
        async def lifespan(_: FastAPI):
            yield
            for client in vars(self._rcon_clients).values():
                if client.is_connected:
                    await client.disconnect()

        self.app.router.lifespan_context = lifespan

        return self


    # --- Server Interface ----------------------------------------------------

    async def initialize(self) -> Result[None]:
        try:
            server_config = uvicorn.Config(
                app=self.app,
                host=config('api.address'),
                port=config('api.port'),
                loop="none",
                log_config=None,
            )
            self._uvicorn_server = uvicorn.Server(config=server_config)
            return Success(None)
        except Exception as exception:
            return Failure(Error(ApiServerError.INITIALIZATION_FAILED, {
                'exception': exception
            }))


    async def run(self) -> Result[None]:
        if not self._uvicorn_server:
            return Failure(Error(ApiServerError.RUN_FAILED, details={
                'message': 'uvicorn server must be initialized before running the api server'
            }))

        try:
            await self._uvicorn_server.serve()
            return Success(None)
        except Exception as exception:
            return Failure(Error(ApiServerError.RUN_FAILED, details={
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


# --- Internal Types ----------------------------------------------------------

class RconContainer:
    def __getattr__(self, name: str) -> RconClient:
        return self.__dict__[name]

class ApiServerError(StrEnum):
    INITIALIZATION_FAILED = "an error occurred while initializing the api server"
    RUN_FAILED = "an error occurred while trying to run the api server"
