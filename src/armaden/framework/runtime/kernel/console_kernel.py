from __future__ import annotations

from typing import override

from returns.pipeline import is_successful
from returns.result import Success

from armaden.framework.runtime.application.core_application import CoreApplication
from armaden.framework.runtime.kernel.kernel import Kernel
from armaden.framework.runtime.supervisor.task.dto.task_graph_data import TaskGraphData
from armaden.framework.types.result import Result


class ConsoleKernel(Kernel[TaskGraphData, int]):
    def __init__(self, application: CoreApplication) -> None:
        super().__init__(application)


    def all(self) -> dict[str, object]:
        return {}


    @override
    def bootstrap(self) -> Result[None]:
        result = self.application.bootstrap()
        if not is_successful(result):
            return result
        return self.application.boot()


    def call(
        self,
        command: str,
        parameters: dict[object, object] | None = None,
    ) -> int:
        result = self.handle(command, parameters)
        return 0 if is_successful(result) else 1


    @override
    def handle(
        self,
        command: str | None = None,
        parameters: dict[object, object] | None = None,
    ) -> Result[int]:
        _ = command
        _ = parameters
        return Success(0)


    def output(self) -> str:
        return ''


    @override
    def terminate(self, status: int = 0) -> None:
        _ = status
        _ = self.application.terminate()