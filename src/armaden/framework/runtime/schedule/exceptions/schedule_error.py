from enum import StrEnum


class ScheduleError(StrEnum):
    DUPLICATE_NAME = 'a schedule with this name is already registered'
    INVALID_DEFINITION = 'the scheduled definition is invalid'
    INVALID_FREQUENCY = 'the scheduled frequency is invalid'
    INVALID_TIME = 'the scheduled time is invalid'
    MISSING_NAME = 'the scheduled definition requires a name'
    REGISTRATION_FAILED = 'the scheduled definition could not be registered'
