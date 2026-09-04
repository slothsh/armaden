from enum import StrEnum


class SubprocessHandleState(StrEnum):
    STARTING = 'starting'
    RUNNING = 'running'
    STOPPING = 'stopping'
    STOPPED = 'stopped'