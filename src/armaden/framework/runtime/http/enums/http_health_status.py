from enum import StrEnum


class HttpHealthStatus(StrEnum):
    DEGRADED = 'DEGRADED'
    OK = 'OK'
    UNKNOWN = 'UNKNOWN'
    UNAVAILABLE = 'UNAVAILABLE'
