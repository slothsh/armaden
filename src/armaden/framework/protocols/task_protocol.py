from enum import Enum
from typing import Protocol

from armaden.framework.protocols.task_policy_protocol import TaskPolicyProtocol
from armaden.framework.protocols.task_runtime_protocol import TaskRuntimeProtocol
from armaden.framework.types.result import Result


class TaskProtocol[E: Enum](Protocol):
    @property
    def auto_restart(self) -> bool: ...

    awaits: list[str | type[object]] | None
    depends_on: list[str | type[object]] | None
    description: str | None
    long_running: bool
    name: str
    @property
    def policy(self) -> TaskPolicyProtocol: ...

    threading_policy: E

    async def initialize(
        self,
        runtime: TaskRuntimeProtocol,
        **kwargs: object,
    ) -> Result[None]: ...

    async def run(
        self,
        runtime: TaskRuntimeProtocol,
        **kwargs: object,
    ) -> Result[object]: ...

    async def shutdown(
        self,
        runtime: TaskRuntimeProtocol,
        **kwargs: object,
    ) -> Result[None]: ...

    async def status(
        self,
        runtime: TaskRuntimeProtocol,
        **kwargs: object,
    ) -> Result[dict[str, object]]: ...
