from enum import StrEnum


class DatabaseProviderError(StrEnum):
    CONNECTION_RESOLVER_UNAVAILABLE = 'database connection resolver is unavailable'
    INVALID_CONFIGURATION = 'database configuration is invalid'
    UNSUPPORTED_DRIVER = 'database driver is unsupported'
