from enum import StrEnum


class SupervisorRequestKind(StrEnum):
    RESTART = 'restart'
    SHUTDOWN = 'shutdown'
