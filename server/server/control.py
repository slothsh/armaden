"""FastAPI-based HTTP control API for the Arma Reforger server supervisor.

Provides runtime endpoints for health checks, status, and dynamic control
of the Arma server process (start, shutdown, restart, load-config).

Typical usage::

    from server.control import ControlServer
    ctrl = ControlServer(supervisor=server, bind="127.0.0.1", port=8888)
    ctrl.start()

Endpoints
~~~~~~~~~

``GET /health``
    Quick liveness check.

``GET /status``
    Detailed runtime state (running, pid, config, etc.).

``POST /start``
    Starts the Arma server if it is currently stopped.

``POST /shutdown``
    Gracefully stops the Arma server (supervisor keeps running).

``POST /restart``
    Gracefully restarts the Arma server.

``POST /load-config``
    Accepts a JSON body (must be a non-empty object), persists a
    timestamped copy under the configured configs directory, and
    triggers a graceful server restart with the new config.
"""

from __future__ import annotations

import json
import logging
import threading
from datetime import datetime
from pathlib import Path
from typing import Any, Protocol

from fastapi import Body, FastAPI, HTTPException, Request
import uvicorn

logger = logging.getLogger("server.control")


class _SupervisorLike(Protocol):
    """Minimal interface the control API expects from the supervisor."""

    config: str | Path | None
    configs_dir: Path
    _proc: Any
    _running: threading.Event

    def trigger_start(self) -> None: ...
    def trigger_shutdown(self) -> None: ...
    def trigger_restart(self) -> None: ...
    def trigger_reload(self, config_path: str | Path) -> None: ...


def _make_app(supervisor: _SupervisorLike) -> FastAPI:
    app = FastAPI(
        title="Arma Reforger Server Control API",
        docs_url=None,
        redoc_url=None,
    )
    app.state.supervisor = supervisor

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.get("/status")
    def status(request: Request) -> dict[str, Any]:
        sv = request.app.state.supervisor
        proc = sv._proc
        running = proc is not None and proc.poll() is None
        return {
            "status": "ok",
            "server_running": running,
            "pid": proc.pid if running else None,
            "config": str(sv.config) if sv.config else None,
        }

    @app.post("/start")
    def start(request: Request) -> dict[str, Any]:
        sv = request.app.state.supervisor
        if sv._running.is_set():
            raise HTTPException(
                status_code=409,
                detail="Server is already running",
            )
        sv.trigger_start()
        return {
            "status": "accepted",
            "action": "start",
        }

    @app.post("/shutdown")
    def shutdown(request: Request) -> dict[str, Any]:
        sv = request.app.state.supervisor
        if not sv._running.is_set():
            raise HTTPException(
                status_code=409,
                detail="Server is not running",
            )
        sv.trigger_shutdown()
        return {
            "status": "accepted",
            "action": "shutdown",
        }

    @app.post("/restart")
    def restart(request: Request) -> dict[str, Any]:
        sv = request.app.state.supervisor
        sv.trigger_restart()
        return {
            "status": "accepted",
            "action": "restart",
        }

    @app.post("/load-config")
    def load_config(request: Request, payload: Any = Body(...)) -> dict[str, Any]:
        if not isinstance(payload, dict) or not payload:
            raise HTTPException(
                status_code=400,
                detail="config must be a non-empty JSON object",
            )

        sv = request.app.state.supervisor

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        config_path = Path(sv.configs_dir) / f"server_{timestamp}.json"
        config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(config_path, "w") as fh:
            json.dump(payload, fh, indent=2)

        logger.info("Config saved to %s — triggering reload", config_path)
        sv.trigger_reload(str(config_path))

        return {
            "status": "accepted",
            "config_path": str(config_path),
        }

    return app


class ControlServer:
    """Runs a FastAPI application via uvicorn in a background daemon thread."""

    def __init__(
        self,
        supervisor: _SupervisorLike,
        bind: str,
        port: int,
    ) -> None:
        self.supervisor = supervisor
        self.bind = bind
        self.port = port
        self._app = _make_app(supervisor)
        self._server: uvicorn.Server | None = None
        self._thread: threading.Thread | None = None

    def start(self) -> None:
        """Start the uvicorn server in a background daemon thread."""
        config = uvicorn.Config(
            self._app,
            host=self.bind,
            port=self.port,
            log_level="warning",
            access_log=False,
        )
        self._server = uvicorn.Server(config)

        self._thread = threading.Thread(
            target=self._server.run,
            name="control-server",
            daemon=True,
        )
        self._thread.start()
        logger.info(
            "Control server listening on http://%s:%d",
            self.bind,
            self.port,
        )

    def stop(self) -> None:
        """Signal the uvicorn server to shut down and wait for the thread."""
        if self._server is not None:
            self._server.should_exit = True
        if self._thread is not None:
            self._thread.join(timeout=5.0)
