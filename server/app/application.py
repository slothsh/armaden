import logging

from returns.result import Success

from framework.application import Application as ApplicationBase
from framework.classes.service import Service
from framework.facades import app
from framework.utils.types import Result
from games.arma_reforger.arma_reforger_server import ArmaReforgerServer


class ArmaReforgerService(Service):
    name = 'arma reforger'

    def __init__(self):
        super().__init__()
        self._server: ArmaReforgerServer | None = None

    def __call__(self) -> Result[None]:
        self._server = ArmaReforgerServer()
        app().supervisor.with_server(self._server)
        return Success(None)


class Application(ApplicationBase):
    def boot(self) -> Result[None]:
        self.service_manager.register_services([ArmaReforgerService()])
        return Success(None)


logger = logging.getLogger(__name__)
