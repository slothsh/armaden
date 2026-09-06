from dataclasses import dataclass, field

from armaden.framework.types.schedule import ScheduleHook


@dataclass(frozen=True, slots=True)
class ScheduleHookData:
    after: tuple[ScheduleHook, ...] = field(default_factory=tuple)
    before: tuple[ScheduleHook, ...] = field(default_factory=tuple)
    on_failure: tuple[ScheduleHook, ...] = field(default_factory=tuple)
    on_success: tuple[ScheduleHook, ...] = field(default_factory=tuple)
