from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ScheduleFrequencyData:
    kind: str = 'interval'
    value: object | None = None
    timezone: str | None = None
