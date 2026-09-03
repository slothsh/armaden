from __future__ import annotations

from typing import Protocol

from armaden.framework.protocols.task_protocol import TaskProtocol


class TaskGraphCompilerProtocol[G](Protocol):
    def compile(self, tasks: list[TaskProtocol]) -> G: ...
