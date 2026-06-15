from returns.result import Success

from server.arma.reforger.arma_reforger_server import ArmaReforgerServer
from server.facades.app import app
from server.lib.service import Service
from server.lib.types import Result


class ArmaReforgerService(Service):
    def __init__(self):
        super().__init__()
        self._server = ArmaReforgerServer()


    def __call__(self) -> Result[None]:
        self._server = (
            self._server
            .with_supervisor(app().supervisor)
            .build()
        )

        app().supervisor.with_server(self._server)

        return Success(None)
