"""Main entry point for the Arma Reforger dedicated server Docker image.

The entry point performs three duties:

1. **Provision** — detect whether the server binary exists under
   ``$ARMA_INSTALL_DIR`` (default ``/arma``).  If missing, install or update
   via SteamCMD.

2. **Configure** — build the server command line from environment variables.
   Every ``ARMA_*`` variable listed below maps directly to a launch flag.

3. **Supervise** — start the server as a child process, forward its
   stdout/stderr to the container's own descriptors, and handle POSIX
   signals for graceful shutdown or reload.

Supported environment variables
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

General
    ``ARMA_INSTALL_DIR``      — Installation directory (default: ``/arma``).
    ``ARMA_UPDATE_ON_START``  — Force a SteamCMD update before launching
                                (``1``, ``true``, ``yes``).

Paths
    ``ARMA_CONFIG``           — Path to the server JSON config file.
    ``ARMA_PROFILE``          — Profile directory (saves / settings).
    ``ARMA_LOGS_DIR``         — Dedicated log output directory.

Binding
    ``ARMA_BIND_ADDRESS``     — IP address to bind (``-bindIP``).
    ``ARMA_GAME_PORT``        — Game UDP port (``-gamePort``).
    ``ARMA_STEAM_PORT``       — Steam UDP query port (``-steamPort``).

A2S query
    ``ARMA_A2S_ADDRESS``      — A2S query bind address (``-a2s``).
    ``ARMA_A2S_PORT``         — A2S query UDP port (``-a2sPort``).

RCON
    ``ARMA_RCON_ADDRESS``     — RCON bind address (``-rcon``).
    ``ARMA_RCON_PORT``        — RCON TCP port (``-rconPort``).
    ``ARMA_RCON_PASSWORD``    — RCON password (``-rconPassword``).

Gameplay
    ``ARMA_SCENARIO``         — Scenario ID to host (``-scenario``).
    ``ARMA_ADDONS``           — Comma-separated list of mod IDs (``-addon``).
    ``ARMA_LIMIT_FPS``        — Server FPS cap (``-limitFPS``).
    ``ARMA_AUTO_RELOAD``      — Auto-restart on crash (default: ``true``).
    ``ARMA_SERVER_ID``        — Unique server identifier (``-serverId``).
    ``ARMA_REGION``           — Server browser region tag (``-region``).
    ``ARMA_LOAD_SESSION_SAVE``— Path to a session save to load.
    ``ARMA_FORCE_SESSION_LOAD``— Force loading mismatched save (``false``).
"""

from __future__ import annotations

import logging
import os
import signal
import subprocess
import sys
from pathlib import Path
from typing import Any

from server.arma import ArmaReforgerServer
from server.steamcmd import SteamCmdError

ARMA_INSTALL_DIR = Path(os.environ.get("ARMA_INSTALL_DIR", "/arma"))
ARMA_EXECUTABLE = ARMA_INSTALL_DIR / "ArmaReforgerServer"

logger = logging.getLogger("server")


# ------------------------------------------------------------------
# Setup
# ------------------------------------------------------------------

def _setup_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        stream=sys.stdout,
    )


# ------------------------------------------------------------------
# Provisioning
# ------------------------------------------------------------------

def _ensure_installed() -> None:
    """Ensure the server binary exists, installing via SteamCMD if necessary."""
    if ARMA_EXECUTABLE.exists():
        logger.info("Server executable found at %s", ARMA_EXECUTABLE)
        if os.environ.get("ARMA_UPDATE_ON_START", "").lower() in (
            "1",
            "true",
            "yes",
        ):
            logger.info("ARMA_UPDATE_ON_START set — updating server via SteamCMD...")
            result = ArmaReforgerServer.update(
                install_dir=ARMA_INSTALL_DIR, validate=True
            )
            result.raise_for_status()
            logger.info("Update complete.")
        return

    logger.info(
        "Server executable not found at %s. Installing via SteamCMD...",
        ARMA_EXECUTABLE,
    )
    result = ArmaReforgerServer.install(install_dir=ARMA_INSTALL_DIR, validate=True)
    result.raise_for_status()
    logger.info("Installation complete.")


# ------------------------------------------------------------------
# Configuration
# ------------------------------------------------------------------

