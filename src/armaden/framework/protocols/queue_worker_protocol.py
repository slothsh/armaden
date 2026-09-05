from typing import Protocol

from armaden.framework.protocols.task_runtime_protocol import TaskRuntimeProtocol
from armaden.framework.types.result import Result


class QueueWorkerProtocol(Protocol):
    async def run(self, runtime: TaskRuntimeProtocol) -> Result[None]: ...

    async def shutdown(self, runtime: TaskRuntimeProtocol) -> Result[None]: ...
