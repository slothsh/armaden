from returns.result import Success

from armaden.framework.application import Application
from armaden.framework.utils.types import Result


class DefaultApplication(Application):
    def boot(self) -> Result[None]:
        return Success(None)
