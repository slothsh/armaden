import logging

from returns.result import Success

from framework.classes.default_application import DefaultApplication

from app.services.api_service import ApiService
from app.services.arma_reforger_service import ArmaReforgerService
from framework.utils.types import Result

logger = logging.getLogger(__name__)


class Application(DefaultApplication):
    def __init__(self):
        super().__init__(self)


    def boot(self) -> Result[None]:
        self.services.extend([
            ApiService(),
            ArmaReforgerService(),
        ])

        super().boot()

        return Success(None)
