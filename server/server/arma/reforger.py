"""Arma Reforger dedicated server wrapper.

Provides a typed, fluent interface for driving the Arma Reforger server
executable with all documented launch parameters.

Reference:
    https://community.bistudio.com/wiki/Arma_Reforger:Server_Quick_Start_Guide
"""

from __future__ import annotations

import dataclasses
import logging
import os
import shutil
import subprocess
from collections.abc import Iterator
from pathlib import Path
from typing import Any

from server.steamcmd import SteamCmd, SteamCmdError, SteamCmdResult

logger = logging.getLogger(__name__)

STEAM_APP_ID: int = 1874900
STEAM_APP_ID_CLIENT: int = 1874880


class ArmaServerError(Exception):
    """Base exception for Arma Reforger server errors."""

    pass


class ArmaServerNotFoundError(ArmaServerError):
    """Raised when the server executable cannot be located."""

    pass


class ArmaServerExitError(ArmaServerError):
    """Raised when the server exits with a non-zero status.

    Attributes:
        returncode: Exit code from the process.
        stdout: Captured standard output.
        stderr: Captured standard error.
        command: The argument list passed to the executable.
    """

    def __init__(
        self,
        returncode: int,
        stdout: str,
        stderr: str,
        command: list[str],
    ) -> None:
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr
        self.command = command
        super().__init__(
            f"Arma Reforger server exited with code {returncode}: "
            f"{' '.join(command[:5])}..."
        )


@dataclasses.dataclass(frozen=True)
class ArmaServerResult:
    """Result of an Arma Reforger server execution.

    Attributes:
        returncode: Process exit code.
        stdout: Complete standard output as a string.
        stderr: Complete standard error as a string.
        command: The full list of arguments passed to the subprocess.
    """

    returncode: int
    stdout: str
    stderr: str
    command: list[str]

    @property
    def success(self) -> bool:
        """Whether the server started and exited cleanly (``returncode == 0``)."""
        return self.returncode == 0

    def raise_for_status(self) -> ArmaServerResult:
        """Raise :exc:`ArmaServerExitError` if the server exited with an error.

        Returns:
            ``self`` for fluent chaining.

        Raises:
            ArmaServerExitError: If ``returncode != 0``.
        """
        if not self.success:
            raise ArmaServerExitError(
                self.returncode,
                self.stdout,
                self.stderr,
                self.command,
            )
        return self


