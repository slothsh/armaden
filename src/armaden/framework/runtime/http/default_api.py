from __future__ import annotations

import asyncio
from enum import StrEnum
from typing import override

import uvicorn
from fastapi import FastAPI
from returns.result import Failure, Success

from armaden.framework.enums.health_status import HealthStatus
from armaden.framework.error.error import Error
from armaden.framework.protocols.configuration_protocol import ConfigurationProtocol
from armaden.framework.protocols.default_api_protocol import DefaultApiProtocol
from armaden.framework.protocols.task_runtime_protocol import TaskRuntimeProtocol
from armaden.framework.types.result import Result


class DefaultApi(DefaultApiProtocol):
    def __init__(self) -> None:
        self._app: FastAPI = FastAPI(title='Public HTTP API')
        self._uvicorn_server: uvicorn.Server | None = None


    @property
    def app(self) -> FastAPI:
        return self._app


    @override
    async def initialize(
        self,
        runtime: TaskRuntimeProtocol,
        configuration: ConfigurationProtocol,
    ) -> Result[None]:
        _ = runtime
        try:
            host = configuration.get('api.address', '0.0.0.0')
            port = configuration.get('api.port', 8888)
            self._uvicorn_server = uvicorn.Server(uvicorn.Config(
                app=self._app,
                host=host if isinstance(host, str) else '0.0.0.0',
                port=port if isinstance(port, int) else 8888,
                loop='none',
                log_config=None,
            ))
            return Success(None)
        except Exception as exception:
            return Failure(Error(DefaultApiError.INITIALIZATION_FAILED, details={
                'exception': exception,
            }))


    @override
    async def run(self, runtime: TaskRuntimeProtocol) -> Result[None]:
        if self._uvicorn_server is None:
            return Failure(Error(DefaultApiError.RUN_FAILED, details={
                'message': 'uvicorn server must be initialized before running the api server',
            }))
        try:
            serve_task = asyncio.create_task(self._uvicorn_server.serve())
            while not self._uvicorn_server.started:
                await asyncio.sleep(0.1)
            _ = await runtime.signal_ready()
            await serve_task
            return Success(None)
        except Exception as exception:
            return Failure(Error(DefaultApiError.RUN_FAILED, details={
                'exception': exception,
            }))


    @override
    async def shutdown(self, runtime: TaskRuntimeProtocol) -> Result[None]:
        _ = runtime
        if self._uvicorn_server is not None and self._uvicorn_server.started:
            self._uvicorn_server.should_exit = True
        return Success(None)


    @override
    async def status(
        self,
        runtime: TaskRuntimeProtocol,
    ) -> Result[dict[str, object]]:
        _ = runtime
        return Success({'status': HealthStatus.OK})


class DefaultApiError(StrEnum):
    INITIALIZATION_FAILED = 'an error occurred while initializing the api server'
    RUN_FAILED = 'an error occurred while trying to run the api server'
