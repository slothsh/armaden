from returns.result import Success

from framework.application import Application
from framework.facades import app
from framework.utils.types import Result
from runtime.services.default_api_service import DefaultApiServiceProvider


class DefaultApplication(Application):
    def boot(self) -> Result[None]:
        app().register_provider(DefaultApiServiceProvider(self._container))
        return Success(None)
