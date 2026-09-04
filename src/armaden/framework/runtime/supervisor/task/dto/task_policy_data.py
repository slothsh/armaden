from dataclasses import dataclass

from armaden.framework.runtime.supervisor.task.enums.task_restart_policy import TaskRestartPolicy


@dataclass
class TaskPolicy:
    continue_on_failure: bool = False
    priority: int = 0
    ready_timeout: float | None = None
    restart: TaskRestartPolicy = TaskRestartPolicy.NEVER
    retries: int = 0
    retry_backoff: float = 2.0
    retry_delay: float = 1.0
    timeout: float | None = None
