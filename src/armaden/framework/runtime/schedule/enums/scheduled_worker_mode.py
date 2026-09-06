from enum import StrEnum


class ScheduledWorkerMode(StrEnum):
    SHARED = 'shared'
    EXCLUSIVE = 'exclusive'
