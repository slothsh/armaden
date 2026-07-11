import inspect
import logging
import typing
from dataclasses import dataclass, field
from typing import Any
from uuid import uuid4

from armaden.framework.errors import Error
from armaden.framework.protocols.task import Lifecycle, Pipeline
from armaden.framework.runtime.errors import (
    DuplicateTaskNameError,
    TaskGraphCycleError,
    UnresolvedDependencyError,
)
from armaden.framework.runtime.task import Task
from armaden.framework.utils.types import Result

logger = logging.getLogger(__name__)


class TaskGraphState:
    PENDING = 'pending'
    RUNNING = 'running'
    COMPLETED = 'completed'
    FAILED = 'failed'


@dataclass
class TaskGraph:
    tasks: dict[str, Task] = field(default_factory=dict)
    layers: list[list[str]] = field(default_factory=list)
    outputs: dict[str, Result] = field(default_factory=dict)
    lifecycle_signals: dict[str, Result[None]] = field(default_factory=dict)
    adjacency: dict[str, set[str]] = field(default_factory=dict)
    reverse_adjacency: dict[str, set[str]] = field(default_factory=dict)
    pipeline_deps: dict[str, dict[str, tuple[type, type]]] = field(default_factory=dict)
    lifecycle_deps: dict[str, dict[str, type]] = field(default_factory=dict)
    state: str = TaskGraphState.PENDING
    errors: list[Error] = field(default_factory=list)
    graph_id: str = field(default_factory=lambda: str(uuid4()))
    max_concurrency: int | None = None

    @property
    def shutdown_order(self) -> list[str]:
        ordered: list[str] = []
        for layer in reversed(self.layers):
            ordered.extend(layer)
        return ordered


