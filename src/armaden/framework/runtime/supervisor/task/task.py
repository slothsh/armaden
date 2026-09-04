from __future__ import annotations

from abc import ABC, abstractmethod
from copy import copy
from typing import override

from returns.result import Success

from armaden.framework.protocols.task_injector_protocol import TaskInjectorProtocol
from armaden.framework.protocols.task_protocol import TaskProtocol
from armaden.framework.protocols.task_runtime_protocol import TaskRuntimeProtocol
from armaden.framework.runtime.supervisor.task.dto.task_graph_data import TaskGraphData
from armaden.framework.runtime.supervisor.task.dto.task_policy_data import TaskPolicyData
from armaden.framework.runtime.supervisor.task.enums.task_restart_policy import TaskRestartPolicy
from armaden.framework.runtime.supervisor.task.enums.task_threading_policy import (
    TaskThreadingPolicy,
)
from armaden.framework.types.result import Result


class Task(TaskProtocol[TaskThreadingPolicy], ABC):
    awaits: list[str | type[object]] | None = None
    depends_on: list[str | type[object]] | None = None
    description: str | None = None
    long_running: bool = False
    name: str = ''
    _policy: TaskPolicyData = TaskPolicyData()
    _threading_policy: TaskThreadingPolicy = TaskThreadingPolicy.SHARED

    def __init__(
        self,
        name: str | None = None,
        description: str | None = None,
        policy: TaskPolicyData | None = None,
        threading_policy: TaskThreadingPolicy | None = None,
        depends_on: list[str | type[object]] | None = None,
        awaits: list[str | type[object]] | None = None,
        long_running: bool | None = None,
    ) -> None:
        task_class = type(self)
        self._graph_ref: TaskGraphData | None = None
        self._injector_ref: TaskInjectorProtocol[TaskGraphData] | None = None
        self._runtime_ref: TaskRuntimeProtocol | None = None
        self.awaits = list(awaits) if awaits is not None else list(task_class.awaits or [])
        self.depends_on = (
            list(depends_on)
            if depends_on is not None
            else list(task_class.depends_on or [])
        )
        self.description = (
            description if description is not None else task_class.description
        )
        self.long_running = (
            long_running if long_running is not None else task_class.long_running
        )
        self.name = name if name is not None else (task_class.name or task_class.__name__)
        self._policy = copy(task_class._policy) if policy is None else policy
        self._threading_policy = (
            threading_policy
            if threading_policy is not None
            else task_class._threading_policy
        )


    @property
    @override
    def auto_restart(self) -> bool:
        return self.policy.restart != TaskRestartPolicy.NEVER


    @property
    def graph(self) -> TaskGraphData | None:
        return self._graph_ref


    @override
    async def initialize(
        self,
        runtime: TaskRuntimeProtocol,
        **kwargs: object,
    ) -> Result[None]:
        _ = kwargs
        _ = runtime
        return Success(None)


    @property
    def injector(self) -> TaskInjectorProtocol[TaskGraphData] | None:
        return self._injector_ref


    @property
    @override
    def policy(self) -> TaskPolicyData:
        return self._policy


    @property
    def runtime(self) -> TaskRuntimeProtocol | None:
        return self._runtime_ref


    @override
    @abstractmethod
    async def run(
        self,
        runtime: TaskRuntimeProtocol,
        **kwargs: object,
    ) -> Result[object]:
        _ = kwargs
        _ = runtime
        raise NotImplementedError


    @override
    async def shutdown(
        self,
        runtime: TaskRuntimeProtocol,
        **kwargs: object,
    ) -> Result[None]:
        _ = kwargs
        _ = runtime
        return Success(None)


    @override
    async def status(
        self,
        runtime: TaskRuntimeProtocol,
        **kwargs: object,
    ) -> Result[dict[str, object]]:
        _ = kwargs
        _ = runtime
        return Success({})


    @property
    @override
    def threading_policy(self) -> TaskThreadingPolicy:
        return self._threading_policy
