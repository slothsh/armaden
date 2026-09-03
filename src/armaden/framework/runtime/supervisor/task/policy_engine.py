from __future__ import annotations

from returns.result import Failure
from typing import override

from armaden.framework.error.error import Error
from armaden.framework.protocols.policy_engine_protocol import PolicyEngineProtocol
from armaden.framework.protocols.task_injector_protocol import TaskInjectorProtocol
from armaden.framework.runtime.supervisor.task.dto.task_graph_data import TaskGraph
from armaden.framework.protocols.task_protocol import TaskProtocol
from armaden.framework.protocols.task_runtime_protocol import (
    TaskRuntimeProtocol,
)
from armaden.framework.runtime.supervisor.task.task_runtime import TaskError
from armaden.framework.types.result import Result


class PolicyEngine(PolicyEngineProtocol[TaskGraph]):
    @override
    async def execute(
        self,
        task: TaskProtocol,
        runtime: TaskRuntimeProtocol,
        injector: TaskInjectorProtocol[TaskGraph],
        graph: TaskGraph,
    ) -> Result[object]:
        try:
            resolved = await injector.resolve(task, task.run, graph, runtime)
            _ = resolved.pop('runtime', None)
            return await task.run(runtime, **resolved)
        except Exception as exception:
            return Failure(Error(TaskError.SUBPROCESS_ERROR, details={
                'task': task.name,
                'error': str(exception),
            }))
