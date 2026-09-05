from enum import StrEnum


class FilesystemFactoryError(StrEnum):
    MISSING_DRIVER = "filesystem configuration is missing a 'driver' key"
    UNSUPPORTED_DRIVER = 'filesystem driver is unsupported'
