from enum import StrEnum


class ClassDiscoveryError(StrEnum):
    PATH_UNAVAILABLE = 'a configured discovery path is unavailable'
