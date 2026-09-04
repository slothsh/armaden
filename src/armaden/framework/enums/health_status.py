from enum import StrEnum


class HealthStatus(StrEnum):
    DEGRADED = 'DEGRADED'
    OK = 'OK'
    UNKNOWN = 'UNKNOWN'
    UNAVAILABLE = 'UNAVAILABLE'