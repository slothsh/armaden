from enum import StrEnum


class ArmaReforgerHealthStatus(StrEnum):
    DEGRADED = 'DEGRADED'
    OK = 'OK'
    UNKNOWN = 'UNKNOWN'
    UNAVAILABLE = 'UNAVAILABLE'
