from __future__ import annotations

from enum import Enum
import inspect
from typing import override

from armaden.framework.protocols.container_protocol import ContainerProtocol
from armaden.framework.runtime.supervisor.task.dto.task_graph_data import TaskGraph
from armaden.framework.protocols.task_protocol import (
    TaskProtocol,
)
from armaden.framework.protocols.task_runtime_protocol import (
    TaskRuntimeProtocol,
)
from armaden.framework.protocols.task_injector_protocol import TaskInjectorProtocol


class TaskInjector(TaskInjectorProtocol[TaskGraph]):
    def __init__(self, container: ContainerProtocol | None) -> None:
        self._container: ContainerProtocol | None = container

    @override
    async def resolve(
        self,
        task: TaskProtocol[Enum],
        method: object,
        graph: TaskGraph,
        runtime: TaskRuntimeProtocol,
    ) -> dict[str, object]:
        _ = graph
        if not callable(method):
            return {}
        kwargs: dict[str, object] = {}
        for name, parameter in inspect.signature(method).parameters.items():
            annotation = parameter.annotation
            if annotation is inspect.Parameter.empty:
                continue
            if annotation is TaskRuntimeProtocol:
                kwargs[name] = runtime
                continue
            if self._container is not None:
                try:
                    kwargs[name] = self._container.make(annotation)
                except Exception:
                    continue
        _ = task
        return kwargs
