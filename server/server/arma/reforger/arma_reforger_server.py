from enum import StrEnum
from typing import Union
from pathlib import Path

from returns.result import Failure, Success
from server.lib import Result
from server.arma.reforger.arma_reforger_server_executable import ArmaReforgerServerExecutable
from server.lib import Server
from server.lib.types import Error
from server.steamcmd import SteamCmdExecutable, SteamCmdResult

class ArmaReforgerServer(Server):
    STEAM_APP_ID: int = 1874900
    STEAM_APP_ID_CLIENT: int = 1874880

    executable: ExecutableContainer

    def __init__(self):
        setattr(self.executable, 'steamcmd', SteamCmdExecutable())
        setattr(self.executable, 'reforger', ArmaReforgerServerExecutable())


    # -- Server Interface -----------------------------------------------------

    async def initialize(self) -> Result[None]:
        return Failure(Error(ArmaReforgerServerError.INITIALIZATION_FAILED))


    async def run(self) -> Result[None]:
        return Success(None)


    async def shutdown(self) -> Result[None]:
        return Success(None)


    # -- SteamCmdExecutable helpers -------------------------------------------

    @classmethod
    def install(
        cls,
        install_dir: str | Path,
        *,
        steamcmd: SteamCmdExecutable | None = None,
        validate: bool = False,
    ) -> SteamCmdResult:
        """Install the Arma Reforger dedicated server via SteamCMD.

        Args:
            install_dir: Target installation directory.
            steamcmd: Custom :class:`SteamCmdExecutable` instance.  A default one is
                created if omitted.
            validate: Verify file integrity after installation.

        Returns:
            The :class:`SteamCmdResult` from the install operation.
        """
        sc = steamcmd or SteamCmdExecutable()
        return (
            sc.login_anonymous()
            .force_install_dir(install_dir)
            .app_update(cls.STEAM_APP_ID, validate=validate)
            .run()
        )

    @classmethod
    def update(
        cls,
        install_dir: str | Path,
        *,
        steamcmd: SteamCmdExecutable | None = None,
        validate: bool = True,
    ) -> SteamCmdResult:
        """Update the server installation via SteamCMD.

        Args:
            install_dir: Existing server installation directory.
            steamcmd: Custom :class:`SteamCmdExecutable` instance.
            validate: Verify file integrity (recommended for updates).

        Returns:
            The :class:`SteamCmdResult` from the update operation.
        """
        return cls.install(install_dir, steamcmd=steamcmd, validate=validate)


# --- Internal Types ----------------------------------------------------------

type ExecutableUnion = Union[SteamCmdExecutable, ArmaReforgerServerExecutable]

class ExecutableContainer:
    def __getattr__(self, name: str) -> ExecutableUnion:
        return self.__dict__[name]

class ArmaReforgerServerError(StrEnum):
    INITIALIZATION_FAILED = "an error occurred while initializing the arma reforger server"