def _build_server() -> ArmaReforgerServer:
    """Construct an :class:`ArmaReforgerServer` from environment variables."""
    server = ArmaReforgerServer(executable=ARMA_EXECUTABLE)

    if config := os.environ.get("ARMA_CONFIG"):
        server.config(config)

    if profile := os.environ.get("ARMA_PROFILE"):
        server.profile(profile)

    if logs_dir := os.environ.get("ARMA_LOGS_DIR"):
        server.logs_dir(logs_dir)

    # -- binding ------------------------------------------------------
    bind_kwargs: dict[str, Any] = {}
    if addr := os.environ.get("ARMA_BIND_ADDRESS"):
        bind_kwargs["address"] = addr
    if port := os.environ.get("ARMA_GAME_PORT"):
        bind_kwargs["game_port"] = int(port)
    if steam_port := os.environ.get("ARMA_STEAM_PORT"):
        bind_kwargs["steam_port"] = int(steam_port)
    if bind_kwargs:
        server.bind(**bind_kwargs)

    # -- a2s ----------------------------------------------------------
    a2s_kwargs: dict[str, Any] = {}
    if addr := os.environ.get("ARMA_A2S_ADDRESS"):
        a2s_kwargs["address"] = addr
    if port := os.environ.get("ARMA_A2S_PORT"):
        a2s_kwargs["query_port"] = int(port)
    if a2s_kwargs:
        server.a2s(**a2s_kwargs)

    # -- rcon ---------------------------------------------------------
    rcon_kwargs: dict[str, Any] = {}
    if addr := os.environ.get("ARMA_RCON_ADDRESS"):
        rcon_kwargs["address"] = addr
    if port := os.environ.get("ARMA_RCON_PORT"):
        rcon_kwargs["port"] = int(port)
    if password := os.environ.get("ARMA_RCON_PASSWORD"):
        rcon_kwargs["password"] = password
    if rcon_kwargs:
        server.rcon(**rcon_kwargs)

    # -- gameplay -----------------------------------------------------
    if fps := os.environ.get("ARMA_LIMIT_FPS"):
        server.limit_fps(int(fps))

    if scenario := os.environ.get("ARMA_SCENARIO"):
        server.scenario(scenario)

    if addons_raw := os.environ.get("ARMA_ADDONS"):
        addons = [a.strip() for a in addons_raw.split(",") if a.strip()]
        if addons:
            server.addons(*addons)

    if os.environ.get("ARMA_AUTO_RELOAD", "true").lower() not in ("false", "0", "no"):
        server.auto_reload()

    if server_id := os.environ.get("ARMA_SERVER_ID"):
        server.server_id(server_id)

    if region := os.environ.get("ARMA_REGION"):
        server.region(region)

    if session_save := os.environ.get("ARMA_LOAD_SESSION_SAVE"):
        server.load_session_save(session_save)

    if os.environ.get("ARMA_FORCE_SESSION_LOAD", "false").lower() in (
        "true",
        "1",
        "yes",
    ):
        server.force_session_load()

    return server


# ------------------------------------------------------------------
# Main
# ------------------------------------------------------------------

def main() -> int:
    _setup_logging()

    # The child process handle — shared with signal handlers.
    server_proc: subprocess.Popen[Any] | None = None

    # -- signal handlers ----------------------------------------------

    def _handle_sighup(_signum: int, _frame: Any) -> None:
        logger.info("SIGHUP received — reload requested (stubbed, not yet implemented)")

    def _handle_shutdown(signum: int, _frame: Any) -> None:
        signame = signal.Signals(signum).name
        logger.info("%s received — initiating graceful shutdown", signame)

        if server_proc is not None and server_proc.poll() is None:
            logger.info(
                "Sending SIGTERM to server process (PID %d)", server_proc.pid
            )
            server_proc.terminate()
            try:
                server_proc.wait(timeout=30)
                logger.info("Server process exited cleanly")
            except subprocess.TimeoutExpired:
                logger.warning(
                    "Server did not exit within 30s — sending SIGKILL"
                )
                server_proc.kill()
                server_proc.wait()

        sys.exit(0)

    signal.signal(signal.SIGHUP, _handle_sighup)
    signal.signal(signal.SIGINT, _handle_shutdown)
    signal.signal(signal.SIGQUIT, _handle_shutdown)

    # -- provision ----------------------------------------------------

    try:
        _ensure_installed()
    except SteamCmdError as exc:
        logger.error("Server installation failed: %s", exc)
        return 1

    # -- start --------------------------------------------------------

    server = _build_server()
    argv = server._build_argv()
    logger.info("Launching server: %s", " ".join(argv))

    server_proc = subprocess.Popen(
        argv,
        cwd=server._cwd,
        env=server._env,
    )

    try:
        return_code = server_proc.wait()
    except KeyboardInterrupt:
        # SIGINT is handled above; this catches the rare edge case where
        # the signal arrives before the handler is fully wired.
        return 0

    logger.info("Server process exited with code %d", return_code)
    return return_code


if __name__ == "__main__":
    sys.exit(main())
