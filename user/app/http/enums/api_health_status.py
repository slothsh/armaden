from enum import StrEnum


class ApiHealthStatus(StrEnum):
    DEGRADED = 'DEGRADED'
    OK = 'OK'
    UNKNOWN = 'UNKNOWN'
    UNAVAILABLE = 'UNAVAILABLE'
