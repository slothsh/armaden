from enum import StrEnum


class FileCacheDriverError(StrEnum):
    OPERATION_FAILED = 'file cache operation failed'
    MISSING_FILESYSTEM = 'file cache driver requires a filesystem'
    MISSING_STORE_RESOLVER = 'file cache driver requires a store resolver'
