from returns.result import Success
from armaden.framework.classes.service_provider import ServiceProvider
from armaden.framework.utils.types import Result


class ConsoleServiceProvider(ServiceProvider):
    name = 'console'

    def register(self) -> Result[None]:
        from armaden.framework.runtime.kernel import ConsoleKernel
        self._container.singleton(
            'kernel.console', lambda c: ConsoleKernel(c.make('app')))
        return Success(None)

    def boot(self) -> Result[None]:
        return Success(None)
