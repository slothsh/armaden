from __future__ import annotations

import inspect
from enum import Enum, StrEnum
from typing import ClassVar, get_args, get_origin, get_type_hints, override

from armaden.framework.runtime.error.error import Error
from armaden.framework.protocols.container_protocol import ContainerProtocol
from armaden.framework.protocols.task_injector_protocol import TaskInjectorProtocol
from armaden.framework.protocols.task_protocol import TaskProtocol
from armaden.framework.protocols.task_runtime_protocol import TaskRuntimeProtocol
from returns.result import Failure

from armaden.framework.runtime.supervisor.task.dto.task_graph_data import TaskGraphData
from armaden.framework.runtime.supervisor.task.tags import (
    LifecycleTag,
    PipelineTag,
    UnresolvedSentinelTag,
)


class TaskInjectorError(StrEnum):
    REQUEST_NOT_FULFILLED = 'the task injector request could not be fulfilled'


class TaskInjector(TaskInjectorProtocol[TaskGraphData]):
    _UNRESOLVED: ClassVar[UnresolvedSentinelTag] = UnresolvedSentinelTag()

    def __init__(self, container: ContainerProtocol | None) -> None:
        self._container: ContainerProtocol | None = container

    def _get_type_hints(self, method: object) -> dict[str, object]:
        if not callable(method):
            return {}
        try:
            return get_type_hints(method)
        except (NameError, TypeError):
            return {}

    def _is_lifecycle_origin(self, origin: object) -> bool:
        return origin is LifecycleTag

    def _is_pipeline_origin(self, origin: object) -> bool:
        return origin is PipelineTag

    def _resolve_lifecycle(
        self,
        task: TaskProtocol[Enum],
        graph: TaskGraphData,
        parameter_name: str,
    ) -> object:
        dependencies = graph.lifecycle_deps.get(task.name, {})
        if parameter_name not in dependencies:
            return self._UNRESOLVED

        source_name = self._resolve_task_name(
            dependencies[parameter_name],
            graph,
            task.name,
        )
        if source_name not in graph.lifecycle_signals:
            return Failure(Error(
                TaskInjectorError.REQUEST_NOT_FULFILLED,
                details={
                    'message': f"Lifecycle signal for '{source_name}' not available",
                },
            ))
        return graph.lifecycle_signals[source_name]

    def _resolve_parameter(
        self,
        annotation: object,
        task: TaskProtocol[Enum],
        graph: TaskGraphData,
        parameter_name: str,
        runtime: TaskRuntimeProtocol,
    ) -> object:
        origin = get_origin(annotation)
        args = get_args(annotation)
        if self._is_pipeline_origin(origin) and len(args) == 2 and isinstance(args[0], type):
            return self._resolve_pipeline(task, graph, parameter_name, args[0])
        if self._is_lifecycle_origin(origin) and len(args) == 1 and isinstance(args[0], type):
            return self._resolve_lifecycle(task, graph, parameter_name)
        if annotation is TaskRuntimeProtocol:
            return runtime
        if self._container is None:
            return self._UNRESOLVED
        try:
            return self._container.make(annotation)
        except Exception:
            return self._UNRESOLVED

    def _resolve_pipeline(
        self,
        task: TaskProtocol[Enum],
        graph: TaskGraphData,
        parameter_name: str,
        source_type: type[object],
    ) -> object:
        dependencies = graph.pipeline_deps.get(task.name, {})
        if parameter_name not in dependencies:
            return self._UNRESOLVED
        source_name = self._resolve_task_name(source_type, graph, task.name)
        if source_name not in graph.outputs:
            return self._UNRESOLVED
        return graph.outputs[source_name]

    def _resolve_task_name(
        self,
        reference: str | type[object],
        graph: TaskGraphData,
        task_name: str,
    ) -> str:
        if isinstance(reference, str):
            if reference not in graph.tasks:
                raise RuntimeError(
                    f"Task '{task_name}' depends on unknown task '{reference}'."
                )
            return reference
        matches = [
            name for name, candidate in graph.tasks.items()
            if isinstance(candidate, reference)
        ]
        if len(matches) != 1:
            raise RuntimeError(f"Unable to resolve dependency for task '{task_name}'.")
        return matches[0]

    @override
    async def resolve(
        self,
        task: TaskProtocol[Enum],
        method: object,
        graph: TaskGraphData,
        runtime: TaskRuntimeProtocol,
    ) -> dict[str, object]:
        if not callable(method):
            return {}

        hints = self._get_type_hints(method)
        kwargs: dict[str, object] = {}
        for name, parameter in inspect.signature(method).parameters.items():
            if parameter.kind in (
                inspect.Parameter.VAR_POSITIONAL,
                inspect.Parameter.VAR_KEYWORD,
            ):
                continue
            annotation = hints.get(name, parameter.annotation)
            if annotation is inspect.Parameter.empty:
                continue
            value = self._resolve_parameter(
                annotation,
                task,
                graph,
                name,
                runtime,
            )
            if value is not self._UNRESOLVED:
                kwargs[name] = value
        return kwargs
