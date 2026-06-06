"""FastAPI-based HTTP control API for the Arma Reforger server supervisor.

Provides runtime endpoints for health checks, status, process control
(start / shutdown / restart / load-config), and BattlEye RCON commands.

Typical usage::

    from . import ControlServer
    ctrl = ControlServer(
        supervisor=server,
        bind="127.0.0.1",
        port=8888,
        rcon_host="127.0.0.1",
        rcon_port=2302,
        rcon_password="secret",
    )
    ctrl.start()

Endpoints
~~~~~~~~~

Lifecycle
    ``GET /health``
    ``GET /status``
    ``POST /start``
    ``POST /shutdown``
    ``POST /restart``
    ``POST /load-config``

RCON
    ``GET /rcon/players``
    ``GET /rcon/bans``
    ``GET /rcon/missions``
    ``GET /rcon/users``
    ``POST /rcon/say``
    ``POST /rcon/kick``
    ``POST /rcon/ban``
    ``POST /rcon/add-ban``
    ``POST /rcon/remove-ban``
    ``POST /rcon/load-bans``
    ``POST /rcon/write-bans``
    ``POST /rcon/lock``
    ``POST /rcon/unlock``
    ``POST /rcon/restart``
    ``POST /rcon/shutdown``
    ``POST /rcon/restart-server``
    ``POST /rcon/reassign``
    ``POST /rcon/load-mission``
    ``POST /rcon/server-admin``
    ``POST /rcon/command``
"""

from __future__ import annotations

import json
import logging
import threading
from contextlib import asynccontextmanager
from datetime import datetime
from pathlib import Path
from typing import Any, Protocol

from fastapi import Body, FastAPI, HTTPException, Request
from pydantic import BaseModel
import uvicorn

from server.rcon import ArmaReforgerRcon, Player, RconConnectionError, RconError

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


# ------------------------------------------------------------------
# Rcon helpers
# ------------------------------------------------------------------


async def _ensure_rcon(request: Request) -> ArmaReforgerRcon:
    """Return the shared RCON client, connecting on first use."""
    rcon: ArmaReforgerRcon = request.app.state.rcon
    if not rcon.is_connected:
        try:
            await rcon.connect()
        except RconConnectionError as exc:
            raise HTTPException(status_code=503, detail=str(exc))
    return rcon


async def _rcon_response(cmd_coro: Any) -> dict[str, Any]:
    """Execute an RCON command and wrap the result."""
    try:
        response = await cmd_coro
    except RconError as exc:
        raise HTTPException(status_code=502, detail=str(exc))
    return {"status": "ok", "response": response}


# ------------------------------------------------------------------
# Request models
# ------------------------------------------------------------------


class _SayPayload(BaseModel):
    message: str


class _KickPayload(BaseModel):
    player_id: str | int
    reason: str | None = None


class _BanPayload(BaseModel):
    player_id: str | int
    duration: str | None = None
    reason: str | None = None


class _AddBanPayload(BaseModel):
    guid_or_ip: str
    duration: str | None = None
    reason: str | None = None


class _RemoveBanPayload(BaseModel):
    ban_id: str


class _LoadMissionPayload(BaseModel):
    name: str
    difficulty: str | None = None


class _ServerAdminPayload(BaseModel):
    cmd: str


class _CommandPayload(BaseModel):
    cmd: str


# ------------------------------------------------------------------
# App factory
# ------------------------------------------------------------------


