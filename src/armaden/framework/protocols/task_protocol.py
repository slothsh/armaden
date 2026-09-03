from enum import Enum
from typing import Protocol

from armaden.framework.protocols.task_policy_protocol import TaskPolicyProtocol
from armaden.framework.types.task import TaskCallback, TaskStatusCallback


class TaskProtocol[E: Enum](Protocol):
    @property
    def auto_restart(self) -> bool: ...

    @property
    def awaits(self) -> list[str | type[object]] | None: ...

    @property
    def depends_on(self) -> list[str | type[object]] | None: ...

    @property
    def description(self) -> str | None: ...

    @property
    def initialize(self) -> TaskCallback | None: ...

    @property
    def long_running(self) -> bool: ...

    @property
    def name(self) -> str: ...

    @property
    def policy(self) -> TaskPolicyProtocol: ...

    @property
    def run(self) -> TaskCallback: ...

    @property
    def shutdown(self) -> TaskCallback | None: ...

    @property
    def status(self) -> TaskStatusCallback | None: ...

    @property
    def threading_policy(self) -> E: ...

    _graph_ref: object | None
    _injector_ref: object | None
    _runtime_ref: object | None
