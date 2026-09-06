from dataclasses import dataclass, field

from armaden.framework.types.schedule import ScheduleCondition


@dataclass(frozen=True, slots=True)
class ScheduleConstraintData:
    days: tuple[int, ...] = ()
    environments: tuple[str, ...] = ()
    skip: tuple[ScheduleCondition, ...] = field(default_factory=tuple)
    start_time: str | None = None
    end_time: str | None = None
    unless_start_time: str | None = None
    unless_end_time: str | None = None
    when: tuple[ScheduleCondition, ...] = field(default_factory=tuple)
    weekdays_only: bool = False
    weekends_only: bool = False
