from enum import StrEnum
from typing import List, Self, Tuple, Union
from collections.abc import Callable
import logging
import uvicorn
from returns.result import Failure, Success
from fastapi import FastAPI
from contextlib import asynccontextmanager
from server.lib.interfaces import Server
from server.lib.types import Error, Result
from server.rcon.rcon_client import RconClient
from server.lib import QueueableSupervisor, config
from server.arma import ArmaReforgerRconClient

logger = logging.getLogger("server.api_server")

class ApiServer(Server):
    supervisor: QueueableSupervisor | None
    rcon_clients: RconContainer

    def __init__(self) -> None:
        self.app = FastAPI(
            title="Arma Reforger Server public HTTP API"
        )

        self._supervisor: QueueableSupervisor | None = None
        self._rcon_clients = RconContainer()


    # --- Builder Methods -----------------------------------------------------

    def with_supervisor(self, supervisor: QueueableSupervisor) -> Self:
        self.supervisor = supervisor
        return self


    def with_rcon_clients(self, rcon_clients: List[Tuple[str, RconClientUnion]]) -> Self:
        for (name, client) in rcon_clients:
            setattr(self.rcon_clients, name, client)
        return self


    def with_routes(self, routes: Callable[[FastAPI], None]) -> Self:
        routes(self.app)
        return self


    def build(self) -> Self:
        @asynccontextmanager
        async def lifespan(_: FastAPI):
            yield
            for client in vars(self._rcon_clients).values():
                if client.is_connected():
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
        except Exception as e:
            return Failure(Error(ApiServerError.INITIALIZATION_FAILED, {
                'exception': e
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


# --- Internal Types ----------------------------------------------------------

type RconClientUnion = Union[RconClient, ArmaReforgerRconClient]

class RconContainer:
    def __getattr__(self, name: str) -> RconClientUnion:
        return self.__dict__[name]

class ApiServerError(StrEnum):
    INITIALIZATION_FAILED = "an error occurred while initializing the api server"
    RUN_FAILED = "an error occurred while trying to run the api server"
