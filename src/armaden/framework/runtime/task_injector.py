import inspect
import logging
import typing

from returns.result import Failure

from armaden.framework.classes.instance_container import BindingResolutionException
from armaden.framework.errors import Error
from armaden.framework.protocols.task import Lifecycle, Pipeline
from armaden.framework.protocols.task_runtime import TaskRuntimeInterface
from armaden.framework.runtime.errors import TaskError, UnresolvedDependencyError
from armaden.framework.runtime.task import Task
from armaden.framework.runtime.task_graph import TaskGraph

logger = logging.getLogger(__name__)


class TaskInjector:
    def __init__(self, container) -> None:
        self._container = container

    async def resolve(
        self,
        task: Task,
        method,
        graph: TaskGraph,
        runtime: TaskRuntimeInterface,
    ) -> dict:
        kwargs: dict = {}
        method_hints = self._get_type_hints(method)

        for param_name, parameter in inspect.signature(method).parameters.items():
            if parameter.kind in (inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD):
                continue

            annotation = method_hints.get(param_name)
            if annotation is None:
                continue

            value = self._resolve_parameter(
                annotation, task, graph, runtime, param_name, parameter
            )
            if value is _UNRESOLVED:
                continue
            kwargs[param_name] = value

        return kwargs

    def _resolve_parameter(
        self,
        annotation,
        task: Task,
        graph: TaskGraph,
        runtime: TaskRuntimeInterface,
        param_name: str,
        parameter: inspect.Parameter,
    ):
        origin = typing.get_origin(annotation)

        if self._is_pipeline_origin(origin):
            return self._resolve_pipeline(task, graph, param_name)

        if self._is_lifecycle_origin(origin):
            return self._resolve_lifecycle(task, graph, param_name)

        if annotation is TaskRuntimeInterface or parameter.annotation is TaskRuntimeInterface:
            return runtime

        try:
            return self._container.make(annotation)
        except BindingResolutionException:
            logger.warning(
                "Could not resolve parameter '%s' of task '%s' from the container; "
                "leaving it for Python to handle",
                param_name,
                task.name,
            )
            return _UNRESOLVED

    def _resolve_pipeline(self, task: Task, graph: TaskGraph, param_name: str):
        deps = graph.pipeline_deps.get(task.name or '', {})
        if param_name not in deps:
            logger.warning(
                "Task '%s' has a Pipeline parameter '%s' with no recorded dependency",
                task.name, param_name,
            )
            return _UNRESOLVED

        source_type, _output_type = deps[param_name]
        source_name = self._resolve_task_name(source_type, graph, task.name or '')

        if source_name not in graph.outputs:
            logger.error(
                "Pipeline source '%s' for task '%s' has not run yet (should be caught by compiler)",
                source_name, task.name,
            )
            return _UNRESOLVED

        return graph.outputs[source_name]

    def _resolve_lifecycle(self, task: Task, graph: TaskGraph, param_name: str):
        deps = graph.lifecycle_deps.get(task.name or '', {})
        if param_name not in deps:
            logger.warning(
                "Task '%s' has a Lifecycle parameter '%s' with no recorded dependency",
                task.name, param_name,
            )
            return _UNRESOLVED

        source_type = deps[param_name]
        source_name = self._resolve_task_name(source_type, graph, task.name or '')

        if source_name not in graph.lifecycle_signals:
            logger.warning(
                "Lifecycle signal for '%s' (required by '%s') is not available yet",
                source_name, task.name,
            )
            return Failure(Error(
                TaskError.REQUEST_NOT_FULFILLED,
                details={'message': f"Lifecycle signal for '{source_name}' not available"},
            ))

        return graph.lifecycle_signals[source_name]

    def _resolve_task_name(self, ref: str | type, graph: TaskGraph, task_name: str) -> str:
        if isinstance(ref, str):
            if ref not in graph.tasks:
                raise UnresolvedDependencyError(task_name, ref)
            return ref

        matches = [name for name, candidate in graph.tasks.items() if isinstance(candidate, ref)]
        if not matches:
            raise UnresolvedDependencyError(task_name, ref)
        if len(matches) > 1:
            raise UnresolvedDependencyError(task_name, ref)
        return matches[0]

    def _get_type_hints(self, func) -> dict:
        try:
            return typing.get_type_hints(func)
        except Exception:
            return {}

    def _is_pipeline_origin(self, origin) -> bool:
        try:
            return origin is Pipeline or (isinstance(origin, type) and issubclass(origin, Pipeline))
        except TypeError:
            return False

    def _is_lifecycle_origin(self, origin) -> bool:
        try:
            return origin is Lifecycle or (isinstance(origin, type) and issubclass(origin, Lifecycle))
        except TypeError:
            return False


class _UnresolvedSentinel:
    pass


_UNRESOLVED = _UnresolvedSentinel()
