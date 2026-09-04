from __future__ import annotations

import logging
from enum import Enum
from typing import get_args, get_origin, get_type_hints, override

from armaden.framework.protocols.task_graph_compiler_protocol import (
    TaskGraphCompilerProtocol,
)
from armaden.framework.protocols.task_protocol import TaskProtocol
from armaden.framework.runtime.supervisor.task.dto.task_graph_data import TaskGraphData
from armaden.framework.runtime.supervisor.task.tags import LifecycleTag, PipelineTag

logger = logging.getLogger(__name__)


class TaskGraphCompiler(TaskGraphCompilerProtocol[TaskGraphData]):
    def _add_dependencies(
        self,
        graph: TaskGraphData,
        task_name: str,
        references: list[str | type[object]],
    ) -> None:
        for reference in references:
            dependency_name = self._resolve_dependency_ref(reference, graph, task_name)
            if dependency_name == task_name:
                continue
            graph.adjacency[task_name].add(dependency_name)
            graph.reverse_adjacency[dependency_name].add(task_name)

    def _collect_dependencies(self, graph: TaskGraphData) -> None:
        for name, task in graph.tasks.items():
            pipeline_params = self._extract_pipeline_params(task.run)
            lifecycle_params = self._extract_lifecycle_params(task.run)
            output_dependencies = list(task.depends_on or [])
            lifecycle_dependencies = list(task.awaits or [])

            for parameter_name, dependency in pipeline_params.items():
                graph.pipeline_deps[name][parameter_name] = dependency
                output_dependencies.append(dependency[0])

            for parameter_name, dependency in lifecycle_params.items():
                graph.lifecycle_deps[name][parameter_name] = dependency
                lifecycle_dependencies.append(dependency)

            self._add_dependencies(graph, name, output_dependencies)
            self._add_dependencies(graph, name, lifecycle_dependencies)

    def _extract_lifecycle_params(self, method: object) -> dict[str, type[object]]:
        params: dict[str, type[object]] = {}
        for parameter_name, annotation in self._parameter_hints(method).items():
            origin = get_origin(annotation)
            if not self._is_lifecycle_origin(origin):
                continue
            args = get_args(annotation)
            if len(args) == 1 and isinstance(args[0], type):
                params[parameter_name] = args[0]
        return params

    def _extract_pipeline_params(
        self,
        method: object,
    ) -> dict[str, tuple[type[object], type[object]]]:
        params: dict[str, tuple[type[object], type[object]]] = {}
        for parameter_name, annotation in self._parameter_hints(method).items():
            origin = get_origin(annotation)
            if not self._is_pipeline_origin(origin):
                continue
            args = get_args(annotation)
            if len(args) == 2 and all(isinstance(argument, type) for argument in args):
                params[parameter_name] = (args[0], args[1])
        return params

    def _is_lifecycle_origin(self, origin: object) -> bool:
        return origin is LifecycleTag

    def _is_pipeline_origin(self, origin: object) -> bool:
        return origin is PipelineTag

    def _layer(self, graph: TaskGraphData) -> None:
        remaining = set(graph.tasks)
        in_degree = {name: len(graph.adjacency[name]) for name in graph.tasks}
        while remaining:
            layer = sorted(
                (name for name in remaining if in_degree[name] == 0),
                key=lambda name: (graph.tasks[name].policy.priority, name),
            )
            if not layer:
                raise RuntimeError('Task graph contains a cycle.')
            graph.layers.append(layer)
            for name in layer:
                remaining.remove(name)
                for dependent in graph.reverse_adjacency[name]:
                    in_degree[dependent] -= 1

    def _parameter_hints(self, method: object) -> dict[str, object]:
        if not callable(method):
            return {}
        try:
            return get_type_hints(method)
        except (NameError, TypeError):
            return {}

    def _resolve_dependency_ref(
        self,
        reference: str | type[object],
        graph: TaskGraphData,
        task_name: str,
    ) -> str:
        if isinstance(reference, str):
            if reference not in graph.tasks:
                raise RuntimeError(f"Task '{task_name}' depends on unknown task '{reference}'.")
            return reference
        matches = [
            name for name, task in graph.tasks.items()
            if isinstance(task, reference)
        ]
        if len(matches) != 1:
            raise RuntimeError(f"Unable to resolve dependency for task '{task_name}'.")
        return matches[0]

    def _resolve_names(
        self,
        tasks: list[TaskProtocol[Enum]],
        graph: TaskGraphData,
    ) -> None:
        for task in tasks:
            name = task.name or type(task).__name__
            if name in graph.tasks:
                raise RuntimeError(f"Duplicate task name '{name}'.")
            graph.tasks[name] = task
            graph.adjacency[name] = set()
            graph.lifecycle_deps[name] = {}
            graph.pipeline_deps[name] = {}
            graph.reverse_adjacency[name] = set()

    @override
    def compile(self, tasks: list[TaskProtocol[Enum]]) -> TaskGraphData:
        graph = TaskGraphData()
        self._resolve_names(tasks, graph)
        self._collect_dependencies(graph)
        self._layer(graph)
        return graph
