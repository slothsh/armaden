from enum import StrEnum


class FileCacheIndexError(StrEnum):
    INVALID_DATA = 'file cache index data is invalid'
    PERSIST_FAILED = 'file cache index persistence failed'
