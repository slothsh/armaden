from __future__ import annotations

import inspect
from collections.abc import Callable, Mapping, Sequence
from dataclasses import replace
from datetime import datetime
from typing import cast, override

from returns.pipeline import is_successful

from armaden.framework.runtime.schedule.dto.schedule_constraint_data import ScheduleConstraintData
from armaden.framework.runtime.schedule.dto.schedule_execution_options_data import (
    ScheduleExecutionOptionsData,
)
from armaden.framework.runtime.schedule.dto.schedule_frequency_data import ScheduleFrequencyData
from armaden.framework.runtime.schedule.dto.schedule_hook_data import ScheduleHookData
from armaden.framework.runtime.schedule.dto.schedule_inspection_data import ScheduleInspectionData
from armaden.framework.runtime.schedule.dto.schedule_queue_data import ScheduleQueueData
from armaden.framework.runtime.schedule.dto.scheduled_event_definition_data import (
    ScheduledEventDefinitionData,
)
from armaden.framework.protocols.scheduled_event_protocol import ScheduledEventProtocol
from armaden.framework.runtime.schedule.exceptions.schedule_definition_error import (
    ScheduleDefinitionError,
)
from armaden.framework.runtime.schedule.enums import ScheduledEventKind, ScheduledWorkerMode
from armaden.framework.runtime.schedule.exceptions.schedule_error import ScheduleError
from armaden.framework.types.result import Result
from armaden.framework.types.schedule import (
    ScheduleCallback,
    ScheduleCondition,
    ScheduleHook,
)


