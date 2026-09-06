from __future__ import annotations

from collections.abc import Mapping
from typing import Callable, cast

from armaden.framework.runtime.schedule.dto.schedule_frequency_data import ScheduleFrequencyData
from armaden.framework.runtime.schedule.exceptions.schedule_definition_error import (
    ScheduleDefinitionError,
)
from armaden.framework.runtime.schedule.exceptions.schedule_error import ScheduleError


def create_trigger(
    frequency: ScheduleFrequencyData,
    default_timezone: str = 'UTC',
) -> object:
    try:
        if frequency.kind == 'interval':
            return _interval_trigger(frequency, default_timezone)
        return _cron_trigger(frequency, default_timezone)
    except (ImportError, KeyError, TypeError, ValueError) as exception:
        if isinstance(exception, ImportError):
            raise
        raise ScheduleDefinitionError(ScheduleError.INVALID_FREQUENCY) from exception


def _cron_trigger(frequency: ScheduleFrequencyData, timezone: str) -> object:
    module = __import__('apscheduler.triggers.cron', fromlist=['CronTrigger'])
    trigger_type = cast(Callable[..., object], getattr(module, 'CronTrigger'))
    values = _values(frequency.value)
    trigger_timezone = frequency.timezone or timezone
    if frequency.kind == 'cron':
        from_crontab = cast(Callable[..., object], getattr(trigger_type, 'from_crontab'))
        return from_crontab(str(frequency.value), timezone=trigger_timezone)

    fields = _calendar_fields(frequency.kind, values)
    return trigger_type(timezone=trigger_timezone, **fields)


def _calendar_fields(kind: str, values: Mapping[str, object]) -> dict[str, object]:
    if kind == 'daily':
        return _time_fields(values)
    if kind == 'every_four_hours':
        return {'hour': '*/4', 'minute': values.get('minute', 0)}
    if kind == 'every_six_hours':
        return {'hour': '*/6', 'minute': values.get('minute', 0)}
    if kind == 'every_odd_hour':
        return {'hour': '1-23/2', 'minute': values.get('minute', 0)}
    if kind == 'every_three_hours':
        return {'hour': '*/3', 'minute': values.get('minute', 0)}
    if kind == 'every_two_hours':
        return {'hour': '*/2', 'minute': values.get('minute', 0)}
    if kind == 'hourly':
        return {'minute': values.get('minute', 0)}
    if kind == 'last_day_of_month':
        return {'day': 'last', **_time_fields(values)}
    if kind == 'monthly':
        return {'day': 1}
    if kind == 'monthly_on':
        return {'day': values['day'], **_time_fields(values)}
    if kind == 'quarterly':
        return {'month': '1,4,7,10', 'day': 1}
    if kind == 'quarterly_on':
        return {'month': '1,4,7,10', 'day': values['day'], **_time_fields(values)}
    if kind == 'twice_daily':
        return {'hour': f"{values['first_hour']},{values['second_hour']}"}
    if kind == 'twice_daily_at':
        return {
            'hour': f"{values['first_hour']},{values['second_hour']}",
            'minute': values['minute'],
        }
    if kind == 'weekly':
        return {'day_of_week': 6}
    if kind == 'weekly_on':
        return {'day_of_week': values['day'], **_time_fields(values)}
    if kind == 'yearly':
        return {'month': 1, 'day': 1}
    if kind == 'yearly_on':
        return {
            'day': values['day'],
            'month': values['month'],
            **_time_fields(values),
        }
    raise ScheduleDefinitionError(ScheduleError.INVALID_FREQUENCY)


def _interval_trigger(frequency: ScheduleFrequencyData, timezone: str) -> object:
    module = __import__('apscheduler.triggers.interval', fromlist=['IntervalTrigger'])
    trigger_type = cast(Callable[..., object], getattr(module, 'IntervalTrigger'))
    seconds = frequency.value
    if (
        isinstance(seconds, bool)
        or not isinstance(seconds, (int, float))
        or seconds <= 0
    ):
        raise ScheduleDefinitionError(ScheduleError.INVALID_FREQUENCY)
    return trigger_type(seconds=seconds, timezone=frequency.timezone or timezone)


def _time_fields(values: Mapping[str, object]) -> dict[str, object]:
    time = values.get('time', '00:00')
    if not isinstance(time, str) or ':' not in time:
        raise ScheduleDefinitionError(ScheduleError.INVALID_TIME)
    hour, minute = time.split(':', 1)
    return {'hour': int(hour), 'minute': int(minute)}


def _values(value: object | None) -> Mapping[str, object]:
    if isinstance(value, Mapping):
        return cast(Mapping[str, object], value)
    return {}
