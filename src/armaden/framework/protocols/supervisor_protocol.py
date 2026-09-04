from enum import Enum
from typing import Protocol

from armaden.framework.protocols.scheduler_protocol import SchedulerProtocol
from armaden.framework.protocols.task_protocol import TaskProtocol


class SupervisorProtocol[G](Protocol):
    async def execute_graph(self, graph: G) -> None: ...

    def ensure_scheduler(self) -> SchedulerProtocol: ...

    def submit(self, tasks: list[TaskProtocol[Enum]]) -> G: ...
