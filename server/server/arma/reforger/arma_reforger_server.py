from dataclasses import dataclass
from enum import StrEnum
import logging
from typing import Self, Union
from pathlib import Path

from returns.pipeline import is_successful
from returns.result import Failure, Success
from server.arma.reforger.arma_reforger_server_executable import ArmaReforgerServerExecutable
from server.arma.reforger.arma_reforger_rcon_client import ArmaReforgerRconClient
from server.lib import Result, Server, Error
from server.lib.interfaces import QueueableSupervisor
from server.steamcmd import SteamCmdExecutable

logger = logging.getLogger('server.arma.reforger.server')

class ArmaReforgerServer(Server):
    STEAM_APP_ID: int = 1874900
    STEAM_APP_ID_CLIENT: int = 1874880

    def __init__(self):
        self._supervisor: QueueableSupervisor | None = None

        self._executable = ExecutableContainer(
            steamcmd=SteamCmdExecutable(),
            reforger=ArmaReforgerServerExecutable()
        )

        self._rcon_client = ArmaReforgerRconClient('127.0.0.1', 2011, 'password')


    # --- Accessor Methods -----------------------------------------------------

    def rcon_client(self) -> ArmaReforgerRconClient | None:
        return self._rcon_client


    # --- Builder Methods -----------------------------------------------------

    def with_supervisor(self, supervisor: QueueableSupervisor) -> Self:
        self._supervisor = supervisor
        return self


    def build(self) -> Self:
        return self


    # -- Server Interface -----------------------------------------------------

    async def initialize(self) -> Result[None]:
        if not is_successful(result := await self.install("path/to/installation", True)):
            return result

        try:
            return Success(None)
        except Exception as e:
            return Failure(Error(ArmaReforgerServerError.INITIALIZATION_FAILED, {
                'exception': e
            }))


    async def run(self) -> Result[None]:
        if not self._supervisor:
            return Failure(Error(ArmaReforgerServerError.SUPERVISOR_UNAVAILABLE))

        argv = (
            self._executable.reforger
            .config('path/to/config')
            .rcon(address='127.0.0.1', port=2011, password='password')
            .build_argv()
        )

        await self._supervisor.dispatch_subprocess(argv)

        return await self.shutdown()


    async def shutdown(self) -> Result[None]:
        return Success(None)


    # -- steamcmd helpers -------------------------------------------

    async def install(
        self,
        install_dir: str | Path,
        validate: bool = False,
    ) -> Result[None]:
        if not self._supervisor:
            return Failure(Error(ArmaReforgerServerError.SUPERVISOR_UNAVAILABLE))

        cmd = (
            self._executable.steamcmd
            .login_anonymous()
            .force_install_dir(install_dir)
            .app_update(self.STEAM_APP_ID, validate=validate)
            .build_argv()
        )

        if not is_successful(result := await self._supervisor.dispatch_subprocess(cmd)):
            logger.info('An error occurred trying to install the Arma Reforger Server Assets: %s', result.failure())
            return result.map(lambda _: None)

        return Success(None)

    # @classmethod
    # def update(
    #     cls,
    #     install_dir: str | Path,
    #     *,
    #     steamcmd: SteamCmdExecutable | None = None,
    #     validate: bool = True,
    # ) -> SteamCmdResult:
    #     """Update the server installation via SteamCMD.
    #
    #     Args:
    #         install_dir: Existing server installation directory.
    #         steamcmd: Custom :class:`SteamCmdExecutable` instance.
    #         validate: Verify file integrity (recommended for updates).
    #
    #     Returns:
    #         The :class:`SteamCmdResult` from the update operation.
    #     """
    #     return cls.install(install_dir, steamcmd=steamcmd, validate=validate)


# --- Internal Types ----------------------------------------------------------

type ExecutableUnion = Union[SteamCmdExecutable, ArmaReforgerServerExecutable]

@dataclass
class ExecutableContainer:
    steamcmd: SteamCmdExecutable
    reforger: ArmaReforgerServerExecutable


class ArmaReforgerServerError(StrEnum):
    INITIALIZATION_FAILED = "an error occurred while initializing the arma reforger server"
    SUPERVISOR_UNAVAILABLE = "an arma reforger server's supervisor is unavailable"
