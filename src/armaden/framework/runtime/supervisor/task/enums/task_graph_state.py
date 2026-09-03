from enum import StrEnum


class TaskGraphState(StrEnum):
    COMPLETED = 'completed'
    FAILED = 'failed'
    PENDING = 'pending'
    RUNNING = 'running'
