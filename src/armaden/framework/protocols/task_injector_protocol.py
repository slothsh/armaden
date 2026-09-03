from __future__ import annotations

from enum import Enum
from typing import Protocol

from armaden.framework.protocols.task_protocol import TaskProtocol
from armaden.framework.protocols.task_runtime_protocol import TaskRuntimeProtocol


class TaskInjectorProtocol[G](Protocol):
    async def resolve(
        self,
        task: TaskProtocol[Enum],
        method: object,
        graph: G,
        runtime: TaskRuntimeProtocol,
    ) -> dict[str, object]: ...
