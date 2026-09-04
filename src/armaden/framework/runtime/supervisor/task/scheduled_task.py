from __future__ import annotations

import inspect
from typing import override

from armaden.framework.protocols.task_runtime_protocol import TaskRuntimeProtocol
from armaden.framework.runtime.supervisor.task.dto.task_policy_data import TaskPolicyData
from armaden.framework.runtime.supervisor.task.task import Task
from armaden.framework.types.result import Result
from armaden.framework.types.task import TaskCallback
from returns.result import Success


class ScheduledTask(Task):
    def __init__(
        self,
        name: str,
        action: TaskCallback,
        policy: TaskPolicyData,
        depends_on: list[str | type[object]] | None = None,
        awaits: list[str | type[object]] | None = None,
    ) -> None:
        super().__init__(
            name=name,
            policy=policy,
            depends_on=depends_on,
            awaits=awaits,
        )
        self._action: TaskCallback = action


    @override
    async def run(
        self,
        runtime: TaskRuntimeProtocol,
        **kwargs: object,
    ) -> Result[object]:
        _ = runtime
        _ = kwargs
        result = self._action(self)
        if inspect.isawaitable(result):
            return await result
        return result


    @override
    async def shutdown(
        self,
        runtime: TaskRuntimeProtocol,
        **kwargs: object,
    ) -> Result[None]:
        _ = runtime
        _ = kwargs
        return Success(None)
