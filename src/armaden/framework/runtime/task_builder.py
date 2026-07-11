from abc import abstractmethod
from dataclasses import dataclass, field
from typing import Any, Self, override

from returns.result import Success

from armaden.framework.enums.restart_policy import RestartPolicy
from armaden.framework.enums.task_threading_policy import TaskThreadingPolicy
from armaden.framework.protocols.task import TaskInterface, TaskBuilderInterface
from armaden.framework.runtime.task import Task, TaskPolicy
from armaden.framework.utils.types import Result


class TaskBuilder:
    def __init__(self) -> None:
        self._name: str | None = None
        self._description: str | None = None
        self._initialize = None
        self._run = None
        self._shutdown = None
        self._status = None
        self._threading_policy = TaskThreadingPolicy.SHARED

        self._timeout: float | None = None
        self._retries = 0
        self._retry_delay = 1.0
        self._retry_backoff = 2.0
        self._priority = 0
        self._restart = RestartPolicy.NEVER
        self._continue_on_failure = False
        self._ready_timeout: float | None = None
        self._auto_restart = False

        self._depends_on: list[str | type] = []
        self._awaits: list[str | type] = []
        self._long_running = False

    def name(self, value: str | None) -> Self:
        self._name = value
        return self

    def description(self, value: str | None) -> Self:
        self._description = value
        return self

    def on_initialize(self, callback) -> Self:
        self._initialize = callback
        return self

    def on_run(self, callback) -> Self:
        self._run = callback
        return self

    def on_shutdown(self, callback) -> Self:
        self._shutdown = callback
        return self

    def on_status(self, callback) -> Self:
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

    def timeout(self, seconds: float) -> Self:
        self._timeout = seconds
        return self

    def retries(self, count: int, delay: float = 1.0, backoff: float = 2.0) -> Self:
        self._retries = count
        self._retry_delay = delay
        self._retry_backoff = backoff
        return self

    def priority(self, value: int) -> Self:
        self._priority = value
        return self

    def restart(self, policy: RestartPolicy) -> Self:
        self._restart = policy
        return self

    def continue_on_failure(self) -> Self:
        self._continue_on_failure = True
        return self

    def ready_timeout(self, seconds: float) -> Self:
        self._ready_timeout = seconds
        return self

    def depends_on(self, *names: str | type) -> Self:
        self._depends_on.extend(names)
        return self

    def awaits(self, *names: str | type) -> Self:
        self._awaits.extend(names)
        return self

    def long_running(self) -> Self:
        self._long_running = True
        return self

    def _build_policy(self) -> TaskPolicy:
        restart = self._restart
        if self._auto_restart and restart == RestartPolicy.NEVER:
            restart = RestartPolicy.ALWAYS
        return TaskPolicy(
            timeout=self._timeout,
            retries=self._retries,
            retry_delay=self._retry_delay,
            retry_backoff=self._retry_backoff,
            priority=self._priority,
            restart=restart,
            continue_on_failure=self._continue_on_failure,
            ready_timeout=self._ready_timeout,
        )

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
            callbacks=callbacks,
            name=self._name,
            description=self._description,
            policy=self._build_policy(),
            threading_policy=self._threading_policy,
            depends_on=list(self._depends_on),
            awaits=list(self._awaits),
            long_running=self._long_running,
        )


@dataclass
class _BuiltCallbacks:
    initialize: Any = None
    run: Any = None
    shutdown: Any = None
    status: Any = None


class _BuiltTask(Task):
    def __init__(self, callbacks: _BuiltCallbacks, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._callbacks = callbacks

    @override
    async def initialize(self) -> Result[None]:
        if self._callbacks.initialize is None:
            return Success(None)
        result = self._callbacks.initialize(self)
        if hasattr(result, '__await__'):
            return await result
        return result

    @override
    async def run(self) -> Result[Any]:
        result = self._callbacks.run(self)
        if hasattr(result, '__await__'):
            return await result
        return result

    @override
    async def shutdown(self) -> Result[None]:
        if self._callbacks.shutdown is None:
            return Success(None)
        result = self._callbacks.shutdown(self)
        if hasattr(result, '__await__'):
            return await result
        return result

    @override
    async def status(self) -> Result[dict[str, Any]]:
        if self._callbacks.status is None:
            return Success({})
        result = self._callbacks.status(self)
        if hasattr(result, '__await__'):
            return await result
        return result
