from dataclasses import dataclass

from armaden.framework.runtime.schedule.dto.schedule_queue_data import ScheduleQueueData
from armaden.framework.runtime.schedule.enums import ScheduledWorkerMode


@dataclass(frozen=True, slots=True)
class ScheduleExecutionOptionsData:
    append_output_path: str | None = None
    even_in_maintenance_mode: bool = False
    on_one_server: bool = False
    output_path: str | None = None
    queue: ScheduleQueueData | None = None
    run_in_background: bool = False
    worker_mode: ScheduledWorkerMode = ScheduledWorkerMode.SHARED
    without_overlapping_minutes: int | None = None
