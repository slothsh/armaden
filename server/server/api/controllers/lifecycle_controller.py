import json
import logging
from pathlib import Path
from datetime import datetime
from typing import Any
from fastapi import Body, HTTPException, Request
from server.api.dto.rcon_data import *

logger = logging.getLogger('api.controllers.lifecycle')

class LifecycleController:
    @classmethod
    def health(cls) -> dict[str, str]:
        return {"status": "ok"}


    @classmethod
    def status(cls, request: Request) -> dict[str, Any]:
        sv = request.app.state.supervisor
        proc = sv._proc
        running = proc is not None and proc.poll() is None
        return {
            "status": "ok",
            "server_running": running,
            "pid": proc.pid if running else None,
            "config": str(sv.config) if sv.config else None,
        }


    @classmethod
    def start(cls, request: Request) -> dict[str, Any]:
        sv = request.app.state.supervisor
        if sv._running.is_set():
            raise HTTPException(status_code=409, detail="Server is already running")
        sv.queue_start()
        return {"status": "accepted", "action": "start"}


    @classmethod
    def shutdown(cls, request: Request) -> dict[str, Any]:
        sv = request.app.state.supervisor
        if not sv._running.is_set():
            raise HTTPException(status_code=409, detail="Server is not running")
        sv.queue_shutdown()
        return {"status": "accepted", "action": "shutdown"}


    @classmethod
    def restart(cls, request: Request) -> dict[str, Any]:
        sv = request.app.state.supervisor
        sv.queue_restart()
        return {"status": "accepted", "action": "restart"}


    @classmethod
    def load_config(cls, request: Request, payload: Any = Body(...)) -> dict[str, Any]:
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
        sv.queue_reload(str(config_path))

        return {"status": "accepted", "config_path": str(config_path)}
