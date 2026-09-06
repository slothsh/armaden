from dataclasses import dataclass, field

from armaden.framework.runtime.schedule.dto.schedule_constraint_data import ScheduleConstraintData
from armaden.framework.runtime.schedule.dto.schedule_execution_options_data import (
    ScheduleExecutionOptionsData,
)
from armaden.framework.runtime.schedule.dto.schedule_frequency_data import ScheduleFrequencyData
from armaden.framework.runtime.schedule.dto.schedule_hook_data import ScheduleHookData
from armaden.framework.runtime.schedule.enums import ScheduledEventKind
from armaden.framework.types.schedule import ScheduleTag


@dataclass(frozen=True, slots=True)
class ScheduledEventDefinitionData:
    kind: ScheduledEventKind
    target: object
    constraints: ScheduleConstraintData = field(default_factory=ScheduleConstraintData)
    description: str | None = None
    execution: ScheduleExecutionOptionsData = field(
        default_factory=ScheduleExecutionOptionsData,
    )
    frequency: ScheduleFrequencyData = field(default_factory=ScheduleFrequencyData)
    hooks: ScheduleHookData = field(default_factory=ScheduleHookData)
    name: str | None = None
    tags: tuple[ScheduleTag, ...] = field(default_factory=tuple)
