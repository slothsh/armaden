import logging

from returns.result import Success

from framework.application import Application as ApplicationBase
from framework.utils.types import Result


class Application(ApplicationBase):
    def boot(self) -> Result[None]:
        return Success(None)


logger = logging.getLogger(__name__)
