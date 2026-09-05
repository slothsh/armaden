from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from uuid import uuid4

from armaden.framework.runtime.error.error import Error
from armaden.framework.protocols.task_protocol import TaskProtocol
from armaden.framework.runtime.supervisor.task.enums.task_graph_state import TaskGraphState
from armaden.framework.types.result import Result


@dataclass
class TaskGraphData:
    adjacency: dict[str, set[str]] = field(default_factory=dict)
    errors: list[Error] = field(default_factory=list)
    graph_id: str = field(default_factory=lambda: str(uuid4()))
    layers: list[list[str]] = field(default_factory=list)
    lifecycle_deps: dict[str, dict[str, type[object]]] = field(default_factory=dict)
    lifecycle_signals: dict[str, Result[None]] = field(default_factory=dict)
    max_concurrency: int | None = None
    outputs: dict[str, Result[object]] = field(default_factory=dict)
    pipeline_deps: dict[str, dict[str, tuple[type[object], type[object]]]] = field(default_factory=dict)
    reverse_adjacency: dict[str, set[str]] = field(default_factory=dict)
    state: TaskGraphState = TaskGraphState.PENDING
    tasks: dict[str, TaskProtocol[Enum]] = field(default_factory=dict)

    @property
    def shutdown_order(self) -> list[str]:
        ordered: list[str] = []
        for layer in reversed(self.layers):
            ordered.extend(layer)
        return ordered
