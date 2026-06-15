from returns.result import Success

from server.arma.reforger.arma_reforger_server import ArmaReforgerServer
from server.facades.app import app
from server.lib.service import Service
from server.lib.types import Result


class ArmaReforgerService(Service):
    def __call__(self) -> Result[None]:
        app().supervisor.with_server(
            ArmaReforgerServer()
                .with_supervisor(app().supervisor)
                .build()
        )

        return Success(None)
