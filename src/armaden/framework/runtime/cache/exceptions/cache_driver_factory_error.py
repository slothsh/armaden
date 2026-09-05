from enum import StrEnum


class CacheDriverFactoryError(StrEnum):
    MISSING_DRIVER = "cache store configuration is missing a 'driver' key"
    UNSUPPORTED_DRIVER = 'cache store driver is unsupported'
