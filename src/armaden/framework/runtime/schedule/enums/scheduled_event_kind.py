from enum import StrEnum


class ScheduledEventKind(StrEnum):
    CALL = 'call'
    EXEC = 'exec'
    JOB = 'job'
