from typing import TYPE_CHECKING, Any

from armaden.framework.runtime.task import Task, TaskPolicy
from armaden.framework.runtime.task_graph import TaskGraph
from armaden.framework.utils.types import Result

if TYPE_CHECKING:
    from armaden.framework.runtime.supervisor import Supervisor


class _ScheduledTask(Task):
    def __init__(self, name: str, action, policy: TaskPolicy, **kwargs: Any) -> None:
        super().__init__(name=name, policy=policy, **kwargs)
        self._action = action

    async def run(self) -> Result[Any]:
        result = self._action(self)
        if hasattr(result, '__await__'):
            return await result
        return result


class ScheduleBuilder:
    def __init__(
        self,
        supervisor: 'Supervisor',
        name: str,
        seconds: float | None = None,
        cron: str | None = None,
    ) -> None:
        self._supervisor = supervisor
        self._name = name
        self._seconds = seconds
        self._cron = cron
        self._action = None
        self._timeout: float | None = None
        self._retries = 0
        self._retry_delay = 1.0
        self._retry_backoff = 2.0
        self._depends_on: list[str | type] = []
        self._awaits: list[str | type] = []

    def action(self, callback) -> 'ScheduleBuilder':
        self._action = callback
        return self

    def timeout(self, seconds: float) -> 'ScheduleBuilder':
        self._timeout = seconds
        return self

    def retries(self, count: int, delay: float = 1.0, backoff: float = 2.0) -> 'ScheduleBuilder':
        self._retries = count
        self._retry_delay = delay
        self._retry_backoff = backoff
        return self

    def depends_on(self, *names: str | type) -> 'ScheduleBuilder':
        self._depends_on.extend(names)
        return self

    def awaits(self, *names: str | type) -> 'ScheduleBuilder':
        self._awaits.extend(names)
        return self

    def build(self) -> _ScheduledTask:
        if self._action is None:
            raise ValueError('ScheduleBuilder requires an action() before building')
        policy = TaskPolicy(
            timeout=self._timeout,
            retries=self._retries,
            retry_delay=self._retry_delay,
            retry_backoff=self._retry_backoff,
        )
        return _ScheduledTask(
            name=self._name,
            action=self._action,
            policy=policy,
            depends_on=list(self._depends_on),
            awaits=list(self._awaits),
        )

    def submit(self) -> TaskGraph:
        task = self.build()
        graph = self._supervisor.submit([task])

        scheduler = self._supervisor._ensure_scheduler()
        trigger = self._build_trigger()
        scheduler.add_job(
            self._supervisor._execute_graph,
            trigger=trigger,
            args=[graph],
            id=self._name,
            replace_existing=True,
        )
        return graph

    def _build_trigger(self):
        if self._cron is not None:
            from apscheduler.triggers.cron import CronTrigger
            return CronTrigger.from_crontab(self._cron)
        from apscheduler.triggers.interval import IntervalTrigger
        return IntervalTrigger(seconds=self._seconds or 1.0)