def _make_app(
    supervisor: _SupervisorLike,
    rcon: ArmaReforgerRcon,
) -> FastAPI:
    @asynccontextmanager
    async def _lifespan(app: FastAPI):
        yield
        if rcon.is_connected:
            await rcon.disconnect()

    app = FastAPI(
        title="Arma Reforger Server Control API",
        docs_url=None,
        redoc_url=None,
        lifespan=_lifespan,
    )
    app.state.supervisor = supervisor
    app.state.rcon = rcon

    # -- Lifecycle --------------------------------------------------

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
            raise HTTPException(status_code=409, detail="Server is already running")
        sv.trigger_start()
        return {"status": "accepted", "action": "start"}

    @app.post("/shutdown")
    def shutdown(request: Request) -> dict[str, Any]:
        sv = request.app.state.supervisor
        if not sv._running.is_set():
            raise HTTPException(status_code=409, detail="Server is not running")
        sv.trigger_shutdown()
        return {"status": "accepted", "action": "shutdown"}

    @app.post("/restart")
    def restart(request: Request) -> dict[str, Any]:
        sv = request.app.state.supervisor
        sv.trigger_restart()
        return {"status": "accepted", "action": "restart"}

    @app.post("/load-config")
    def load_config(request: Request, payload: Any = Body(...)) -> dict[str, Any]:
        if not isinstance(payload, dict) or not payload:
            raise HTTPException(
                status_code=400, detail="config must be a non-empty JSON object"
            )

        sv = request.app.state.supervisor
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        config_path = Path(sv.configs_dir) / f"server_{timestamp}.json"
        config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(config_path, "w") as fh:
            json.dump(payload, fh, indent=2)

        logger.info("Config saved to %s — triggering reload", config_path)
        sv.trigger_reload(str(config_path))

        return {"status": "accepted", "config_path": str(config_path)}

    # -- RCON -------------------------------------------------------

    @app.get("/rcon/players")
    async def rcon_players(request: Request) -> dict[str, Any]:
        rcon = await _ensure_rcon(request)
        try:
            players = await rcon.players()
        except RconError as exc:
            raise HTTPException(status_code=502, detail=str(exc))
        return {
            "status": "ok",
            "response": [
                {"slot": p.slot, "uid": p.uid, "name": p.name} for p in players
            ],
        }

    @app.get("/rcon/bans")
    async def rcon_bans(request: Request) -> dict[str, Any]:
        return await _rcon_response((await _ensure_rcon(request)).bans())

    @app.get("/rcon/missions")
    async def rcon_missions(request: Request) -> dict[str, Any]:
        return await _rcon_response((await _ensure_rcon(request)).missions())

    @app.get("/rcon/users")
    async def rcon_users(request: Request) -> dict[str, Any]:
        return await _rcon_response((await _ensure_rcon(request)).users())

    @app.post("/rcon/say")
    async def rcon_say(
        request: Request, payload: _SayPayload
    ) -> dict[str, Any]:
        return await _rcon_response(
            (await _ensure_rcon(request)).say(payload.message)
        )

    @app.post("/rcon/kick")
    async def rcon_kick(
        request: Request, payload: _KickPayload
    ) -> dict[str, Any]:
        return await _rcon_response(
            (await _ensure_rcon(request)).kick(payload.player_id, payload.reason)
        )

    @app.post("/rcon/ban")
    async def rcon_ban(
        request: Request, payload: _BanPayload
    ) -> dict[str, Any]:
        return await _rcon_response(
            (await _ensure_rcon(request)).ban(
                payload.player_id, payload.duration, payload.reason
            )
        )

    @app.post("/rcon/add-ban")
    async def rcon_add_ban(
        request: Request, payload: _AddBanPayload
    ) -> dict[str, Any]:
        return await _rcon_response(
            (await _ensure_rcon(request)).add_ban(
                payload.guid_or_ip, payload.duration, payload.reason
            )
        )

    @app.post("/rcon/remove-ban")
    async def rcon_remove_ban(
        request: Request, payload: _RemoveBanPayload
    ) -> dict[str, Any]:
        return await _rcon_response(
            (await _ensure_rcon(request)).remove_ban(payload.ban_id)
        )

    @app.post("/rcon/load-bans")
    async def rcon_load_bans(request: Request) -> dict[str, Any]:
        return await _rcon_response((await _ensure_rcon(request)).load_bans())

    @app.post("/rcon/write-bans")
    async def rcon_write_bans(request: Request) -> dict[str, Any]:
        return await _rcon_response((await _ensure_rcon(request)).write_bans())

    @app.post("/rcon/lock")
    async def rcon_lock(request: Request) -> dict[str, Any]:
        return await _rcon_response((await _ensure_rcon(request)).lock())

    @app.post("/rcon/unlock")
    async def rcon_unlock(request: Request) -> dict[str, Any]:
        return await _rcon_response((await _ensure_rcon(request)).unlock())

    @app.post("/rcon/restart")
    async def rcon_restart(request: Request) -> dict[str, Any]:
        return await _rcon_response((await _ensure_rcon(request)).restart())

    @app.post("/rcon/shutdown")
    async def rcon_shutdown(request: Request) -> dict[str, Any]:
        return await _rcon_response((await _ensure_rcon(request)).shutdown())

    @app.post("/rcon/restart-server")
    async def rcon_restart_server(request: Request) -> dict[str, Any]:
        return await _rcon_response((await _ensure_rcon(request)).restart_server())

    @app.post("/rcon/reassign")
    async def rcon_reassign(request: Request) -> dict[str, Any]:
        return await _rcon_response((await _ensure_rcon(request)).reassign())

    @app.post("/rcon/load-mission")
    async def rcon_load_mission(
        request: Request, payload: _LoadMissionPayload
    ) -> dict[str, Any]:
        return await _rcon_response(
            (await _ensure_rcon(request)).load_mission(
                payload.name, payload.difficulty
            )
        )

    @app.post("/rcon/server-admin")
    async def rcon_server_admin(
        request: Request, payload: _ServerAdminPayload
    ) -> dict[str, Any]:
        return await _rcon_response(
            (await _ensure_rcon(request)).server_admin(payload.cmd)
        )

    @app.post("/rcon/command")
    async def rcon_command(
        request: Request, payload: _CommandPayload
    ) -> dict[str, Any]:
        return await _rcon_response(
            (await _ensure_rcon(request)).command(payload.cmd)
        )

    return app


class ControlServer:
    """Runs a FastAPI application via uvicorn in a background daemon thread."""

    def __init__(
        self,
        supervisor: _SupervisorLike,
        bind: str,
        port: int,
        rcon_host: str,
        rcon_port: int,
        rcon_password: str,
    ) -> None:
        self.supervisor = supervisor
        self.bind = bind
        self.port = port
        self._rcon = ArmaReforgerRcon(
            host=rcon_host,
            port=rcon_port,
            password=rcon_password,
        )
        self._app = _make_app(supervisor, self._rcon)
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
