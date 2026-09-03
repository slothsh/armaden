from dataclasses import dataclass


@dataclass(frozen=True)
class TaskRecordData:
    task_id: int
    name: str | None
    description: str | None
    status: str
