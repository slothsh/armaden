from __future__ import annotations

import inspect
from collections.abc import Awaitable
from typing import cast, override

from returns.result import Success

from armaden.framework.protocols.task_runtime_protocol import TaskRuntimeProtocol
from armaden.framework.runtime.supervisor.task.dto.built_task_callbacks_data import (
    BuiltTaskCallbacksData,
)
from armaden.framework.runtime.supervisor.task.dto.task_policy_data import TaskPolicyData
from armaden.framework.runtime.supervisor.task.enums.task_threading_policy import (
    TaskThreadingPolicy,
)
from armaden.framework.runtime.supervisor.task.task import Task
from armaden.framework.types.result import Result
from armaden.framework.types.task import BuiltTaskCallback


class BuiltTask(Task):
    def __init__(
        self,
        awaits: list[str | type[object]],
        callbacks: BuiltTaskCallbacksData,
        depends_on: list[str | type[object]],
        description: str | None,
        long_running: bool,
        name: str | None,
        policy: TaskPolicyData,
        threading_policy: TaskThreadingPolicy,
    ) -> None:
        super().__init__(
            awaits=awaits,
            depends_on=depends_on,
            description=description,
            long_running=long_running,
            name=name,
            policy=policy,
            threading_policy=threading_policy,
        )
        self._callbacks: BuiltTaskCallbacksData = callbacks


    async def _invoke_callback(
        self,
        callback: BuiltTaskCallback,
        runtime: TaskRuntimeProtocol,
    ) -> Result[object]:
        kwargs = await self._resolve_kwargs(callback, runtime)
        result = callback(**kwargs)
        if inspect.isawaitable(result):
            return await cast(Awaitable[Result[object]], result)
        return result


    async def _resolve_kwargs(
        self,
        callback: BuiltTaskCallback,
        runtime: TaskRuntimeProtocol,
    ) -> dict[str, object]:
        graph = self.graph
        injector = self.injector
        if graph is None or injector is None:
            return {}
        return await injector.resolve(self, callback, graph, runtime)


    @override
    async def initialize(
        self,
        runtime: TaskRuntimeProtocol,
        **kwargs: object,
    ) -> Result[None]:
        _ = kwargs
        callback = self._callbacks.initialize
        if callback is None:
            return Success(None)
        result = await self._invoke_callback(callback, runtime)
        return cast(Result[None], result)


    @override
    async def run(
        self,
        runtime: TaskRuntimeProtocol,
        **kwargs: object,
    ) -> Result[object]:
        _ = kwargs
        callback = self._callbacks.run
        if callback is None:
            raise RuntimeError('Task run callback must be set before building')
        return await self._invoke_callback(callback, runtime)


    @override
    async def shutdown(
        self,
        runtime: TaskRuntimeProtocol,
        **kwargs: object,
    ) -> Result[None]:
        _ = kwargs
        callback = self._callbacks.shutdown
        if callback is None:
            return Success(None)
        result = await self._invoke_callback(callback, runtime)
        return cast(Result[None], result)


    @override
    async def status(
        self,
        runtime: TaskRuntimeProtocol,
        **kwargs: object,
    ) -> Result[dict[str, object]]:
        _ = kwargs
        callback = self._callbacks.status
        if callback is None:
            return Success({})
        result = await self._invoke_callback(callback, runtime)
        return cast(Result[dict[str, object]], result)
