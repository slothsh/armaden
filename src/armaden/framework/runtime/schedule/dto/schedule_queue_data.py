from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ScheduleQueueData:
    connection: str | None = None
    name: str | None = None
    priority: int = 0
