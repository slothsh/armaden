from returns.pipeline import is_successful

from armaden.framework.runtime.application.core_application import CoreApplication
from armaden.framework.runtime.kernel.console_kernel import ConsoleKernel
from armaden.framework.runtime.kernel.http_kernel import HttpKernel
from armaden.framework.types.result import Result


def bootstrap_console() -> Result[int]:
    application = CoreApplication()
    kernel = ConsoleKernel(application)
    result = kernel.bootstrap()
    if not is_successful(result):
        return result.map(lambda _: 0)
    return kernel.handle()


def bootstrap_http() -> Result[None]:
    application = CoreApplication()
    kernel = HttpKernel(application)
    result = kernel.bootstrap()
    if not is_successful(result):
        return result
    return kernel.handle()


class RuntimeEntry:
    @staticmethod
    def bootstrap() -> Result[None]:
        return bootstrap_http()