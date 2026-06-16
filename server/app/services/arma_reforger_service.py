from returns.result import Success

from framework.classes.service import Service
from framework.utils.types import Result
from framework.facades import app

from games.arma_reforger import ArmaReforgerServer


class ArmaReforgerService(Service):
    name = 'arma_reforger'

    def __call__(self) -> Result[None]:
        arma_reforger_server = (
            ArmaReforgerServer()
                .build()
        )

        self.status_callbacks.extend([
            ('server', arma_reforger_server.status)
        ])

        app().supervisor.with_server(arma_reforger_server)

        return Success(None)
