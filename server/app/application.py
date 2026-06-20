import logging
from typing import cast

from returns.result import Success

from framework.runtime.default_application import DefaultApplication

from framework.classes.service import Service
from framework.runtime.facades.app import app
from framework.utils.types import Result
from games.arma_reforger.arma_reforger_server import ArmaReforgerServer

class ArmaReforgerService(Service):
    name = 'arma reforger'

    def __call__(self) -> Result[None]:
        self.server = ArmaReforgerServer()
        app().supervisor.with_server(self.server)
        return Success(None)


logger = logging.getLogger(__name__)


class Application(DefaultApplication):
    def __init__(self):
        super().__init__(app_handle=cast(DefaultApplication, self))


    def boot(self) -> Result[None]:
        super().boot()
        self.service_manager.register_services([
            ArmaReforgerService(),
        ])


        return Success(None)
