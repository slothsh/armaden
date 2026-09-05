from enum import StrEnum


class QueueResolverError(StrEnum):
    CONNECTION_NOT_FOUND = 'the requested queue connection is not configured'
    DEFAULT_CONNECTION_NOT_FOUND = 'the configured default queue connection is not available'
