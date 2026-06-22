from returns.result import Success

from framework.application import Application
from framework.facades import app
from framework.utils.types import Result
from .services.default_api_service import DefaultApiService


class DefaultApplication(Application):
    def boot(self) -> Result[None]:
        self.service_manager.register_services([DefaultApiService()])
        return Success(None)
