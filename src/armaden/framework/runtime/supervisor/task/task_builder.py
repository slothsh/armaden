from __future__ import annotations

import inspect
from dataclasses import dataclass
from typing import cast, override
from collections.abc import Awaitable

from returns.result import Success

from armaden.framework.protocols.task_builder_protocol import TaskBuilderProtocol
from armaden.framework.protocols.task_runtime_protocol import TaskRuntimeProtocol
from armaden.framework.runtime.supervisor.task.dto.task_policy_data import TaskPolicy
from armaden.framework.runtime.supervisor.task.enums.task_restart_policy import TaskRestartPolicy
from armaden.framework.runtime.supervisor.task.enums.task_threading_policy import (
    TaskThreadingPolicy,
)
from armaden.framework.runtime.supervisor.task.task import Task
from armaden.framework.types.result import Result
from armaden.framework.types.task import TaskCallback, TaskStatusCallback


type BuiltTaskCallback = TaskCallback | TaskStatusCallback


class TaskBuilder(TaskBuilderProtocol[TaskThreadingPolicy]):
    def __init__(self) -> None:
        self._awaits: list[str | type[object]] = []
        self._auto_restart: bool = False
        self._continue_on_failure: bool = False
        self._depends_on: list[str | type[object]] = []
        self._description: str | None = None
        self._initialize: TaskCallback | None = None
        self._long_running: bool = False
        self._name: str | None = None
        self._priority: int = 0
        self._ready_timeout: float | None = None
        self._restart: TaskRestartPolicy = TaskRestartPolicy.NEVER
        self._retries: int = 0
        self._retry_backoff: float = 2.0
        self._retry_delay: float = 1.0
        self._run: TaskCallback | None = None
        self._shutdown: TaskCallback | None = None
        self._status: TaskStatusCallback | None = None
        self._threading_policy: TaskThreadingPolicy = TaskThreadingPolicy.SHARED
        self._timeout: float | None = None


    def _build_policy(self) -> TaskPolicy:
        restart = self._restart
        if self._auto_restart and restart == TaskRestartPolicy.NEVER:
            restart = TaskRestartPolicy.ALWAYS
        return TaskPolicy(
            continue_on_failure=self._continue_on_failure,
            priority=self._priority,
            ready_timeout=self._ready_timeout,
            restart=restart,
            retries=self._retries,
            retry_backoff=self._retry_backoff,
            retry_delay=self._retry_delay,
            timeout=self._timeout,
        )


    @override
    def awaits(self, *references: str | type[object]) -> TaskBuilder:
        self._awaits.extend(references)
        return self


    @override
    def build(self) -> Task:
        if self._run is None:
            raise ValueError('Task run callback must be set before building')

        callbacks = _BuiltCallbacks(
            initialize=self._initialize,
            run=self._run,
            shutdown=self._shutdown,
            status=self._status,
        )
        return _BuiltTask(
            awaits=list(self._awaits),
            callbacks=callbacks,
            depends_on=list(self._depends_on),
            description=self._description,
            long_running=self._long_running,
            name=self._name,
            policy=self._build_policy(),
            threading_policy=self._threading_policy,
        )


    @override
    def continue_on_failure(self) -> TaskBuilder:
        self._continue_on_failure = True
        return self


    @override
    def depends_on(self, *references: str | type[object]) -> TaskBuilder:
        self._depends_on.extend(references)
        return self


    @override
    def description(self, value: str | None) -> TaskBuilder:
        self._description = value
        return self


    @override
    def exclusive_thread(self) -> TaskBuilder:
        self._threading_policy = TaskThreadingPolicy.EXCLUSIVE
        return self


    @override
    def long_running(self) -> TaskBuilder:
        self._long_running = True
        return self


    @override
    def name(self, value: str | None) -> TaskBuilder:
        self._name = value
        return self


    @override
    def on_initialize(self, callback: TaskCallback) -> TaskBuilder:
        self._initialize = callback
        return self


    @override
    def on_run(self, callback: TaskCallback) -> TaskBuilder:
        self._run = callback
        return self


    @override
    def on_shutdown(self, callback: TaskCallback) -> TaskBuilder:
        self._shutdown = callback
        return self


    @override
    def on_status(self, callback: TaskStatusCallback) -> TaskBuilder:
        self._status = callback
        return self


    @override
    def priority(self, value: int) -> TaskBuilder:
        self._priority = value
        return self


    @override
    def ready_timeout(self, seconds: float) -> TaskBuilder:
        self._ready_timeout = seconds
        return self


    @override
    def restart(self, policy: str) -> TaskBuilder:
        self._restart = TaskRestartPolicy(policy)
        return self


    @override
    def retries(
        self,
        count: int,
        delay: float = 1.0,
        backoff: float = 2.0,
    ) -> TaskBuilder:
        self._retries = count
        self._retry_backoff = backoff
        self._retry_delay = delay
        return self


    @override
    def shared_thread(self) -> TaskBuilder:
        self._threading_policy = TaskThreadingPolicy.SHARED
        return self


    @override
    def timeout(self, seconds: float) -> TaskBuilder:
        self._timeout = seconds
        return self


    @override
    def with_auto_restart(self) -> TaskBuilder:
        self._auto_restart = True
        return self


@dataclass
class _BuiltCallbacks:
    initialize: TaskCallback | None = None
    run: TaskCallback | None = None
    shutdown: TaskCallback | None = None
    status: TaskStatusCallback | None = None


class _BuiltTask(Task):
    def __init__(
        self,
        awaits: list[str | type[object]],
        callbacks: _BuiltCallbacks,
        depends_on: list[str | type[object]],
        description: str | None,
        long_running: bool,
        name: str | None,
        policy: TaskPolicy,
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
        self._callbacks: _BuiltCallbacks = callbacks


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
