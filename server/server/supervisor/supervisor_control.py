"""FastAPI-based HTTP control API for the Arma Reforger server supervisor.

Provides runtime endpoints for interacting with the Arma Reforger server and BattlEye RCON (remote console).

Typical usage::

    from . import SupervisorControl
    ctrl = SupervisorControl(
        supervisor=server,
        bind="127.0.0.1",
        port=8888,
        rcon_host="127.0.0.1",
        rcon_port=2302,
        rcon_password="secret",
    )
    ctrl.start()
"""

import logging
import threading
import uvicorn

from server.api import ApiServer
from server.lib import QueueableSupervisor
from server.arma.reforger import ArmaReforgerRconClient

logger = logging.getLogger("supervisor.control")

class SupervisorControl:
    """Runs a FastAPI application via uvicorn in a background daemon thread."""

    def __init__(
        self,
        supervisor: QueueableSupervisor,
        bind: str,
        port: int,
        rcon_host: str,
        rcon_port: int,
        rcon_password: str,
    ) -> None:
        self.supervisor = supervisor
        self.bind = bind
        self.port = port
        self._rcon = ArmaReforgerRconClient(
            host=rcon_host,
            port=rcon_port,
            password=rcon_password,
        )
        self._app = ApiServer()
        self._server: uvicorn.Server | None = None
        self._thread: threading.Thread | None = None

    def start(self) -> None:
        """Start the uvicorn server in a background daemon thread."""
        config = uvicorn.Config(
            self._app.app,
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
