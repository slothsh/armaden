from returns.result import Success

from framework.classes.service_provider import ServiceProvider
from framework.facades import app
from framework.utils.types import Result
from games.arma_reforger.arma_reforger_server import ArmaReforgerServer


class AppServiceProvider(ServiceProvider):
    name = 'arma_reforger'

    def register(self) -> Result[None]:
        self._container.singleton(ArmaReforgerServer)
        return Success(None)

    def boot(self) -> Result[None]:
        server = self._container.make(ArmaReforgerServer)
        app().supervisor.with_server(server)
        return Success(None)
