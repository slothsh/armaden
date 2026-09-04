from enum import Enum
from typing import override

from armaden.framework.protocols.concurrency_builder_protocol import (
    ConcurrencyBuilderProtocol,
)
from armaden.framework.protocols.supervisor_protocol import SupervisorProtocol
from armaden.framework.protocols.task_protocol import TaskProtocol
from armaden.framework.runtime.supervisor.task.dto.task_graph_data import TaskGraphData
from armaden.framework.runtime.supervisor.task.enums.concurrency_mode import ConcurrencyMode


class ConcurrencyBuilder(ConcurrencyBuilderProtocol[Enum, TaskGraphData]):
    def __init__(
        self,
        supervisor: SupervisorProtocol[TaskGraphData],
        tasks: list[TaskProtocol[Enum]],
        mode: ConcurrencyMode,
    ) -> None:
        if not tasks:
            raise ValueError('ConcurrencyBuilder requires at least one task')

        self._max_concurrency: int | None = None
        self._mode: ConcurrencyMode = mode
        self._supervisor: SupervisorProtocol[TaskGraphData] = supervisor
        self._tasks: list[TaskProtocol[Enum]] = list(tasks)

        if mode is ConcurrencyMode.SEQUENTIAL:
            self._add_sequential_dependencies()


    def _add_sequential_dependencies(self) -> None:
        for index in range(1, len(self._tasks)):
            previous_name = self._tasks[index - 1].name
            task = self._tasks[index]
            dependencies = task.depends_on
            if dependencies is None:
                dependencies = []
                task.depends_on = dependencies
            if previous_name not in dependencies:
                dependencies.append(previous_name)


    @override
    def build(self) -> list[TaskProtocol[Enum]]:
        return list(self._tasks)


    @override
    def continue_on_failure(self) -> ConcurrencyBuilder:
        for task in self._tasks:
            task.policy.continue_on_failure = True
        return self


    @override
    def max_concurrency(self, value: int) -> ConcurrencyBuilder:
        self._max_concurrency = value
        return self


    @override
    def submit(self) -> TaskGraphData:
        graph = self._supervisor.submit(self.build())
        if self._max_concurrency is not None:
            graph.max_concurrency = self._max_concurrency
        return graph