class TaskGraphCompiler:
    def compile(self, tasks: list[Task]) -> TaskGraph:
        graph = TaskGraph()

        self._resolve_names(tasks, graph)
        self._collect_dependencies(tasks, graph)
        self._detect_cycles(graph)
        self._layer(graph)
        self._validate(graph)

        return graph

    def _resolve_names(self, tasks: list[Task], graph: TaskGraph) -> None:
        for task in tasks:
            name = task.name or type(task).__name__
            if name in graph.tasks:
                existing_type = type(graph.tasks[name]).__name__
                new_type = type(task).__name__
                raise DuplicateTaskNameError(name, [existing_type, new_type])
            task.name = name
            graph.tasks[name] = task
            graph.adjacency.setdefault(name, set())
            graph.reverse_adjacency.setdefault(name, set())
            graph.pipeline_deps.setdefault(name, {})
            graph.lifecycle_deps.setdefault(name, {})

    def _collect_dependencies(self, tasks: list[Task], graph: TaskGraph) -> None:
        _ = tasks
        pipeline_params_by_task = {
            name: self._extract_pipeline_params(task.run) for name, task in graph.tasks.items()
        }
        lifecycle_params_by_task = {
            name: self._extract_lifecycle_params(task.run) for name, task in graph.tasks.items()
        }

        for name, task in graph.tasks.items():
            declared_output_deps = list(task.depends_on or [])
            declared_lifecycle_deps = list(task.awaits or [])

            for param_name, (source_type, output_type) in pipeline_params_by_task[name].items():
                graph.pipeline_deps[name][param_name] = (source_type, output_type)
                declared_output_deps.append(source_type)

            for param_name, source_type in lifecycle_params_by_task[name].items():
                graph.lifecycle_deps[name][param_name] = source_type
                declared_lifecycle_deps.append(source_type)

            seen: set[str] = set()
            for ref in declared_output_deps:
                dep_name = self._resolve_dependency_ref(ref, graph, name)
                if dep_name == name:
                    logger.warning("Task '%s' declares a self-dependency via Pipeline; ignoring edge", name)
                    continue
                if dep_name in seen:
                    continue
                seen.add(dep_name)
                graph.adjacency[name].add(dep_name)
                graph.reverse_adjacency[dep_name].add(name)

            seen_lifecycle: set[str] = set()
            for ref in declared_lifecycle_deps:
                dep_name = self._resolve_dependency_ref(ref, graph, name)
                if dep_name == name:
                    logger.warning("Task '%s' declares a self lifecycle-dependency; ignoring edge", name)
                    continue
                if dep_name in seen_lifecycle:
                    continue
                seen_lifecycle.add(dep_name)
                graph.adjacency[name].add(dep_name)
                graph.reverse_adjacency[dep_name].add(name)

    def _resolve_dependency_ref(self, ref: str | type, graph: TaskGraph, task_name: str) -> str:
        if isinstance(ref, str):
            if ref not in graph.tasks:
                raise UnresolvedDependencyError(task_name, ref)
            return ref

        matches = [name for name, task in graph.tasks.items() if isinstance(task, ref)]
        if not matches:
            raise UnresolvedDependencyError(task_name, ref)
        if len(matches) > 1:
            raise UnresolvedDependencyError(task_name, ref)
        return matches[0]

    def _detect_cycles(self, graph: TaskGraph) -> None:
        WHITE, GRAY, BLACK = 0, 1, 2
        color: dict[str, int] = {name: WHITE for name in graph.tasks}
        path: list[str] = []

        def visit(node: str) -> None:
            color[node] = GRAY
            path.append(node)
            for neighbor in graph.adjacency.get(node, ()):
                if color[neighbor] == GRAY:
                    cycle_start = path.index(neighbor)
                    cycle = path[cycle_start:] + [neighbor]
                    raise TaskGraphCycleError(cycle)
                if color[neighbor] == WHITE:
                    visit(neighbor)
            path.pop()
            color[node] = BLACK

        for name in graph.tasks:
            if color[name] == WHITE:
                visit(name)

    def _layer(self, graph: TaskGraph) -> None:
        in_degree: dict[str, int] = {
            name: len(graph.adjacency.get(name, set())) for name in graph.tasks
        }
        remaining = set(graph.tasks)

        while remaining:
            layer = sorted(
                [name for name in remaining if in_degree[name] == 0],
                key=lambda n: (graph.tasks[n].policy.priority if graph.tasks[n].policy is not None else 0),
            )
            if not layer:
                raise TaskGraphCycleError(sorted(remaining))
            graph.layers.append(layer)
            for name in layer:
                remaining.discard(name)
                for dependent in graph.reverse_adjacency.get(name, set()):
                    in_degree[dependent] -= 1

    def _validate(self, graph: TaskGraph) -> None:
        for name, task in graph.tasks.items():
            if task.long_running and not graph.reverse_adjacency.get(name):
                logger.info("Task '%s' is long-running but has no dependents", name)

    def _get_type_hints(self, func) -> dict[str, Any]:
        try:
            return typing.get_type_hints(func)
        except Exception:
            return {}

    def _extract_pipeline_params(self, method) -> dict[str, tuple[type, type]]:
        params: dict[str, tuple[type, type]] = {}
        hints = self._get_type_hints(method)
        for param_name in inspect.signature(method).parameters:
            annotation = hints.get(param_name)
            if annotation is None:
                continue
            origin = typing.get_origin(annotation)
            if origin is None:
                continue
            if not self._is_pipeline_origin(origin):
                continue
            args = typing.get_args(annotation)
            if len(args) < 2:
                logger.warning("Pipeline annotation on '%s.%s' missing type parameters", method.__qualname__, param_name)
                continue
            params[param_name] = (args[0], args[1])
        return params

    def _extract_lifecycle_params(self, method) -> dict[str, type]:
        params: dict[str, type] = {}
        hints = self._get_type_hints(method)
        for param_name in inspect.signature(method).parameters:
            annotation = hints.get(param_name)
            if annotation is None:
                continue
            origin = typing.get_origin(annotation)
            if origin is None:
                continue
            if not self._is_lifecycle_origin(origin):
                continue
            args = typing.get_args(annotation)
            if len(args) < 1:
                logger.warning("Lifecycle annotation on '%s.%s' missing type parameter", method.__qualname__, param_name)
                continue
            params[param_name] = args[0]
        return params

    def _is_pipeline_origin(self, origin: Any) -> bool:
        try:
            return origin is Pipeline or (isinstance(origin, type) and issubclass(origin, Pipeline))
        except TypeError:
            return False

    def _is_lifecycle_origin(self, origin: Any) -> bool:
        try:
            return origin is Lifecycle or (isinstance(origin, type) and issubclass(origin, Lifecycle))
        except TypeError:
            return False

