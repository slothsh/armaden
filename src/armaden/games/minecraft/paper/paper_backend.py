from __future__ import annotations

from enum import StrEnum
from typing import final, override

from returns.result import Failure

from armaden.framework.api.error import Error
from armaden.framework.protocols.task_runtime_protocol import TaskRuntimeProtocol
from armaden.framework.types.result import Result
from armaden.games.minecraft.minecraft_server_config import (
    Config as MinecraftServerConfig,
)
from armaden.games.minecraft.protocols import MinecraftServerBackendProtocol


class PaperBackendError(StrEnum):
    CONFIGURATION_NOT_IMPLEMENTED = (
        'paper server configuration preparation is not implemented yet'
    )
    INSTALLATION_NOT_IMPLEMENTED = 'paper server installation is not implemented yet'
    LAUNCH_COMMAND_NOT_IMPLEMENTED = (
        'paper server launch command construction is not implemented yet'
    )
    UPDATE_NOT_IMPLEMENTED = 'paper server updates are not implemented yet'


@final
class PaperBackend(MinecraftServerBackendProtocol):
    def __init__(self, config: MinecraftServerConfig) -> None:
        self._config: MinecraftServerConfig = config


    @override
    async def install(self, runtime: TaskRuntimeProtocol) -> Result[None]:
        _ = runtime
        return Failure(
            Error(
                PaperBackendError.INSTALLATION_NOT_IMPLEMENTED,
                details={
                    'installation': self._config.get('installation'),
                    'paper': self._config.get('paper'),
                },
            )
        )


    @override
    def launch_command(self) -> Result[list[str]]:
        return Failure(
            Error(
                PaperBackendError.LAUNCH_COMMAND_NOT_IMPLEMENTED,
                details={
                    'arguments': self._config.get('arguments'),
                    'installation': self._config.get('installation'),
                    'java': self._config.get('java'),
                    'jvm': self._config.get('jvm'),
                },
            )
        )


    @override
    async def prepare(self) -> Result[None]:
        return Failure(
            Error(
                PaperBackendError.CONFIGURATION_NOT_IMPLEMENTED,
                details={
                    'eula': self._config.get('eula'),
                    'server': self._config.get('server'),
                },
            )
        )


    @override
    async def update(self, runtime: TaskRuntimeProtocol) -> Result[None]:
        _ = runtime
        return Failure(
            Error(
                PaperBackendError.UPDATE_NOT_IMPLEMENTED,
                details={
                    'installation': self._config.get('installation'),
                    'paper': self._config.get('paper'),
                },
            )
        )