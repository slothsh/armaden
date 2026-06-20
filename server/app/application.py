import logging
from typing import cast

from returns.result import Success

from framework.runtime.default_application import DefaultApplication

# from app.services.api_service import ApiService
# from app.services.arma_reforger_service import ArmaReforgerService
from framework.utils.types import Result

logger = logging.getLogger(__name__)


class Application(DefaultApplication):
    def __init__(self):
        super().__init__(app_handle=cast(DefaultApplication, self))


    def boot(self) -> Result[None]:
        super().boot()
        # self.services.extend([
        #     ApiService(),
        #     ArmaReforgerService(),
        # ])


        return Success(None)
