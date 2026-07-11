from abc import ABC, abstractmethod
from copy import copy
from dataclasses import dataclass
from typing import Any

from returns.result import Success

from armaden.framework.classes.instance_container import MultiImplementation
from armaden.framework.enums.restart_policy import RestartPolicy
from armaden.framework.enums.task_threading_policy import TaskThreadingPolicy
from armaden.framework.utils.types import Result


@dataclass
class TaskPolicy:
    timeout: float | None = None
    retries: int = 0
    retry_delay: float = 1.0
    retry_backoff: float = 2.0
    priority: int = 0
    restart: RestartPolicy = RestartPolicy.NEVER
    continue_on_failure: bool = False
    ready_timeout: float | None = None


class Task(ABC, MultiImplementation):
    name: str | None = None
    description: str | None = None
    policy: TaskPolicy | None = None
    threading_policy: TaskThreadingPolicy = TaskThreadingPolicy.SHARED
    depends_on: list[str | type] | None = None
    awaits: list[str | type] | None = None
    long_running: bool = False

    _runtime_ref: Any = None
    _injector_ref: Any = None
    _graph_ref: Any = None

    def __init__(
        self,
        name: str | None = None,
        description: str | None = None,
        policy: TaskPolicy | None = None,
        threading_policy: TaskThreadingPolicy | None = None,
        depends_on: list[str | type] | None = None,
        awaits: list[str | type] | None = None,
        long_running: bool | None = None,
    ) -> None:
        cls = type(self)

        self.name = name if name is not None else (cls.name or cls.__name__)
        self.description = description if description is not None else cls.description

        if policy is not None:
            self.policy = policy
        elif cls.policy is not None:
            self.policy = copy(cls.policy)
        else:
            self.policy = TaskPolicy()

        self.threading_policy = (
            threading_policy if threading_policy is not None else cls.threading_policy
        )

        self.depends_on = list(depends_on) if depends_on is not None else list(cls.depends_on or [])
        self.awaits = list(awaits) if awaits is not None else list(cls.awaits or [])
        self.long_running = long_running if long_running is not None else cls.long_running

    @property
    def runtime(self) -> Any:
        return self._runtime_ref

    @property
    def injector(self) -> Any:
        return self._injector_ref

    @property
    def graph(self) -> Any:
        return self._graph_ref

    async def initialize(self) -> Result[None]:
        return Success(None)

    @abstractmethod
    async def run(self) -> Result[Any]:
        raise NotImplementedError

    async def shutdown(self) -> Result[None]:
        return Success(None)

    async def status(self) -> Result[dict[str, Any]]:
        return Success({})