class ScheduledEvent(
    ScheduledEventProtocol[
        ScheduledEventKind,
        ScheduledEventDefinitionData,
        ScheduleInspectionData,
    ],
):
    def __init__(
        self,
        kind: ScheduledEventKind,
        target: object,
        registration: Callable[
            [ScheduledEventDefinitionData],
            Result[ScheduleInspectionData],
        ]
        | None = None,
    ) -> None:
        self._constraints: ScheduleConstraintData = ScheduleConstraintData()
        self._description: str | None = None
        self._execution: ScheduleExecutionOptionsData = ScheduleExecutionOptionsData()
        self._frequency_data: ScheduleFrequencyData = ScheduleFrequencyData()
        self._hooks: ScheduleHookData = ScheduleHookData()
        self._kind: ScheduledEventKind = kind
        self._name: str | None = None
        self._registration: Callable[
            [ScheduledEventDefinitionData],
            Result[ScheduleInspectionData],
        ] | None = registration
        self._tags: tuple[str | type[object], ...] = ()
        self._target: object = target


    @property
    @override
    def kind(self) -> ScheduledEventKind:
        return self._kind


    @override
    def after(self, callback: ScheduleHook) -> ScheduledEvent:
        self._hooks = replace(self._hooks, after=(*self._hooks.after, callback))
        return self


    @override
    def append_output_to(self, path: str) -> ScheduledEvent:
        self._execution = replace(
            self._execution,
            append_output_path=self._validate_path(path),
            output_path=None,
        )
        return self


    @override
    def at(self, time: str) -> ScheduledEvent:
        validated_time = self._validate_time(time)
        current_value = self._frequency_data.value
        values: dict[str, object] = (
            dict(cast(Mapping[str, object], current_value))
            if isinstance(current_value, Mapping)
            else {}
        )
        values['time'] = validated_time
        self._frequency_data = replace(self._frequency_data, value=values)
        return self


    @override
    def before(self, callback: ScheduleHook) -> ScheduledEvent:
        self._hooks = replace(self._hooks, before=(*self._hooks.before, callback))
        return self


    @override
    def between(self, start: str, end: str) -> ScheduledEvent:
        self._constraints = replace(
            self._constraints,
            end_time=self._validate_time(end),
            start_time=self._validate_time(start),
        )
        return self


    @override
    def connection(self, name: str) -> ScheduledEvent:
        return self.on_connection(name)


    @override
    def cron(self, expression: str) -> ScheduledEvent:
        if not expression.strip():
            raise ScheduleDefinitionError(ScheduleError.INVALID_FREQUENCY)
        return self._set_frequency('cron', expression)


    @override
    def daily(self) -> ScheduledEvent:
        return self._calendar('daily')


    @override
    def daily_at(self, time: str) -> ScheduledEvent:
        return self._calendar('daily', time=self._validate_time(time))


    @override
    def days(self, values: Sequence[int]) -> ScheduledEvent:
        days = tuple(values)
        if not days or any(day not in range(7) for day in days):
            raise ScheduleDefinitionError(ScheduleError.INVALID_FREQUENCY)
        self._constraints = replace(self._constraints, days=days)
        return self


    @override
    def definition(self) -> ScheduledEventDefinitionData:
        return ScheduledEventDefinitionData(
            constraints=self._constraints,
            description=self._description,
            execution=self._execution,
            frequency=self._frequency_data,
            hooks=self._hooks,
            kind=self._kind,
            name=self._name,
            tags=self._tags,
            target=self._target,
        )


    @override
    def description(self, value: str) -> ScheduledEvent:
        self._description = value
        return self


    @override
    def environments(self, *values: str) -> ScheduledEvent:
        if not values or any(not value for value in values):
            raise ScheduleDefinitionError(ScheduleError.INVALID_DEFINITION)
        self._constraints = replace(self._constraints, environments=tuple(values))
        return self


    @override
    def even_in_maintenance_mode(self) -> ScheduledEvent:
        self._execution = replace(self._execution, even_in_maintenance_mode=True)
        return self


    @override
    def every_fifteen_minutes(self) -> ScheduledEvent:
        return self._interval(900)


    @override
    def every_fifteen_seconds(self) -> ScheduledEvent:
        return self._interval(15)


    @override
    def every_five_minutes(self) -> ScheduledEvent:
        return self._interval(300)


    @override
    def every_five_seconds(self) -> ScheduledEvent:
        return self._interval(5)


    @override
    def every_four_hours(self, minute: int = 0) -> ScheduledEvent:
        return self._calendar('every_four_hours', hours=4, minute=self._validate_minute(minute))


    @override
    def every_four_minutes(self) -> ScheduledEvent:
        return self._interval(240)


    @override
    def every_minute(self) -> ScheduledEvent:
        return self._interval(60)


    @override
    def every_odd_hour(self, minute: int = 0) -> ScheduledEvent:
        return self._calendar('every_odd_hour', minute=self._validate_minute(minute))


    @override
    def every_second(self) -> ScheduledEvent:
        return self._interval(1)


    @override
    def every_seconds(self, value: int | float) -> ScheduledEvent:
        if isinstance(value, bool) or value <= 0:
            raise ScheduleDefinitionError(ScheduleError.INVALID_FREQUENCY)
        return self._set_frequency('interval', value)


    @override
    def every_six_hours(self, minute: int = 0) -> ScheduledEvent:
        return self._calendar('every_six_hours', hours=6, minute=self._validate_minute(minute))


    @override
    def every_ten_minutes(self) -> ScheduledEvent:
        return self._interval(600)


    @override
    def every_ten_seconds(self) -> ScheduledEvent:
        return self._interval(10)


    @override
    def every_thirty_minutes(self) -> ScheduledEvent:
        return self._interval(1800)


    @override
    def every_thirty_seconds(self) -> ScheduledEvent:
        return self._interval(30)


    @override
    def every_three_hours(self, minute: int = 0) -> ScheduledEvent:
        return self._calendar('every_three_hours', hours=3, minute=self._validate_minute(minute))


    @override
    def every_three_minutes(self) -> ScheduledEvent:
        return self._interval(180)


    @override
    def every_three_seconds(self) -> ScheduledEvent:
        return self._interval(3)


    @override
    def every_two_hours(self, minute: int = 0) -> ScheduledEvent:
        return self._calendar('every_two_hours', hours=2, minute=self._validate_minute(minute))


    @override
    def every_two_minutes(self) -> ScheduledEvent:
        return self._interval(120)


    @override
    def every_two_seconds(self) -> ScheduledEvent:
        return self._interval(2)


    @override
    def fridays(self) -> ScheduledEvent:
        return self.days([4])


    @override
    def exclusive_worker(self) -> ScheduledEvent:
        self._execution = replace(
            self._execution,
            worker_mode=ScheduledWorkerMode.EXCLUSIVE,
        )
        return self


    @override
    def group(self, callback: ScheduleCallback) -> ScheduledEvent:
        result = callback(self)
        if inspect.isawaitable(result):
            raise ScheduleDefinitionError(ScheduleError.INVALID_DEFINITION)
        return self


    @override
    def hourly(self) -> ScheduledEvent:
        return self._calendar('hourly')


    @override
    def hourly_at(self, minute: int) -> ScheduledEvent:
        return self._calendar('hourly', minute=self._validate_minute(minute))


    @override
    def last_day_of_month(self, time: str = '00:00') -> ScheduledEvent:
        return self._calendar('last_day_of_month', time=self._validate_time(time))


    @override
    def mondays(self) -> ScheduledEvent:
        return self.days([0])


    @override
    def monthly(self) -> ScheduledEvent:
        return self._calendar('monthly')


    @override
    def monthly_on(self, day: int, time: str = '00:00') -> ScheduledEvent:
        return self._calendar(
            'monthly_on',
            day=self._validate_day_of_month(day),
            time=self._validate_time(time),
        )


    @override
    def name(self, value: str) -> ScheduledEvent:
        if not value.strip():
            raise ScheduleDefinitionError(ScheduleError.MISSING_NAME)
        self._name = value
        return self


    @override
    def on_connection(self, name: str) -> ScheduledEvent:
        queue = self._queue()
        self._execution = replace(
            self._execution,
            queue=replace(queue, connection=self._validate_path(name)),
        )
        return self


    @override
    def on_failure(self, callback: ScheduleHook) -> ScheduledEvent:
        self._hooks = replace(self._hooks, on_failure=(*self._hooks.on_failure, callback))
        return self


    @override
    def on_one_server(self) -> ScheduledEvent:
        self._execution = replace(self._execution, on_one_server=True)
        return self


    @override
    def on_queue(self, name: str) -> ScheduledEvent:
        queue = self._queue()
        self._execution = replace(
            self._execution,
            queue=replace(queue, name=self._validate_path(name)),
        )
        return self


    @override
    def on_success(self, callback: ScheduleHook) -> ScheduledEvent:
        self._hooks = replace(self._hooks, on_success=(*self._hooks.on_success, callback))
        return self


    @override
    def priority(self, value: int) -> ScheduledEvent:
        if value < 0:
            raise ScheduleDefinitionError(ScheduleError.INVALID_DEFINITION)
        queue = self._queue()
        self._execution = replace(
            self._execution,
            queue=replace(queue, priority=value),
        )
        return self


    @override
    def quarterly(self) -> ScheduledEvent:
        return self._calendar('quarterly')


    @override
    def quarterly_on(self, day: int, time: str = '00:00') -> ScheduledEvent:
        return self._calendar(
            'quarterly_on',
            day=self._validate_day_of_month(day),
            time=self._validate_time(time),
        )


    @override
    def run_in_background(self) -> ScheduledEvent:
        self._execution = replace(self._execution, run_in_background=True)
        return self


    @override
    def saturdays(self) -> ScheduledEvent:
        return self.days([5])


    @override
    def send_output_to(self, path: str) -> ScheduledEvent:
        self._execution = replace(
            self._execution,
            append_output_path=None,
            output_path=self._validate_path(path),
        )
        return self


    @override
    def skip(self, condition: ScheduleCondition) -> ScheduledEvent:
        self._constraints = replace(self._constraints, skip=(*self._constraints.skip, condition))
        return self


    @override
    def submit(self) -> ScheduleInspectionData:
        if self._registration is None:
            raise ScheduleDefinitionError(ScheduleError.REGISTRATION_FAILED)
        result = self._registration(self.definition())
        if not is_successful(result):
            raise ScheduleDefinitionError(
                ScheduleError.REGISTRATION_FAILED,
                str(result.failure()),
            )
        return result.unwrap()


    @override
    def sundays(self) -> ScheduledEvent:
        return self.days([6])


    @override
    def thursdays(self) -> ScheduledEvent:
        return self.days([3])


    @override
    def tuesdays(self) -> ScheduledEvent:
        return self.days([1])


    @override
    def timezone(self, value: str) -> ScheduledEvent:
        if not value.strip():
            raise ScheduleDefinitionError(ScheduleError.INVALID_DEFINITION)
        self._frequency_data = replace(self._frequency_data, timezone=value)
        return self


    @override
    def twice_daily(self, first_hour: int, second_hour: int) -> ScheduledEvent:
        return self._calendar(
            'twice_daily',
            first_hour=self._validate_hour(first_hour),
            second_hour=self._validate_hour(second_hour),
        )


    @override
    def twice_daily_at(
        self,
        first_hour: int,
        second_hour: int,
        minute: int = 0,
    ) -> ScheduledEvent:
        return self._calendar(
            'twice_daily_at',
            first_hour=self._validate_hour(first_hour),
            minute=self._validate_minute(minute),
            second_hour=self._validate_hour(second_hour),
        )


    @override
    def unless_between(self, start: str, end: str) -> ScheduledEvent:
        self._constraints = replace(
            self._constraints,
            unless_end_time=self._validate_time(end),
            unless_start_time=self._validate_time(start),
        )
        return self


    @override
    def when(self, condition: ScheduleCondition) -> ScheduledEvent:
        self._constraints = replace(self._constraints, when=(*self._constraints.when, condition))
        return self


    @override
    def wednesdays(self) -> ScheduledEvent:
        return self.days([2])


    @override
    def weekdays(self) -> ScheduledEvent:
        self._constraints = replace(self._constraints, weekdays_only=True, weekends_only=False)
        return self


    @override
    def weekends(self) -> ScheduledEvent:
        self._constraints = replace(self._constraints, weekdays_only=False, weekends_only=True)
        return self


    @override
    def weekly(self) -> ScheduledEvent:
        return self._calendar('weekly')


    @override
    def weekly_on(self, day: int, time: str = '00:00') -> ScheduledEvent:
        return self._calendar(
            'weekly_on',
            day=self._validate_day(day),
            time=self._validate_time(time),
        )


    @override
    def without_overlapping(self, minutes: int = 1440) -> ScheduledEvent:
        if minutes < 0:
            raise ScheduleDefinitionError(ScheduleError.INVALID_DEFINITION)
        self._execution = replace(
            self._execution,
            without_overlapping_minutes=minutes,
        )
        return self


    @override
    def yearly(self) -> ScheduledEvent:
        return self._calendar('yearly')


    @override
    def yearly_on(self, month: int, day: int, time: str = '00:00') -> ScheduledEvent:
        return self._calendar(
            'yearly_on',
            day=self._validate_day_of_month(day),
            month=self._validate_month(month),
            time=self._validate_time(time),
        )


    def tag(self, *tags: str | type[object]) -> ScheduledEvent:
        self._tags = (*self._tags, *tags)
        return self


    def _calendar(self, kind: str, **values: object) -> ScheduledEvent:
        return self._set_frequency(kind, values or None)


    def _set_frequency(self, kind: str, value: object | None = None) -> ScheduledEvent:
        self._frequency_data = replace(self._frequency_data, kind=kind, value=value)
        return self


    def _interval(self, seconds: int) -> ScheduledEvent:
        if seconds <= 0:
            raise ScheduleDefinitionError(ScheduleError.INVALID_FREQUENCY)
        return self._set_frequency('interval', seconds)


    def _queue(self) -> ScheduleQueueData:
        return self._execution.queue or ScheduleQueueData()


    @staticmethod
    def _validate_day(value: int) -> int:
        if value not in range(7):
            raise ScheduleDefinitionError(ScheduleError.INVALID_FREQUENCY)
        return value


    @staticmethod
    def _validate_day_of_month(value: int) -> int:
        if value not in range(1, 32):
            raise ScheduleDefinitionError(ScheduleError.INVALID_FREQUENCY)
        return value


    @staticmethod
    def _validate_hour(value: int) -> int:
        if value not in range(24):
            raise ScheduleDefinitionError(ScheduleError.INVALID_TIME)
        return value


    @staticmethod
    def _validate_minute(value: int) -> int:
        if value not in range(60):
            raise ScheduleDefinitionError(ScheduleError.INVALID_TIME)
        return value


    @staticmethod
    def _validate_month(value: int) -> int:
        if value not in range(1, 13):
            raise ScheduleDefinitionError(ScheduleError.INVALID_FREQUENCY)
        return value


    @staticmethod
    def _validate_path(value: str) -> str:
        if not value.strip():
            raise ScheduleDefinitionError(ScheduleError.INVALID_DEFINITION)
        return value


    @staticmethod
    def _validate_time(value: str) -> str:
        try:
            _ = datetime.strptime(value, '%H:%M')
        except ValueError as exception:
            raise ScheduleDefinitionError(ScheduleError.INVALID_TIME) from exception
        return value
