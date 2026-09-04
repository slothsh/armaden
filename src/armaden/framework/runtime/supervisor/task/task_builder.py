from __future__ import annotations

from typing import override

from armaden.framework.protocols.task_builder_protocol import TaskBuilderProtocol
from armaden.framework.runtime.supervisor.task.built_task import BuiltTask
from armaden.framework.runtime.supervisor.task.dto.built_task_callbacks_data import (
    BuiltTaskCallbacksData,
)
from armaden.framework.runtime.supervisor.task.dto.task_policy_data import TaskPolicyData
from armaden.framework.runtime.supervisor.task.enums.task_restart_policy import TaskRestartPolicy
from armaden.framework.runtime.supervisor.task.enums.task_threading_policy import (
    TaskThreadingPolicy,
)
from armaden.framework.runtime.supervisor.task.task import Task
from armaden.framework.types.task import TaskCallback, TaskStatusCallback


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


    def _build_policy(self) -> TaskPolicyData:
        restart = self._restart
        if self._auto_restart and restart == TaskRestartPolicy.NEVER:
            restart = TaskRestartPolicy.ALWAYS
        return TaskPolicyData(
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

        callbacks = BuiltTaskCallbacksData(
            initialize=self._initialize,
            run=self._run,
            shutdown=self._shutdown,
            status=self._status,
        )
        return BuiltTask(
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
