from enum import StrEnum


class TaskThreadingPolicy(StrEnum):
    EXCLUSIVE = 'exclusive'
    SHARED = 'shared'
