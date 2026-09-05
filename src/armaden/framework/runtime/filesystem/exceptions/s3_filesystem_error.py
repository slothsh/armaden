from enum import StrEnum


class S3FilesystemError(StrEnum):
    OPERATION_FAILED = 'S3 filesystem operation failed'
    PATH_OUTSIDE_ROOT = 'S3 filesystem path contains an invalid traversal segment'
