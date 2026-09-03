from collections.abc import Callable, Coroutine

from armaden.framework.protocols.task_runtime_protocol import TaskRuntimeProtocol
from armaden.framework.types.result import Result


type TaskCallback = Callable[
    [TaskRuntimeProtocol],
    Coroutine[object, object, Result[None]],
]

type TaskStatusCallback = Callable[
    [TaskRuntimeProtocol],
    Coroutine[object, object, Result[dict[str, object]]],
]
