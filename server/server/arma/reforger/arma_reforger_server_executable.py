"""Arma Reforger dedicated server wrapper.

Provides a typed, fluent interface for driving the Arma Reforger server
executable with all documented launch parameters.

Reference:
    https://community.bistudio.com/wiki/Arma_Reforger:Server_Quick_Start_Guide
"""

from enum import StrEnum

import logging
from pathlib import Path

from returns.result import Success
from server.lib.interfaces import Executable
from server.lib.types import Result

logger = logging.getLogger('server.arma.reforger.executable')


class ArmaReforgerServerExecutable(Executable):
    HEADLESS: str = "-logLevel"
    BIND_IP: str = "-bindIP"
    GAME_HOST: str = "-gproj"
    GAME_PORT: str = "-gamePort"
    STEAM_PORT: str = "-steamPort"
    A2S_ADDRESS: str = "-a2s"
    A2S_PORT: str = "-a2sPort"
    CONFIG_FILE: str = "-config"
    PROFILE_DIR: str = "-profile"
    LOGS_DIR: str = "-logLogs"
    LIMIT_FPS: str = "-limitFPS"
    RCON_HOST: str = "-rcon"
    RCON_PORT: str = "-rconPort"
    RCON_PASSWORD: str = "-rconPassword"
    ADDON: str = "-addon"
    SCENARIO: str = "-scenario"
    AUTO_RELOAD: str = "-autoReload"
    SERVER_ID: str = "-serverId"
    SERVER_REGION: str = "-region"
    LOAD_SESSION_SAVE: str = "-loadSessionSave"
    FORCE_SESSION_LOAD: str = "-forceSessionLoad"

    def __init__(self) -> None:
        super().__init__(ArmaReforgerServerExecutable.resolve_executable)


    @classmethod
    def resolve_executable(cls) -> Result[Path]:
        return Success(Path("/bin/echo"))
        # common_paths = [
        #     Path("/arma/ArmaReforgerServer"),
        #     Path.home() / "Steam" / "steamapps" / "common" / "Arma Reforger" / "ArmaReforgerServer",
        #     Path.home() / ".local" / "share" / "Steam" / "steamapps" / "common" / "Arma Reforger" / "ArmaReforgerServer",
        #     Path("C:\\Program Files (x86)\\Steam\\steamapps\\common\\Arma Reforger\\ArmaReforgerServer.exe"),
        # ]
        #
        # for candidate in common_paths:
        #     if candidate.exists():
        #         return Success(candidate.resolve())
        #
        # return Failure(
        #     Error(ArmaReforgerExecutableError.EXECUTABLE_NOT_FOUND)
        # )


    # -- Arma Reforger Server Flags -------------------------------------------

    def config(self, path: str | Path) -> ArmaReforgerServerExecutable:
        """Path to a server configuration JSON file."""
        self.push(self.CONFIG_FILE, str(Path(path).resolve()))
        return self


    def profile(self, path: str | Path) -> ArmaReforgerServerExecutable:
        """Directory for profiles (saves, logs, settings).

        The directory is created automatically if it does not exist.
        """
        target = Path(path)
        target.mkdir(parents=True, exist_ok=True)
        self.push(self.PROFILE_DIR, str(target.resolve()))
        return self


    def logs_dir(self, path: str | Path) -> ArmaReforgerServerExecutable:
        """Redirect log output to the given directory."""
        target = Path(path)
        target.mkdir(parents=True, exist_ok=True)
        self.push(self.LOGS_DIR, str(target.resolve()))
        return self


    def bind(
        self,
        *,
        address: str | None = None,
        game_port: int | None = None,
        steam_port: int | None = None,
    ) -> ArmaReforgerServerExecutable:
        """Bind the server to specific addresses / ports.

        Keyword Args:
            address: IP address to bind (sets ``-bindIP``).
            game_port: Game UDP port (sets ``-gamePort``).
            steam_port: Steam query UDP port (sets ``-steamPort``).
        """
        if address:
            self.push(self.BIND_IP, address)
        if game_port is not None:
            self.push(self.GAME_PORT, game_port)
        if steam_port is not None:
            self.push(self.STEAM_PORT, steam_port)
        return self


    def a2s(
        self,
        *,
        address: str | None = None,
        query_port: int | None = None,
    ) -> ArmaReforgerServerExecutable:
        """Configure A2S query endpoint.

        Keyword Args:
            address: IP address for A2S queries (sets ``-a2s``).
            query_port: UDP port for A2S queries (sets ``-a2sPort``).
        """
        if address:
            self.push(self.A2S_ADDRESS, address)
        if query_port is not None:
            self.push(self.A2S_PORT, query_port)
        return self


    def rcon(
        self,
        *,
        address: str | None = None,
        port: int | None = None,
        password: str | None = None,
    ) -> ArmaReforgerServerExecutable:
        """Configure BattlEye / RCON remote console.

        Keyword Args:
            address: IP address for RCON (sets ``-rcon``).
            port: TCP port for RCON (sets ``-rconPort``).
            password: RCON password (sets ``-rconPassword``).
        """
        if address:
            self.push(self.RCON_HOST, address)
        if port is not None:
            self.push(self.RCON_PORT, port)
        if password is not None:
            self.push(self.RCON_PASSWORD, password)
        return self


    def limit_fps(self, fps: int) -> ArmaReforgerServerExecutable:
        """Cap the server frame rate."""
        self.push(self.LIMIT_FPS, fps)
        return self


    def addon(self, mod_id: str) -> ArmaReforgerServerExecutable:
        """Load a server-side addon (mod) by ID.

        May be called multiple times to load several mods.
        """
        self.push(self.ADDON, mod_id)
        return self


    def addons(self, *mod_ids: str) -> ArmaReforgerServerExecutable:
        """Load multiple addons at once.

        Args:
            mod_ids: Variable-length list of Steam Workshop / mod IDs.
        """
        for mod_id in mod_ids:
            self.addon(mod_id)
        return self


    def scenario(self, scenario_id: str) -> ArmaReforgerServerExecutable:
        """ID of the scenario to host."""
        self.push(self.SCENARIO, scenario_id)
        return self


    def auto_reload(self, enabled: bool = True) -> ArmaReforgerServerExecutable:
        """Auto-restart the server when it crashes (default: ``True``)."""
        if enabled:
            self._params.append(self.AUTO_RELOAD)
        return self


    def server_id(self, server_id: str) -> ArmaReforgerServerExecutable:
        """Unique server identifier."""
        self.push(self.SERVER_ID, server_id)
        return self


    def region(self, region: str) -> ArmaReforgerServerExecutable:
        """Server region tag (used by the server browser)."""
        self.push(self.SERVER_REGION, region)
        return self


    def load_session_save(self, path: str | Path) -> ArmaReforgerServerExecutable:
        """Path to a session save to load on startup."""
        self.push(self.LOAD_SESSION_SAVE, str(Path(path).resolve()))
        return self


    def force_session_load(self, enabled: bool = True) -> ArmaReforgerServerExecutable:
        """Force loading a session save even if version mismatched."""
        if enabled:
            self._params.append(self.FORCE_SESSION_LOAD)
        return self


    def custom(self, flag: str, *values: str | int) -> ArmaReforgerServerExecutable:
        """Append an arbitrary launch flag and values.

        Useful for undocumented or future parameters.

        Args:
            flag: The flag name (e.g. ``"-myFlag"``).
            values: Flag values.
        """
        self.push(flag, *values)
        return self


# --- Internal Types ----------------------------------------------------------

class ArmaReforgerExecutableError(StrEnum):
    EXECUTABLE_NOT_FOUND = "the arma reforger server executable could not be found in the host system"
