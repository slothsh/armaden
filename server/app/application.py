import logging

from framework.classes.default_application import DefaultApplication

from app.services.api_service import ApiService
from app.services.arma_reforger_service import ArmaReforgerService

logger = logging.getLogger(__name__)


class Application(DefaultApplication):
    def __init__(self):
        super().__init__(self)

        self.services.extend([
            ApiService(),
            ArmaReforgerService(),
        ])
