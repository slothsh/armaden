from __future__ import annotations

import logging
from collections.abc import Callable
from copy import deepcopy
from enum import StrEnum
from typing import ClassVar, Self, final

from returns.pipeline import is_successful
from returns.result import Failure, Success

from armaden.framework.api.configurable import Configurable
from armaden.framework.api.error import Error
from armaden.framework.protocols.task_runtime_protocol import TaskRuntimeProtocol
from armaden.framework.types.result import Result
from armaden.games.minecraft.enums import MinecraftServerBackend
from armaden.games.minecraft.minecraft_server_config import (
    Config as MinecraftServerConfig,
    DEFAULT_CONFIG,
)
from armaden.games.minecraft.paper.paper_backend import PaperBackend
from armaden.games.minecraft.protocols import MinecraftServerBackendProtocol

logger = logging.getLogger(__name__)


@final
class MinecraftServer(Configurable[MinecraftServerConfig]):
    _BACKEND_REGISTRY: ClassVar[dict[MinecraftServerBackend, Callable[[MinecraftServerConfig], MinecraftServerBackendProtocol]]] = {
        MinecraftServerBackend.PAPER: PaperBackend,
    }

    config: MinecraftServerConfig = DEFAULT_CONFIG

    _backend: MinecraftServerBackendProtocol | None
    _initialized: bool

    def __new__(
        cls,
        *,
        config: MinecraftServerConfig | None = None,
    ) -> Self:
        return super().__new__(cls, config=config)


    def __init__(self, *, config: MinecraftServerConfig | None = None) -> None:
        _ = config
        self.config = deepcopy(self.config)
        self._backend = None
        self._initialized = False


    async def initialize(self, runtime: TaskRuntimeProtocol) -> Result[None]:
        self._backend = None
        self._initialized = False

        if not is_successful(validation := self._validate_configuration()):
            return validation

        if not is_successful(selection := self._select_backend()):
            return selection.map(lambda _: None)

        backend = selection.unwrap()
        self._backend = backend

        if not is_successful(installation := await backend.install(runtime)):
            return installation

        if not is_successful(preparation := await backend.prepare()):
            return preparation

        self._initialized = True
        return Success(None)


    async def run(self, runtime: TaskRuntimeProtocol) -> Result[None]:
        backend = self._backend

        if backend is None or not self._initialized:
            return Failure(Error(MinecraftServerError.NOT_INITIALIZED))

        if not is_successful(command := backend.launch_command()):
            return command.map(lambda _: None)

        installation = self.config.get('installation')
        directory = installation.get('directory') if installation else None

        if not is_successful(readiness := await runtime.signal_ready()):
            return readiness

        if not is_successful(
            execution := await runtime.dispatch_subprocess(
                command.unwrap(),
                cwd=directory,
                handle_std_stream=self._log_subprocess,
            )
        ):
            return execution.map(lambda _: None)

        return await self.shutdown()


    async def shutdown(self) -> Result[None]:
        return Success(None)


    async def status(self, runtime: TaskRuntimeProtocol) -> Result[dict[str, object]]:
        _ = runtime
        return Success(
            {
                'backend': self.config.get('backend'),
                'initialized': self._initialized,
            }
        )


    @classmethod
    async def _log_subprocess(cls, line: str) -> Result[None]:
        logger.info(line)
        return Success(None)


    def _select_backend(self) -> Result[MinecraftServerBackendProtocol]:
        name = self.config.get('backend') or MinecraftServerBackend.PAPER.value

        try:
            kind = MinecraftServerBackend(name)
        except ValueError:
            return Failure(
                Error(
                    MinecraftServerError.UNKNOWN_BACKEND,
                    details={
                        'backend': name,
                        'supported': [
                            member.value for member in MinecraftServerBackend
                        ],
                    },
                )
            )

        backend_factory = self._BACKEND_REGISTRY.get(kind)

        if backend_factory is None:
            return Failure(
                Error(
                    MinecraftServerError.UNKNOWN_BACKEND,
                    details={
                        'backend': name,
                        'supported': [
                            member.value for member in MinecraftServerBackend
                        ],
                    },
                )
            )

        return Success(backend_factory(self.config))


    def _validate_configuration(self) -> Result[None]:
        paper = self.config.get('paper')

        if paper and paper.get('build') is not None and paper.get('version') is None:
            return Failure(
                Error(
                    MinecraftServerError.INVALID_CONFIGURATION,
                    details={
                        'paper': paper,
                        'reason': 'a paper build requires an explicit paper version',
                    },
                )
            )

        return Success(None)


# --- Internal Types ----------------------------------------------------------

class MinecraftServerError(StrEnum):
    INVALID_CONFIGURATION = 'the minecraft server configuration is invalid or mutually incompatible'
    NOT_INITIALIZED = 'the minecraft server backend has not been initialized'
    UNKNOWN_BACKEND = 'the requested minecraft server backend is not supported'