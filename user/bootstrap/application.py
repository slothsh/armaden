import logging
from typing import override

from returns.result import Success

from armaden.framework.api.application import Application as ApplicationBase
from armaden.framework.types.result import Result


class Application(ApplicationBase):
    @override
    def route_groups(self) -> dict[str, dict[str, object]]:
        return {
            'api': {'prefix': '/api'},
        }

    @override
    def boot(self) -> Result[None]:
        return Success(None)


logger = logging.getLogger(__name__)
