from enum import StrEnum


class ServiceProviderHealth(StrEnum):
    DEGRADED = 'DEGRADED'
    OK = 'OK'
    UNKNOWN = 'UNKNOWN'
    UNAVAILABLE = 'UNAVAILABLE'
