from __future__ import annotations

from enum import Enum
from typing import Protocol

from armaden.framework.protocols.task_injector_protocol import TaskInjectorProtocol
from armaden.framework.protocols.task_protocol import TaskProtocol
from armaden.framework.protocols.task_runtime_protocol import TaskRuntimeProtocol
from armaden.framework.types.result import Result


class PolicyEngineProtocol[G](Protocol):
    async def execute(
        self,
        task: TaskProtocol[Enum],
        runtime: TaskRuntimeProtocol,
        injector: TaskInjectorProtocol[G],
        graph: G,
    ) -> Result[object]: ...
