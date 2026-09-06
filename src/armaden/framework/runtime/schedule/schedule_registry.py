from __future__ import annotations

import asyncio
import inspect
import logging
from collections.abc import Awaitable, Callable
from dataclasses import replace
from datetime import datetime, time
from typing import cast, override
from zoneinfo import ZoneInfo

from returns.pipeline import is_successful
from returns.result import Failure, Success

from armaden.framework.runtime.schedule.dto.schedule_inspection_data import ScheduleInspectionData
from armaden.framework.runtime.schedule.dto.scheduled_event_definition_data import (
    ScheduledEventDefinitionData,
)
from armaden.framework.protocols.schedule_registry_protocol import ScheduleRegistryProtocol
from armaden.framework.protocols.scheduler_protocol import SchedulerProtocol
from armaden.framework.runtime.error.error import Error
from armaden.framework.runtime.schedule.exceptions.schedule_error import ScheduleError
from armaden.framework.runtime.schedule.frequency import create_trigger
from armaden.framework.types.result import Result
from armaden.framework.types.schedule import ScheduleCondition, ScheduleHook, ScheduleTag

logger = logging.getLogger(__name__)


class ScheduleRegistry(
    ScheduleRegistryProtocol[ScheduledEventDefinitionData, ScheduleInspectionData],
):
    def __init__(
        self,
        scheduler: SchedulerProtocol,
        dispatcher: Callable[
            [ScheduledEventDefinitionData],
            object | Awaitable[object],
        ],
        timezone: str = 'UTC',
        environment: Callable[[], str] | None = None,
    ) -> None:
        self._definitions: dict[str, ScheduleInspectionData] = {}
        self._dispatcher: Callable[
            [ScheduledEventDefinitionData],
            object | Awaitable[object],
        ] = dispatcher
        self._environment: Callable[[], str] = environment or (lambda: 'local')
        self._locks: dict[str, asyncio.Lock] = {}
        self._next_identifier: int = 1
        self._scheduler: SchedulerProtocol = scheduler
        self._started: bool = bool(getattr(scheduler, 'running', False))
        self._timezone: str = timezone


    @override
    def definitions(
        self,
        tag: ScheduleTag | None = None,
    ) -> list[ScheduleInspectionData]:
        values = [self._refresh(value) for value in self._definitions.values()]
        if tag is None:
            return values
        return [value for value in values if tag in value.definition.tags]


    async def _dispatch(self, definition: ScheduledEventDefinitionData) -> Result[object]:
        name = definition.name or 'scheduled-event'
        if not await self._should_run(definition):
            self._increment(name, 'skipped_count')
            self._update(name, last_status='skipped')
            return Success(None)

        options = definition.execution
        lock = self._locks.setdefault(name, asyncio.Lock())
        if options.without_overlapping_minutes is not None and lock.locked():
            self._increment(name, 'skipped_count')
            self._update(name, last_status='skipped')
            return Success(None)

        started_at = datetime.now()
        self._increment(name, 'run_count')
        self._update(name, last_started_at=started_at, last_status='running')

        if options.without_overlapping_minutes is not None:
            _ = await lock.acquire()

        try:
            await self._run_hooks(definition.hooks.before, definition)
            result = self._dispatcher(definition)
            if inspect.isawaitable(result):
                result = await result
            if isinstance(result, (Success, Failure)):
                typed_result = cast(Result[object], result)
            else:
                typed_result = Success(result)
            status = 'success' if is_successful(typed_result) else 'failure'
            error = None if is_successful(typed_result) else str(typed_result.failure())
            finished_at = datetime.now()
            self._update(
                name,
                last_error=error,
                last_duration_seconds=(finished_at - started_at).total_seconds(),
                last_finished_at=finished_at,
                last_status=status,
            )
            await self._run_hooks(definition.hooks.on_success if is_successful(typed_result) else definition.hooks.on_failure, typed_result)
            return typed_result
        except Exception as exception:
            finished_at = datetime.now()
            self._update(
                name,
                last_error=str(exception),
                last_duration_seconds=(finished_at - started_at).total_seconds(),
                last_finished_at=finished_at,
                last_status='failure',
            )
            await self._run_hooks(definition.hooks.on_failure, exception)
            return Failure(Error(ScheduleError.REGISTRATION_FAILED, details={'error': str(exception)}))
        finally:
            await self._run_hooks(definition.hooks.after, definition)
            if lock.locked():
                lock.release()


    async def _run_condition(self, condition: ScheduleCondition) -> bool:
        result = condition()
        if inspect.isawaitable(result):
            result = await result
        return bool(result)


    async def _run_hooks(self, hooks: tuple[ScheduleHook, ...], value: object) -> None:
        for hook in hooks:
            try:
                parameters = inspect.signature(hook).parameters
                result = hook() if not parameters else hook(value)
                if inspect.isawaitable(result):
                    await result
            except Exception as exception:
                logger.warning('Scheduled hook failed: %s', exception)


    async def _should_run(self, definition: ScheduledEventDefinitionData) -> bool:
        constraints = definition.constraints
        now = self._now(definition)
        if constraints.days and now.weekday() not in constraints.days:
            return False
        if constraints.weekdays_only and now.weekday() > 4:
            return False
        if constraints.weekends_only and now.weekday() < 5:
            return False
        if constraints.environments and self._environment() not in constraints.environments:
            return False
        if constraints.start_time and constraints.end_time and not self._within(
            now.time(), constraints.start_time, constraints.end_time,
        ):
            return False
        if constraints.unless_start_time and constraints.unless_end_time and self._within(
            now.time(), constraints.unless_start_time, constraints.unless_end_time,
        ):
            return False
        for condition in constraints.when:
            if not await self._run_condition(condition):
                return False
        for condition in constraints.skip:
            if await self._run_condition(condition):
                return False
        return True


    def _now(self, definition: ScheduledEventDefinitionData) -> datetime:
        timezone = definition.frequency.timezone or self._timezone
        try:
            return datetime.now(ZoneInfo(timezone))
        except Exception:
            return datetime.now()


    def _job_callback(
        self,
        definition: ScheduledEventDefinitionData,
    ) -> Callable[[], Awaitable[Result[object]]]:
        job_name = definition.name or 'scheduled-event'

        async def callback() -> Result[object]:
            return await self._dispatch(definition)

        callback.__name__ = job_name
        callback.__qualname__ = job_name
        return callback


    def _name(self, definition: ScheduledEventDefinitionData) -> str:
        if definition.name is not None:
            return definition.name
        name = f'schedule-{self._next_identifier}'
        self._next_identifier += 1
        return name


    def _increment(self, name: str, field: str) -> None:
        inspection = self._definitions.get(name)
        if inspection is None:
            return
        value = getattr(inspection, field, 0)
        self._update(name, **{field: value + 1 if isinstance(value, int) else 1})


    def _refresh(self, inspection: ScheduleInspectionData) -> ScheduleInspectionData:
        try:
            jobs = self._scheduler.get_jobs()
        except Exception:
            return inspection
        for job in jobs:
            if getattr(job, 'id', None) == inspection.definition.name:
                next_run_at = getattr(job, 'next_run_time', None)
                return replace(
                    inspection,
                    next_run_at=next_run_at,
                    paused=next_run_at is None and not inspection.paused,
                )
        return inspection


    def _update(self, name: str, **values: object) -> None:
        inspection = self._definitions.get(name)
        if inspection is not None:
            self._definitions[name] = replace(inspection, **values)


    @staticmethod
    def _parse_time(value: str) -> time:
        return datetime.strptime(value, '%H:%M').time()


    @classmethod
    def _within(cls, current: time, start: str, end: str) -> bool:
        start_time = cls._parse_time(start)
        end_time = cls._parse_time(end)
        if start_time <= end_time:
            return start_time <= current <= end_time
        return current >= start_time or current <= end_time


    @override
    def register(
        self,
        definition: ScheduledEventDefinitionData,
    ) -> Result[ScheduleInspectionData]:
        name = self._name(definition)
        if name in self._definitions:
            return Failure(Error(ScheduleError.DUPLICATE_NAME, details={'name': name}))

        named_definition = replace(definition, name=name)
        try:
            trigger = create_trigger(named_definition.frequency, self._timezone)
            _ = self._scheduler.add_job(
                self._job_callback(named_definition),
                trigger=trigger,
                args=[],
                id=name,
                replace_existing=False,
            )
        except Exception as exception:
            return Failure(Error(
                ScheduleError.REGISTRATION_FAILED,
                details={'name': name, 'error': str(exception)},
            ))

        inspection = ScheduleInspectionData(definition=named_definition)
        self._definitions[name] = inspection
        return Success(inspection)


    @override
    def pause(self, name: str) -> Result[None]:
        if name not in self._definitions:
            return Failure(Error(ScheduleError.INVALID_DEFINITION, details={'name': name}))
        try:
            pause_job = getattr(self._scheduler, 'pause_job')
            _ = pause_job(name)
        except Exception as exception:
            return Failure(Error(ScheduleError.REGISTRATION_FAILED, details={'name': name, 'error': str(exception)}))
        self._update(name, paused=True)
        return Success(None)


    @override
    def remove(self, name: str) -> Result[None]:
        if name not in self._definitions:
            return Failure(Error(ScheduleError.INVALID_DEFINITION, details={'name': name}))
        try:
            _ = self._scheduler.remove_job(name)
        except Exception as exception:
            return Failure(Error(
                ScheduleError.REGISTRATION_FAILED,
                details={'name': name, 'error': str(exception)},
            ))
        del self._definitions[name]
        _ = self._locks.pop(name, None)
        return Success(None)


    @override
    def resume(self, name: str) -> Result[None]:
        if name not in self._definitions:
            return Failure(Error(ScheduleError.INVALID_DEFINITION, details={'name': name}))
        try:
            resume_job = getattr(self._scheduler, 'resume_job')
            _ = resume_job(name)
        except Exception as exception:
            return Failure(Error(ScheduleError.REGISTRATION_FAILED, details={'name': name, 'error': str(exception)}))
        self._update(name, paused=False)
        return Success(None)


    @override
    def shutdown(self) -> Result[None]:
        if not self._started:
            self._definitions.clear()
            self._locks.clear()
            return Success(None)
        try:
            _ = self._scheduler.shutdown(wait=False)
        except Exception as exception:
            return Failure(Error(ScheduleError.REGISTRATION_FAILED, details={'error': str(exception)}))
        self._started = False
        self._definitions.clear()
        self._locks.clear()
        return Success(None)


    @override
    def start(self) -> Result[None]:
        if self._started or bool(getattr(self._scheduler, 'running', False)):
            self._started = True
            return Success(None)
        try:
            _ = self._scheduler.start()
        except Exception as exception:
            return Failure(Error(ScheduleError.REGISTRATION_FAILED, details={'error': str(exception)}))
        self._started = True
        return Success(None)
