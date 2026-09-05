from enum import StrEnum


class QueueFactoryError(StrEnum):
    MISSING_DRIVER = "queue configuration is missing a 'driver' key"
    UNSUPPORTED_DRIVER = 'queue driver is unsupported'
