from __future__ import annotations

from typing import override

from armaden.framework.protocols.task_graph_compiler_protocol import (
    TaskGraphCompilerProtocol,
)
from armaden.framework.protocols.task_protocol import TaskProtocol
from armaden.framework.runtime.supervisor.task.dto.task_graph_data import TaskGraph


class TaskGraphCompiler(TaskGraphCompilerProtocol[TaskGraph]):
    @override
    def compile(self, tasks: list[TaskProtocol]) -> TaskGraph:
        graph = TaskGraph()
        self._resolve_names(tasks, graph)
        self._collect_dependencies(graph)
        self._layer(graph)
        return graph

    def _collect_dependencies(self, graph: TaskGraph) -> None:
        for name, task in graph.tasks.items():
            dependencies = list(task.depends_on or []) + list(task.awaits or [])
            for reference in dependencies:
                dependency_name = self._resolve_dependency_ref(reference, graph, name)
                if dependency_name == name:
                    continue
                graph.adjacency[name].add(dependency_name)
                graph.reverse_adjacency[dependency_name].add(name)

    def _layer(self, graph: TaskGraph) -> None:
        remaining = set(graph.tasks)
        in_degree = {name: len(graph.adjacency[name]) for name in graph.tasks}
        while remaining:
            layer = sorted(name for name in remaining if in_degree[name] == 0)
            if not layer:
                raise RuntimeError('Task graph contains a cycle.')
            graph.layers.append(layer)
            for name in layer:
                remaining.remove(name)
                for dependent in graph.reverse_adjacency[name]:
                    in_degree[dependent] -= 1

    def _resolve_dependency_ref(
        self,
        reference: str | type[object],
        graph: TaskGraph,
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

    def _resolve_names(self, tasks: list[TaskProtocol], graph: TaskGraph) -> None:
        for task in tasks:
            name = task.name or type(task).__name__
            if name in graph.tasks:
                raise RuntimeError(f"Duplicate task name '{name}'.")
            graph.tasks[name] = task
            graph.adjacency[name] = set()
            graph.reverse_adjacency[name] = set()
