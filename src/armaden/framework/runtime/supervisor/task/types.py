from armaden.framework.error.protocols.error_protocol import ErrorProtocol
from armaden.framework.runtime.supervisor.task.protocols.task_runtime_protocol import TaskRuntimeProtocol
from collections.abc import Callable, Coroutine
from returns.result import Result
from typing import Any


type TaskCallback = Callable[
    [TaskRuntimeProtocol],
    Coroutine[Any, Any, Result[None, ErrorProtocol]]
]

type TaskStatusCallback = Callable[
    [TaskRuntimeProtocol],
    Coroutine[Any, Any, Result[dict[str, Any], ErrorProtocol]]
]
