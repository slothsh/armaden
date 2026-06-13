from enum import StrEnum
from typing import Self, Union
from pathlib import Path

from returns.result import Failure, Success
from server.arma.reforger.arma_reforger_server_executable import ArmaReforgerServerExecutable
from server.arma.reforger.arma_reforger_rcon_client import ArmaReforgerRconClient
from server.lib import Result, Server, Error
from server.steamcmd import SteamCmdExecutable, SteamCmdResult

class ArmaReforgerServer(Server):
    STEAM_APP_ID: int = 1874900
    STEAM_APP_ID_CLIENT: int = 1874880

    def __init__(self):
        self._executable = ExecutableContainer()
        setattr(self._executable, 'steamcmd', SteamCmdExecutable())
        setattr(self._executable, 'reforger', ArmaReforgerServerExecutable())

        self._rcon_client = ArmaReforgerRconClient('127.0.0.1', 2011, 'password')


    # --- Accessor Methods -----------------------------------------------------

    def rcon_client(self) -> ArmaReforgerRconClient | None:
        return self._rcon_client


    # --- Builder Methods -----------------------------------------------------

    def build(self) -> Self:
        return self


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
