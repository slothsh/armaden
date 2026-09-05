from enum import Enum
from typing import Protocol

from armaden.framework.protocols.scheduler_protocol import SchedulerProtocol
from armaden.framework.protocols.task_protocol import TaskProtocol
from armaden.framework.runtime.supervisor.dto.request_info_data import SupervisorRequestData
from armaden.framework.types.result import Result


class SupervisorProtocol[G](Protocol):
    async def enqueue_request(self, request: SupervisorRequestData) -> Result[None]: ...

    async def execute_graph(self, graph: G) -> None: ...

    async def initialize(self) -> Result[None]: ...

    def ensure_scheduler(self) -> SchedulerProtocol: ...

    async def run(self) -> Result[None]: ...

    def submit(self, tasks: list[TaskProtocol[Enum]]) -> G: ...
