from enum import StrEnum


class TaskError(StrEnum):
    TIMEOUT = 'task execution timed out'
    MAX_RETRIES_EXCEEDED = 'task exceeded maximum retry attempts'
    READY_TIMEOUT = 'long-running task failed to signal ready within timeout'
    UNRESOLVED_DEPENDENCY = 'a task dependency could not be resolved'
    CYCLE_DETECTED = 'a cycle was detected in the task graph'
    DUPLICATE_NAME = 'a duplicate task name was encountered'
    SUBPROCESS_ERROR = 'a non-zero exit code occurred when running a subprocess'
    INITIALIZATION_FAILED = 'an error occurred while initializing the supervisor'
    REQUEST_IGNORED = 'the provided request has been ignored'
    BAD_REQUEST_DATA = 'the provided supervisor request data is invalid'
    REQUEST_NOT_FULFILLED = 'the specified request could not be fulfilled'


class TaskGraphCycleError(Exception):
    def __init__(self, cycle_path: list[str]) -> None:
        self.cycle_path = cycle_path
        super().__init__(f'Cycle detected in task graph: {" -> ".join(cycle_path)}')


class UnresolvedDependencyError(Exception):
    def __init__(self, task_name: str, dep_ref: str | type) -> None:
        self.task_name = task_name
        self.dep_ref = dep_ref
        ref = dep_ref if isinstance(dep_ref, str) else getattr(dep_ref, '__name__', str(dep_ref))
        super().__init__(f"Task '{task_name}' has unresolved dependency '{ref}'")


class DuplicateTaskNameError(Exception):
    def __init__(self, name: str, task_types: list[str]) -> None:
        self.name = name
        self.task_types = task_types
        super().__init__(
            f"Duplicate task name '{name}' used by tasks: {', '.join(task_types)}"
        )
