from enum import StrEnum


class ConcurrencyMode(StrEnum):
    PARALLEL = 'parallel'
    SEQUENTIAL = 'sequential'