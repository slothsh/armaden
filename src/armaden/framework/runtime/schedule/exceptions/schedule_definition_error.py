from armaden.framework.runtime.schedule.exceptions.schedule_error import ScheduleError


class ScheduleDefinitionError(ValueError):
    def __init__(self, kind: ScheduleError, message: str | None = None) -> None:
        self.kind: ScheduleError = kind
        super().__init__(message or kind.value)
