from dataclasses import dataclass
from datetime import datetime

from armaden.framework.runtime.schedule.dto.scheduled_event_definition_data import (
    ScheduledEventDefinitionData,
)


@dataclass(frozen=True, slots=True)
class ScheduleInspectionData:
    definition: ScheduledEventDefinitionData
    last_error: str | None = None
    last_finished_at: datetime | None = None
    last_started_at: datetime | None = None
    last_duration_seconds: float | None = None
    last_status: str | None = None
    next_run_at: datetime | None = None
    paused: bool = False
    run_count: int = 0
    skipped_count: int = 0
