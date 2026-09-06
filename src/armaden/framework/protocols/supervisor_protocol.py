from enum import Enum
from typing import Protocol

from armaden.framework.protocols.scheduler_protocol import SchedulerProtocol
from armaden.framework.protocols.task_protocol import TaskProtocol
from armaden.framework.types.result import Result
from armaden.framework.types.schedule import ScheduleCallback


class SupervisorProtocol[G](Protocol):
    async def dispatch_scheduled(
        self,
        name: str,
        callback: ScheduleCallback,
        options: object,
    ) -> Result[object]: ...

    async def dispatch_task(
        self,
        task: TaskProtocol[Enum],
        run_in_background: bool = False,
    ) -> Result[object]: ...

    async def enqueue_request(self, request: object) -> Result[None]: ...

    async def execute_graph(self, graph: G) -> None: ...

    async def initialize(self) -> Result[None]: ...

    def ensure_scheduler(self) -> SchedulerProtocol: ...

    async def run(self) -> Result[None]: ...

    def submit(self, tasks: list[TaskProtocol[Enum]]) -> G: ...
