from collections.abc import Callable, Coroutine
from returns.result import Result
from typing import Any, Dict, Generic, Protocol, Self, TypeVar

from armaden.framework.protocols.error import ErrorInterface
from armaden.framework.protocols.task_runtime import TaskRuntimeInterface


type TaskCallback = Callable[
    [TaskRuntimeInterface],
    Coroutine[Any, Any, Result[None, ErrorInterface]]
]
type StatusCallback = Callable[
    [TaskRuntimeInterface],
    Coroutine[Any, Any, Result[Dict[str, Any], ErrorInterface]]
]


_PipelineSourceT = TypeVar('_PipelineSourceT')
_PipelineOutputT = TypeVar('_PipelineOutputT')
_LifecycleSourceT = TypeVar('_LifecycleSourceT')


class Pipeline(Generic[_PipelineSourceT, _PipelineOutputT]):
    ...


class Lifecycle(Generic[_LifecycleSourceT]):
    ...


class TaskInterface(Protocol):
    @property
    def name(self) -> str | None: ...

    @property
    def description(self) -> str | None: ...

    @property
    def initialize(self) -> TaskCallback | None: ...

    @property
    def run(self) -> TaskCallback: ...

    @property
    def shutdown(self) -> TaskCallback | None: ...

    @property
    def status(self) -> StatusCallback | None: ...

    @property
    def threading_policy(self) -> 'TaskThreadingPolicy': ...

    @property
    def auto_restart(self) -> bool: ...


class TaskBuilderInterface(Protocol):
    def name(self, value: str | None) -> Self: ...

    def description(self, value: str | None) -> Self: ...

    def on_initialize(self, callback: TaskCallback) -> Self: ...

    def on_run(self, callback: TaskCallback) -> Self: ...

    def on_shutdown(self, callback: TaskCallback) -> Self: ...

    def on_status(self, callback: StatusCallback) -> Self: ...

    def exclusive_thread(self) -> Self: ...

    def shared_thread(self) -> Self: ...

    def with_auto_restart(self) -> Self: ...

    def build(self) -> TaskInterface: ...
