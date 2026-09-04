from __future__ import annotations

from collections.abc import Callable
from typing import cast, override

from armaden.framework.protocols.schedule_builder_protocol import ScheduleBuilderProtocol
from armaden.framework.protocols.supervisor_protocol import SupervisorProtocol
from armaden.framework.runtime.supervisor.task.dto.task_graph_data import TaskGraphData
from armaden.framework.runtime.supervisor.task.dto.task_policy_data import TaskPolicyData
from armaden.framework.runtime.supervisor.task.enums.task_threading_policy import (
    TaskThreadingPolicy,
)
from armaden.framework.runtime.supervisor.task.scheduled_task import ScheduledTask
from armaden.framework.types.task import TaskCallback


class ScheduleBuilder(ScheduleBuilderProtocol[TaskThreadingPolicy, TaskGraphData]):
    def __init__(
        self,
        supervisor: SupervisorProtocol[TaskGraphData],
        name: str,
        seconds: float | None = None,
        cron: str | None = None,
    ) -> None:
        self._action: TaskCallback | None = None
        self._awaits: list[str | type[object]] = []
        self._cron: str | None = cron
        self._depends_on: list[str | type[object]] = []
        self._name: str = name
        self._retry_backoff: float = 2.0
        self._retry_delay: float = 1.0
        self._retries: int = 0
        self._seconds: float | None = seconds
        self._supervisor: SupervisorProtocol[TaskGraphData] = supervisor
        self._timeout: float | None = None


    def _build_trigger(self) -> object:
        if self._cron is not None:
            module = __import__('apscheduler.triggers.cron', fromlist=['CronTrigger'])
            cron_trigger = getattr(module, 'CronTrigger')
            from_crontab = cast(
                Callable[[str], object],
                getattr(cron_trigger, 'from_crontab'),
            )
            return from_crontab(self._cron)
        module = __import__('apscheduler.triggers.interval', fromlist=['IntervalTrigger'])
        interval_trigger = cast(
            Callable[..., object],
            getattr(module, 'IntervalTrigger'),
        )
        return interval_trigger(seconds=self._seconds or 1.0)


    @override
    def action(self, callback: TaskCallback) -> ScheduleBuilder:
        self._action = callback
        return self


    @override
    def awaits(self, *references: str | type[object]) -> ScheduleBuilder:
        self._awaits.extend(references)
        return self


    @override
    def build(self) -> ScheduledTask:
        if self._action is None:
            raise ValueError('ScheduleBuilder requires an action() before building')
        return ScheduledTask(
            name=self._name,
            action=self._action,
            policy=TaskPolicyData(
                timeout=self._timeout,
                retries=self._retries,
                retry_delay=self._retry_delay,
                retry_backoff=self._retry_backoff,
            ),
            depends_on=list(self._depends_on),
            awaits=list(self._awaits),
        )


    @override
    def depends_on(self, *references: str | type[object]) -> ScheduleBuilder:
        self._depends_on.extend(references)
        return self


    @override
    def retries(
        self,
        count: int,
        delay: float = 1.0,
        backoff: float = 2.0,
    ) -> ScheduleBuilder:
        self._retries = count
        self._retry_backoff = backoff
        self._retry_delay = delay
        return self


    @override
    def submit(self) -> TaskGraphData:
        graph = self._supervisor.submit([self.build()])
        scheduler = self._supervisor.ensure_scheduler()
        _ = scheduler.add_job(
            self._supervisor.execute_graph,
            trigger=self._build_trigger(),
            args=[graph],
            id=self._name,
            replace_existing=True,
        )
        return graph


    @override
    def timeout(self, seconds: float) -> ScheduleBuilder:
        self._timeout = seconds
        return self