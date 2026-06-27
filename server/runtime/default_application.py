from returns.result import Success

from framework.application import Application
from framework.utils.types import Result


class DefaultApplication(Application):
    def boot(self) -> Result[None]:
        return Success(None)
