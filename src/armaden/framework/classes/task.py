import warnings
from typing import Self

from armaden.framework.protocols.task import TaskInterface, TaskCallback, StatusCallback
from armaden.framework.enums.task_threading_policy import TaskThreadingPolicy


class _LegacyTask(TaskInterface):
    def __init__(
        self,
        name: str | None,
        description: str | None,
        initialize: TaskCallback | None,
        run: TaskCallback,
        shutdown: TaskCallback | None,
        status: StatusCallback | None,
        threading_policy: TaskThreadingPolicy,
        auto_restart: bool,
    ) -> None:
        self._name = name
        self._description = description
        self._initialize = initialize
        self._run = run
        self._shutdown = shutdown
        self._status = status
        self._threading_policy = threading_policy
        self._auto_restart = auto_restart

    @property
    def name(self) -> str | None:
        return self._name

    @property
    def description(self) -> str | None:
        return self._description

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
        self._name = None
        self._description = None
        self._initialize: TaskCallback | None = None
        self._run: TaskCallback | None = None
        self._shutdown: TaskCallback | None = None
        self._status: StatusCallback | None = None
        self._threading_policy = TaskThreadingPolicy.SHARED
        self._auto_restart = False

    def name(self, value: str | None) -> Self:
        self._name = value
        return self

    def description(self, value: str | None) -> Self:
        self._description = value
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
        warnings.warn(
            'TaskBuilder.with_auto_restart() is deprecated; use .restart(RestartPolicy.ALWAYS) instead',
            DeprecationWarning,
            stacklevel=2,
        )
        self._auto_restart = True
        return self

    def build(self) -> TaskInterface:
        if self._run is None:
            raise ValueError('Task run callback must be set before building')

        return _LegacyTask(
            name=self._name,
            description=self._description,
            initialize=self._initialize,
            run=self._run,
            shutdown=self._shutdown,
            status=self._status,
            threading_policy=self._threading_policy,
            auto_restart=self._auto_restart,
        )


def __getattr__(name):
    if name == 'Task':
        warnings.warn(
            'armaden.framework.classes.task.Task is deprecated; '
            'subclass armaden.framework.runtime.task.Task or use '
            'armaden.framework.runtime.task_builder.TaskBuilder instead',
            DeprecationWarning,
            stacklevel=2,
        )
        return _LegacyTask
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
