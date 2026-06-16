from enum import StrEnum


class HealthStatus(StrEnum):
    OK = 'OK'
    DEGRADED = 'DEGRADED'
    UNAVAILABLE = 'UNAVAILABLE'
    UNKOWN = 'UNKNOWN'
