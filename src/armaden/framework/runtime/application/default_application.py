from typing import override

from armaden.framework.runtime.application.application import Application
from armaden.framework.types.result import Result


class DefaultApplication(Application):
    @override
    def boot(self) -> Result[None]:
        return super().boot()