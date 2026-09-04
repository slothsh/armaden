from __future__ import annotations

import asyncio
from typing import cast, override

from returns.pipeline import is_successful
from returns.result import Success

from armaden.framework.protocols.application_protocol import ApplicationProtocol
from armaden.framework.runtime.application.core_application import CoreApplication
from armaden.framework.runtime.kernel.kernel import Kernel
from armaden.framework.runtime.supervisor.task.dto.task_graph_data import TaskGraphData
from armaden.framework.types.result import Result


class HttpKernel(Kernel[TaskGraphData, None]):
    def __init__(self, application: CoreApplication) -> None:
        super().__init__(application)


    @override
    def bootstrap(self) -> Result[None]:
        result = self.application.bootstrap()
        if not is_successful(result):
            return result
        user_application = cast(
            ApplicationProtocol[TaskGraphData],
            self.application.make(ApplicationProtocol),
        )
        result = user_application.boot()
        if not is_successful(result):
            return result
        return self.application.boot()


    @override
    def handle(self) -> Result[None]:
        return asyncio.run(
            self._handle_async(),
            loop_factory=lambda: self.application.event_loop,
        )


    async def _handle_async(self) -> Result[None]:
        supervisor = self.application.supervisor
        result = await supervisor.initialize()
        if not is_successful(result):
            return result
        result = await supervisor.run()
        if not is_successful(result):
            return result
        return Success(None)


    @override
    def terminate(self) -> None:
        _ = self.application.terminate()