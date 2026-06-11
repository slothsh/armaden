from __future__ import annotations

import threading
import uvicorn
import logging
from .supervisor_like import SupervisorLike
from ..arma import ArmaReforgerRcon
from ..api import make_api_app

logger = logging.getLogger("server.controller")

class SupervisorController:
    """Runs a FastAPI application via uvicorn in a background daemon thread."""

    def __init__(
        self,
        supervisor: SupervisorLike,
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
        self._app = make_api_app(supervisor, self._rcon)
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


