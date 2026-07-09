import logging

from returns.result import Success

from armaden.framework.application import Application as ApplicationBase
from armaden.framework.utils.types import Result


class Application(ApplicationBase):
    def route_groups(self) -> dict:
        return {
            'api': {'prefix': '/api'},
        }

    def boot(self) -> Result[None]:
        return Success(None)


logger = logging.getLogger(__name__)
