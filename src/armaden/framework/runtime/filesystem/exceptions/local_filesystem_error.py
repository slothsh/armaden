from enum import StrEnum


class LocalFilesystemError(StrEnum):
    OPERATION_FAILED = 'local filesystem operation failed'
    PATH_OUTSIDE_ROOT = 'local filesystem path is outside the configured root'
