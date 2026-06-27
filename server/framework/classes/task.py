from collections.abc import Callable, Coroutine
from returns.result import Result
from typing import Any, Dict, Self

from framework.protocols.error import ErrorInterface
from framework.protocols.task import TaskInterface, TaskCallback, StatusCallback
from framework.enums.task_threading_policy import TaskThreadingPolicy


class Task(TaskInterface):
    def __init__(
        self,
        name: str,
        initialize: TaskCallback | None,
        run: TaskCallback,
        shutdown: TaskCallback | None,
        status: StatusCallback | None,
        threading_policy: TaskThreadingPolicy,
        auto_restart: bool,
    ) -> None:
        self._name = name
        self._initialize = initialize
        self._run = run
        self._shutdown = shutdown
        self._status = status
        self._threading_policy = threading_policy
        self._auto_restart = auto_restart

    @property
    def name(self) -> str:
        return self._name

    @property
    def initialize(self) -> TaskCallback | None:
        return self._initialize

    @property
    def run(self) -> TaskCallback:
        return self._run

    @property
    def shutdown(self) -> TaskCallback | None:
        return self._shutdown

    @property
    def status(self) -> StatusCallback | None:
        return self._status

    @property
    def threading_policy(self) -> TaskThreadingPolicy:
        return self._threading_policy

    @property
    def auto_restart(self) -> bool:
        return self._auto_restart


class TaskBuilder:
    def __init__(self) -> None:
        self._name = 'Task'
        self._initialize: TaskCallback | None = None
        self._run: TaskCallback | None = None
        self._shutdown: TaskCallback | None = None
        self._status: StatusCallback | None = None
        self._threading_policy = TaskThreadingPolicy.SHARED
        self._auto_restart = False

    def name(self, value: str) -> Self:
        self._name = value
        return self

    def on_initialize(self, callback: TaskCallback) -> Self:
        self._initialize = callback
        return self

    def on_run(self, callback: TaskCallback) -> Self:
        self._run = callback
        return self

    def on_shutdown(self, callback: TaskCallback) -> Self:
        self._shutdown = callback
        return self

    def on_status(self, callback: StatusCallback) -> Self:
        self._status = callback
        return self

    def exclusive_thread(self) -> Self:
        self._threading_policy = TaskThreadingPolicy.EXCLUSIVE
        return self

    def shared_thread(self) -> Self:
        self._threading_policy = TaskThreadingPolicy.SHARED
        return self

    def with_auto_restart(self) -> Self:
        self._auto_restart = True
        return self

    def build(self) -> TaskInterface:
        if self._run is None:
            raise ValueError('Task run callback must be set before building')

        return Task(
            name=self._name,
            initialize=self._initialize,
            run=self._run,
            shutdown=self._shutdown,
            status=self._status,
            threading_policy=self._threading_policy,
            auto_restart=self._auto_restart,
        )
