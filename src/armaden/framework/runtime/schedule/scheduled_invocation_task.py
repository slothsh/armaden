from __future__ import annotations

import inspect
from collections.abc import Awaitable
from typing import cast, override

from returns.result import Failure, Success

from armaden.framework.runtime.schedule.dto.schedule_execution_options_data import (
    ScheduleExecutionOptionsData,
)
from armaden.framework.runtime.supervisor.task.dto.task_policy_data import TaskPolicyData
from armaden.framework.runtime.supervisor.task.enums.task_threading_policy import (
    TaskThreadingPolicy,
)
from armaden.framework.runtime.supervisor.task.task import Task
from armaden.framework.protocols.task_runtime_protocol import TaskRuntimeProtocol
from armaden.framework.types.result import Result
from armaden.framework.types.schedule import ScheduleCallback


class ScheduledInvocationTask(Task):
    def __init__(
        self,
        name: str,
        callback: ScheduleCallback,
        options: ScheduleExecutionOptionsData,
    ) -> None:
        queue = options.queue
        priority = queue.priority if queue is not None else 0
        threading_policy = (
            TaskThreadingPolicy.EXCLUSIVE
            if options.worker_mode.value == 'exclusive'
            else TaskThreadingPolicy.SHARED
        )
        super().__init__(
            name=name,
            policy=TaskPolicyData(priority=priority),
            threading_policy=threading_policy,
        )
        self._callback: ScheduleCallback = callback


    @override
    async def run(
        self,
        runtime: TaskRuntimeProtocol,
        **kwargs: object,
    ) -> Result[object]:
        _ = runtime
        _ = kwargs
        result = self._callback()
        if inspect.isawaitable(result):
            result = await cast(Awaitable[object], result)
        if isinstance(result, (Failure, Success)):
            return cast(Result[object], result)
        return Success(result)
