"""Server orchestration for the Arma Reforger dedicated server.

Encapsulates provisioning, configuration, signal handling, and
process supervision in a single :class:`Server` object.
"""

from __future__ import annotations

import logging
import os
import signal
import subprocess
import sys
import threading
from pathlib import Path
from typing import Any

from server.arma import ArmaReforgerServer
from server.steamcmd import SteamCmd, SteamCmdError

logger = logging.getLogger("server")


def _int_env(name: str) -> int | None:
    val = os.environ.get(name)
    return int(val) if val is not None else None


def _list_env(name: str) -> list[str] | None:
    val = os.environ.get(name)
    if not val:
        return None
    return [item.strip() for item in val.split(",") if item.strip()]


class Server:
    """Orchestrates the full lifecycle of an Arma Reforger dedicated server.

    Typically instantiated via :meth:`from_env` and driven with :meth:`run`::

        from server.supervisor import Server

        sys.exit(Server.from_env().run())
    """

    def __init__(
        self,
        *,
        arma_install_dir: str | Path = "/arma",
        arma_executable: str | Path | None = None,
        steamcmd_executable: str | Path | None = None,
        update_on_start: bool = False,
        config: str | Path | None = None,
        configs_dir: str | Path = "/arma/configs",
        profile: str | Path = "/arma/profile",
        logs_dir: str | Path = "/arma/logs",
        bind_address: str | None = None,
        game_port: int | None = None,
        steam_port: int | None = None,
        a2s_address: str | None = None,
        a2s_port: int | None = None,
        rcon_address: str | None = None,
        rcon_port: int | None = None,
        rcon_password: str | None = None,
        limit_fps: int | None = None,
        scenario: str | None = None,
        addons: list[str] | None = None,
        auto_reload: bool = True,
        server_id: str | None = None,
        region: str | None = None,
        load_session_save: str | Path | None = None,
        force_session_load: bool = False,
    ) -> None:
        self.arma_install_dir = Path(arma_install_dir)
        self.arma_executable = Path(
            arma_executable or self.arma_install_dir / "ArmaReforgerServer"
        )
        self.steamcmd_executable = steamcmd_executable
        self.update_on_start = update_on_start
        self.config = config
        self.configs_dir = Path(configs_dir)
        self.profile = Path(profile)
        self.logs_dir = Path(logs_dir)
        self.bind_address = bind_address
        self.game_port = game_port
        self.steam_port = steam_port
        self.a2s_address = a2s_address
        self.a2s_port = a2s_port
        self.rcon_address = rcon_address
        self.rcon_port = rcon_port
        self.rcon_password = rcon_password
        self.limit_fps = limit_fps
        self.scenario = scenario
        self.addons = addons or []
        self.auto_reload = auto_reload
        self.server_id = server_id
        self.region = region
        self.load_session_save = (
            Path(load_session_save) if load_session_save else None
        )
        self.force_session_load = force_session_load

        self._proc: subprocess.Popen[Any] | None = None
        self._shutdown_requested = threading.Event()
        self._shutdown_signal: int | None = None

    # -- factories ----------------------------------------------------

    @classmethod
    def from_env(cls) -> Server:
        """Create a :class:`Server` populated from environment variables."""
        return cls(
            arma_install_dir=os.environ.get("ARMA_INSTALL_DIR", "/arma"),
            arma_executable=os.environ.get("ARMA_EXECUTABLE"),
            steamcmd_executable=os.environ.get("STEAMCMD_EXECUTABLE"),
            update_on_start=os.environ.get("ARMA_UPDATE_ON_START", "").lower()
            in ("1", "true", "yes"),
            config=os.environ.get("ARMA_CONFIG"),
            configs_dir=os.environ.get("ARMA_CONFIGS_DIR", "/arma/configs"),
            profile=os.environ.get("ARMA_PROFILE", "/arma/profile"),
            logs_dir=os.environ.get("ARMA_LOGS_DIR", "/arma/logs"),
            bind_address=os.environ.get("ARMA_BIND_ADDRESS"),
            game_port=_int_env("ARMA_GAME_PORT"),
            steam_port=_int_env("ARMA_STEAM_PORT"),
            a2s_address=os.environ.get("ARMA_A2S_ADDRESS"),
            a2s_port=_int_env("ARMA_A2S_PORT"),
            rcon_address=os.environ.get("ARMA_RCON_ADDRESS"),
            rcon_port=_int_env("ARMA_RCON_PORT"),
            rcon_password=os.environ.get("ARMA_RCON_PASSWORD"),
            limit_fps=_int_env("ARMA_LIMIT_FPS"),
            scenario=os.environ.get("ARMA_SCENARIO"),
            addons=_list_env("ARMA_ADDONS"),
            auto_reload=os.environ.get("ARMA_AUTO_RELOAD", "true").lower()
            not in ("false", "0", "no"),
            server_id=os.environ.get("ARMA_SERVER_ID"),
            region=os.environ.get("ARMA_REGION"),
            load_session_save=os.environ.get("ARMA_LOAD_SESSION_SAVE"),
            force_session_load=os.environ.get(
                "ARMA_FORCE_SESSION_LOAD", "false"
            ).lower()
            in ("true", "1", "yes"),
        )

    # -- setup --------------------------------------------------------

    def setup_logging(self) -> None:
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            stream=sys.stdout,
        )

    # -- provisioning -------------------------------------------------

    def install(self) -> None:
        """Ensure the server binary exists; install or update via SteamCMD."""
        steamcmd = (
            SteamCmd(executable=self.steamcmd_executable)
            if self.steamcmd_executable
            else None
        )

        if self.arma_executable.exists():
            logger.info("Server executable found at %s", self.arma_executable)
            if self.update_on_start:
                logger.info("ARMA_UPDATE_ON_START set — updating via SteamCMD...")
                result = ArmaReforgerServer.update(
                    install_dir=self.arma_install_dir,
                    steamcmd=steamcmd,
                    validate=True,
                )
                result.raise_for_status()
                logger.info("Update complete.")
            return

        logger.info(
            "Server executable not found at %s. Installing via SteamCMD...",
            self.arma_executable,
        )
        result = ArmaReforgerServer.install(
            install_dir=self.arma_install_dir,
            steamcmd=steamcmd,
            validate=True,
        )
        result.raise_for_status()
        logger.info("Installation complete.")

    # -- configuration ------------------------------------------------

    def build_arma_server(self) -> ArmaReforgerServer:
        """Construct an :class:`ArmaReforgerServer` from this configuration."""
        server = ArmaReforgerServer(
            executable=self.arma_executable,
            cwd=self.arma_install_dir,
        )

        server.profile(self.profile)
        server.logs_dir(self.logs_dir)

        if self.config:
            config_path = Path(self.config)
            if not config_path.is_absolute():
                config_path = self.configs_dir / config_path
            server.config(str(config_path))

        if any((self.bind_address, self.game_port, self.steam_port)):
            server.bind(
                address=self.bind_address,
                game_port=self.game_port,
                steam_port=self.steam_port,
            )

        if any((self.a2s_address, self.a2s_port)):
            server.a2s(address=self.a2s_address, query_port=self.a2s_port)

        if any((self.rcon_address, self.rcon_port, self.rcon_password)):
            server.rcon(
                address=self.rcon_address,
                port=self.rcon_port,
                password=self.rcon_password,
            )

        if self.limit_fps is not None:
            server.limit_fps(self.limit_fps)

        if self.scenario:
            server.scenario(self.scenario)

        if self.addons:
            server.addons(*self.addons)

        if self.auto_reload:
            server.auto_reload()

        if self.server_id:
            server.server_id(self.server_id)

        if self.region:
            server.region(self.region)

        if self.load_session_save:
            server.load_session_save(self.load_session_save)

        if self.force_session_load:
            server.force_session_load()

        return server

    # -- signal handling ----------------------------------------------

    def _on_sighup(self, _signum: int, _frame: Any) -> None:
        logger.info("SIGHUP received — reload requested (stubbed)")

    def _on_shutdown(self, signum: int, _frame: Any) -> None:
        signame = signal.Signals(signum).name
        logger.info(
            "%s received — forwarding to server process (PID %s)",
            signame,
            self._proc.pid if self._proc else "<none>",
        )
        self._shutdown_requested.set()
        self._shutdown_signal = signum

        if self._proc is not None and self._proc.poll() is None:
            try:
                self._proc.send_signal(signum)
                logger.info("Forwarded %s to server", signame)
            except (ProcessLookupError, OSError) as exc:
                logger.warning("Failed to forward signal: %s", exc)

    def _install_signal_handlers(self) -> None:
        signal.signal(signal.SIGHUP, self._on_sighup)
        signal.signal(signal.SIGINT, self._on_shutdown)
        signal.signal(signal.SIGQUIT, self._on_shutdown)

    # -- supervision --------------------------------------------------

    def _start_output_pump(self) -> None:
        """Pump child stdout to our own stdout in a background daemon thread.

        This prevents full-buffering issues that occur when the child
        detects stdout is a pipe rather than a TTY.
        """
        if self._proc is None or self._proc.stdout is None:
            return

        def _pump() -> None:
            try:
                for line in self._proc.stdout:
                    sys.stdout.write(line)
                    sys.stdout.flush()
            except Exception as exc:
                logger.debug("Output pump stopped: %s", exc)

        threading.Thread(target=_pump, name="stdout-pump", daemon=True).start()

    def _wait(self, grace_period: float = 30.0, poll_interval: float = 1.0) -> int:
        """Block until the server exits.

        Args:
            grace_period: Seconds to wait after a shutdown signal before
                escalating to SIGKILL.
            poll_interval: Seconds between liveness polls while running.

        Returns:
            The server process exit code.
        """
        if self._proc is None:
            raise RuntimeError("No server process registered")

        while True:
            try:
                return self._proc.wait(timeout=poll_interval)
            except subprocess.TimeoutExpired:
                if self._shutdown_requested.is_set():
                    return self._await_graceful_exit(grace_period)

    def _await_graceful_exit(self, grace_period: float) -> int:
        """Wait for the server to exit after a shutdown signal.

        Falls back to SIGKILL if the grace period expires.
        """
        signame = (
            signal.Signals(self._shutdown_signal).name
            if self._shutdown_signal
            else "shutdown"
        )
        logger.info("Awaiting graceful exit after %s...", signame)
        try:
            return self._proc.wait(timeout=grace_period)
        except subprocess.TimeoutExpired:
            logger.warning(
                "Server did not exit within %.0fs — escalating to SIGKILL",
                grace_period,
            )
            self._proc.kill()
            return self._proc.wait()

    def run(self) -> int:
        """Execute the full server lifecycle.

        Returns:
            Process exit code (``0`` for clean exit).
        """
        self.setup_logging()
        self._install_signal_handlers()

        try:
            self.install()
        except SteamCmdError as exc:
            logger.error("Server installation failed: %s", exc)
            return 1

        arma_server = self.build_arma_server()
        argv = arma_server._build_argv()
        logger.info("Launching server: %s", " ".join(argv))

        self._proc = subprocess.Popen(
            argv,
            cwd=arma_server._cwd,
            env=arma_server._env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
        )
        logger.info("Server process started (PID %d)", self._proc.pid)
        self._start_output_pump()

        try:
            return self._wait()
        except KeyboardInterrupt:
            return 130
