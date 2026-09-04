from dataclasses import dataclass

from armaden.framework.types.task import TaskCallback, TaskStatusCallback


@dataclass
class BuiltTaskCallbacksData:
    initialize: TaskCallback | None = None
    run: TaskCallback | None = None
    shutdown: TaskCallback | None = None
    status: TaskStatusCallback | None = None