class ArmaReforgerServer:
    """Fluent wrapper for the Arma Reforger dedicated server executable.

    Launch parameters are accumulated via method calls until :meth:`run` or
    :meth:`stream` is invoked.  Headless execution is assumed by default.

    Args:
        executable: Path to the server binary.  Falls back to `PATH` lookup
            if not given.
        config: Path to a server JSON configuration file.
        profile: Path to the profile directory (saves, logs, settings).
        logs_dir: Path to redirect log output (``-logLogs`` flag).
        cwd: Working directory for the subprocess.
        env: Additional environment variables for the subprocess.

    Example::

        server = (
            ArmaReforgerServer()
            .config("/arma/config.json")
            .bind(host="0.0.0.0", game_port=2001, steam_port=17777)
            .rcon(host="0.0.0.0", port=19999, password="s3cret")
            .auto_reload()
        )
        server.run()
    """

    # Switch constants
    HEADLESS: str = "-logLevel"  # non-interactive / daemon mode flag
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

    def __init__(
        self,
        executable: str | Path | None = None,
        *,
        config: str | Path | None = None,
        profile: str | Path | None = None,
        logs_dir: str | Path | None = None,
        cwd: str | Path | None = None,
        env: dict[str, str] | None = None,
    ) -> None:
        self._executable = self._resolve_executable(executable)
        self._cwd = cwd
        self._env: dict[str, str] = {**os.environ, **(env or {})}
        self._params: list[str] = []

        if config:
            self.config(config)
        if profile:
            self.profile(profile)
        if logs_dir:
            self.logs_dir(logs_dir)

    @classmethod
    def _resolve_executable(cls, executable: str | Path | None = None) -> Path:
        """Return the absolute path to the server binary.

        Raises:
            ArmaServerNotFoundError: If no binary can be found.
        """
        if executable is not None:
            path = Path(executable)
            if path.exists():
                return path.resolve()
            found = shutil.which(str(executable))
            if found:
                return Path(found).resolve()
            raise ArmaServerNotFoundError(
                f"Provided executable not found: {executable}"
            )

        found = shutil.which("ArmaReforgerServer")
        if found:
            return Path(found).resolve()

        # Common install locations inside a Steam download.
        common_paths = (
            Path("/arma/ArmaReforgerServer"),
            Path.home() / "Steam" / "steamapps" / "common" / "Arma Reforger" / "ArmaReforgerServer",
            Path.home() / ".local" / "share" / "Steam" / "steamapps" / "common" / "Arma Reforger" / "ArmaReforgerServer",
            Path("C:\\Program Files (x86)\\Steam\\steamapps\\common\\Arma Reforger\\ArmaReforgerServer.exe"),
        )
        for candidate in common_paths:
            if candidate.exists():
                return candidate.resolve()

        raise ArmaServerNotFoundError(
            "ArmaReforgerServer executable not found on PATH or in common install locations. "
            "Provide the full path via the `executable` argument."
        )

    def _push(self, flag: str, *values: str | int) -> ArmaReforgerServer:
        """Append a launch flag and its values, returning self."""
        self._params.append(flag)
        for value in values:
            self._params.append(str(value))
        return self

    def _build_argv(self) -> list[str]:
        """Return the full argument vector."""
        return [str(self._executable), *self._params]

    # -- Fluent parameter setters ---------------------------------------

    def config(self, path: str | Path) -> ArmaReforgerServer:
        """Path to a server configuration JSON file."""
        return self._push(self.CONFIG_FILE, str(Path(path).resolve()))

    def profile(self, path: str | Path) -> ArmaReforgerServer:
        """Directory for profiles (saves, logs, settings).

        The directory is created automatically if it does not exist.
        """
        target = Path(path)
        target.mkdir(parents=True, exist_ok=True)
        return self._push(self.PROFILE_DIR, str(target.resolve()))

    def logs_dir(self, path: str | Path) -> ArmaReforgerServer:
        """Redirect log output to the given directory."""
        target = Path(path)
        target.mkdir(parents=True, exist_ok=True)
        return self._push(self.LOGS_DIR, str(target.resolve()))

    def bind(
        self,
        *,
        address: str | None = None,
        game_port: int | None = None,
        steam_port: int | None = None,
    ) -> ArmaReforgerServer:
        """Bind the server to specific addresses / ports.

        Keyword Args:
            address: IP address to bind (sets ``-bindIP``).
            game_port: Game UDP port (sets ``-gamePort``).
            steam_port: Steam query UDP port (sets ``-steamPort``).
        """
        if address:
            self._push(self.BIND_IP, address)
        if game_port is not None:
            self._push(self.GAME_PORT, game_port)
        if steam_port is not None:
            self._push(self.STEAM_PORT, steam_port)
        return self

    def a2s(
        self,
        *,
        address: str | None = None,
        query_port: int | None = None,
    ) -> ArmaReforgerServer:
        """Configure A2S query endpoint.

        Keyword Args:
            address: IP address for A2S queries (sets ``-a2s``).
            query_port: UDP port for A2S queries (sets ``-a2sPort``).
        """
        if address:
            self._push(self.A2S_ADDRESS, address)
        if query_port is not None:
            self._push(self.A2S_PORT, query_port)
        return self

    def rcon(
        self,
        *,
        address: str | None = None,
        port: int | None = None,
        password: str | None = None,
    ) -> ArmaReforgerServer:
        """Configure BattlEye / RCON remote console.

        Keyword Args:
            address: IP address for RCON (sets ``-rcon``).
            port: TCP port for RCON (sets ``-rconPort``).
            password: RCON password (sets ``-rconPassword``).
        """
        if address:
            self._push(self.RCON_HOST, address)
        if port is not None:
            self._push(self.RCON_PORT, port)
        if password is not None:
            self._push(self.RCON_PASSWORD, password)
        return self

    def limit_fps(self, fps: int) -> ArmaReforgerServer:
        """Cap the server frame rate."""
        return self._push(self.LIMIT_FPS, fps)

    def addon(self, mod_id: str) -> ArmaReforgerServer:
        """Load a server-side addon (mod) by ID.

        May be called multiple times to load several mods.
        """
        return self._push(self.ADDON, mod_id)

    def addons(self, *mod_ids: str) -> ArmaReforgerServer:
        """Load multiple addons at once.

        Args:
            mod_ids: Variable-length list of Steam Workshop / mod IDs.
        """
        for mod_id in mod_ids:
            self.addon(mod_id)
        return self

    def scenario(self, scenario_id: str) -> ArmaReforgerServer:
        """ID of the scenario to host."""
        return self._push(self.SCENARIO, scenario_id)

    def auto_reload(self, enabled: bool = True) -> ArmaReforgerServer:
        """Auto-restart the server when it crashes (default: ``True``)."""
        if enabled:
            self._params.append(self.AUTO_RELOAD)
        return self

    def server_id(self, server_id: str) -> ArmaReforgerServer:
        """Unique server identifier."""
        return self._push(self.SERVER_ID, server_id)

    def region(self, region: str) -> ArmaReforgerServer:
        """Server region tag (used by the server browser)."""
        return self._push(self.SERVER_REGION, region)

    def load_session_save(self, path: str | Path) -> ArmaReforgerServer:
        """Path to a session save to load on startup."""
        return self._push(self.LOAD_SESSION_SAVE, str(Path(path).resolve()))

    def force_session_load(self, enabled: bool = True) -> ArmaReforgerServer:
        """Force loading a session save even if version mismatched."""
        if enabled:
            self._params.append(self.FORCE_SESSION_LOAD)
        return self

    def custom(self, flag: str, *values: str | int) -> ArmaReforgerServer:
        """Append an arbitrary launch flag and values.

        Useful for undocumented or future parameters.

        Args:
            flag: The flag name (e.g. ``"-myFlag"``).
            values: Flag values.
        """
        return self._push(flag, *values)

    # -- SteamCmd helpers -----------------------------------------------

    @classmethod
    def install(
        cls,
        install_dir: str | Path,
        *,
        steamcmd: SteamCmd | None = None,
        validate: bool = False,
    ) -> SteamCmdResult:
        """Install the Arma Reforger dedicated server via SteamCMD.

        Args:
            install_dir: Target installation directory.
            steamcmd: Custom :class:`SteamCmd` instance.  A default one is
                created if omitted.
            validate: Verify file integrity after installation.

        Returns:
            The :class:`SteamCmdResult` from the install operation.
        """
        sc = steamcmd or SteamCmd()
        return (
            sc.login_anonymous()
            .force_install_dir(install_dir)
            .app_update(STEAM_APP_ID, validate=validate)
            .run()
        )

    @classmethod
    def update(
        cls,
        install_dir: str | Path,
        *,
        steamcmd: SteamCmd | None = None,
        validate: bool = True,
    ) -> SteamCmdResult:
        """Update the server installation via SteamCMD.

        Args:
            install_dir: Existing server installation directory.
            steamcmd: Custom :class:`SteamCmd` instance.
            validate: Verify file integrity (recommended for updates).

        Returns:
            The :class:`SteamCmdResult` from the update operation.
        """
        return cls.install(install_dir, steamcmd=steamcmd, validate=validate)

    # -- Execution ------------------------------------------------------

    def run(
        self,
        *,
        capture_output: bool = True,
        timeout: float | None = None,
        text: bool = True,
    ) -> ArmaServerResult:
        """Start the dedicated server.

        Keyword Args:
            capture_output: Capture stdout / stderr instead of inheriting
                the parent's file descriptors.
            timeout: Maximum runtime in seconds.  ``None`` disables the timeout.
                Note that a dedicated server normally runs indefinitely;
                this is primarily useful for short-lived test scenarios.
            text: Decode stdout / stderr as text (default ``True``).

        Returns:
            The execution result.  For a normal long-running server this will
            only return once the process exits.

        Raises:
            ArmaServerExitError: Runtime error during server startup.
            ArmaServerError: Subprocess-level failures (timeout, etc.).
        """
        argv = self._build_argv()
        logger.info("Starting Arma Reforger server: %s", " ".join(argv))

        kwargs: dict[str, Any] = {
            "cwd": self._cwd,
            "env": self._env,
            "text": text,
        }
        if capture_output:
            kwargs["stdout"] = subprocess.PIPE
            kwargs["stderr"] = subprocess.PIPE

        try:
            proc = subprocess.run(argv, timeout=timeout, **kwargs)
        except subprocess.TimeoutExpired as exc:
            raise ArmaServerError(
                f"Arma Reforger server timed out after {timeout} seconds: "
                f"{' '.join(argv)}"
            ) from exc
        except FileNotFoundError as exc:
            raise ArmaServerNotFoundError(
                f"Arma Reforger server executable disappeared: {self._executable}"
            ) from exc
        except OSError as exc:
            raise ArmaServerError(
                f"Failed to execute Arma Reforger server: {exc}"
            ) from exc

        stdout = proc.stdout if isinstance(proc.stdout, str) else ""
        stderr = proc.stderr if isinstance(proc.stderr, str) else ""

        result = ArmaServerResult(
            returncode=proc.returncode,
            stdout=stdout,
            stderr=stderr,
            command=argv,
        )

        if result.returncode != 0:
            logger.error(
                "Arma Reforger server exited with code %d\n"
                "stdout: %s\nstderr: %s",
                result.returncode,
                stdout[:2000],
                stderr[:2000],
            )
        else:
            logger.info("Arma Reforger server process ended (code %d)", result.returncode)

        return result

    def stream(
        self,
        *,
        timeout: float | None = None,
        text: bool = True,
    ) -> Iterator[str]:
        """Start the server and yield output lines as they are produced.

        Keyword Args:
            timeout: Maximum runtime in seconds.
            text: Decode output as text.

        Yields:
            Lines from the process stdout.

        Raises:
            ArmaServerExitError: If the process exits with a non-zero code.
        """
        argv = self._build_argv()
        logger.info("Streaming Arma Reforger server: %s", " ".join(argv))

        try:
            with subprocess.Popen(
                argv,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                cwd=self._cwd,
                env=self._env,
                text=text,
            ) as proc:
                if proc.stdout is None:
                    raise ArmaServerError(
                        "Failed to open stdout pipe for Arma Reforger server"
                    )

                for line in proc.stdout:
                    yield line.rstrip("\n\r")

                proc.wait(timeout=timeout)
                if proc.returncode != 0:
                    raise ArmaServerExitError(
                        proc.returncode,
                        "",
                        "",
                        argv,
                    )
        except subprocess.TimeoutExpired as exc:
            raise ArmaServerError(
                f"Arma Reforger server stream timed out after {timeout} seconds"
            ) from exc
        except FileNotFoundError as exc:
            raise ArmaServerNotFoundError(
                f"Arma Reforger server executable disappeared: {self._executable}"
            ) from exc

    def start(self) -> ArmaServerResult:
        """Convenience alias for :meth:`run` with ``capture_output=False``.

        Use this when running the server directly in an interactive or Docker
        context where you want stdout/stderr wired to the terminal.
        """
        return self.run(capture_output=False)

    # -- Dunder support -------------------------------------------------

    def __enter__(self) -> ArmaReforgerServer:
        return self

    def __exit__(self, *exc: object) -> None:
        pass

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__qualname__}("
            f"executable={self._executable!r}, "
            f"params={self._params!r})"
        )
