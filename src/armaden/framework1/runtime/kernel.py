import asyncio
from abc import ABC, abstractmethod
from typing import Any

from returns.pipeline import is_successful
from returns.result import Success

from armaden.framework.protocols.application import ApplicationInterface
from armaden.framework.utils.types import Result as TypedResult

from armaden.framework.runtime.application import CoreApplication


class Kernel(ABC):
    def __init__(self, app: CoreApplication) -> None:
        self._app = app

    @property
    def application(self) -> CoreApplication:
        return self._app

    @abstractmethod
    def bootstrap(self) -> TypedResult[None]: ...

    @abstractmethod
    def handle(self, *args: Any, **kwargs: Any) -> TypedResult[Any]: ...

    @abstractmethod
    def terminate(self, *args: Any, **kwargs: Any) -> None: ...


class HttpKernel(Kernel):
    def bootstrap(self) -> TypedResult[None]:
        result = self._app.bootstrap()
        if not is_successful(result):
            return result

        user_app = self._app.make(ApplicationInterface)
        result = user_app.boot()
        if not is_successful(result):
            return result

        result = self._app.boot()
        if not is_successful(result):
            return result

        return Success(None)

    def handle(self) -> TypedResult[None]:
        return asyncio.run(
            self._handle_async(),
            loop_factory=lambda: self._app.make('event_loop'),
        )

    async def _handle_async(self) -> TypedResult[None]:
        supervisor = self._app.supervisor
        if not is_successful(result := await supervisor.initialize()):
            return result
        if not is_successful(result := await supervisor.run()):
            return result
        return Success(None)

    def terminate(self) -> None:
        pass


class ConsoleKernel(Kernel):
    def bootstrap(self) -> TypedResult[None]:
        result = self._app.bootstrap()
        if not is_successful(result):
            return result

        result = self._app.boot()
        if not is_successful(result):
            return result

        return Success(None)

    def handle(self, command: str | None = None, parameters: dict | None = None) -> TypedResult[int]:
        _ = command
        _ = parameters
        return Success(0)

    def terminate(self, status: int = 0) -> None:
        _ = status
        pass

    def call(self, command: str, parameters: dict | None = None) -> int:
        result = self.handle(command, parameters)
        if is_successful(result):
            return result.unwrap()
        return 1

    def all(self) -> dict:
        return {}

    def output(self) -> str:
        return ""


def bootstrap_http() -> TypedResult[None]:
    from armaden.framework.facades._registry import set_application
    application = CoreApplication()
    set_application(application)
    kernel = HttpKernel(application)
    result = kernel.bootstrap()
    if not is_successful(result):
        return result
    return kernel.handle()


def bootstrap_console() -> TypedResult[int]:
    from armaden.framework.facades._registry import set_application
    application = CoreApplication()
    set_application(application)
    kernel = ConsoleKernel(application)
    result = kernel.bootstrap()
    if not is_successful(result):
        return result.map(lambda _: 0)
    return kernel.handle()


class RuntimeEntry:
    @staticmethod
    def bootstrap() -> TypedResult[None]:
        return bootstrap_http()
