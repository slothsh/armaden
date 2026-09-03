from typing import TYPE_CHECKING

from armaden.framework.runtime.task_graph import TaskGraph

if TYPE_CHECKING:
    from armaden.framework.runtime.supervisor import Supervisor
    from armaden.framework.runtime.task import Task


class ConcurrencyBuilder:
    def __init__(self, supervisor: 'Supervisor', tasks: list['Task'], mode: str) -> None:
        if not tasks:
            raise ValueError('ConcurrencyBuilder requires at least one task')

        self._supervisor = supervisor
        self._tasks = list(tasks)
        self._mode = mode
        self._max_concurrency: int | None = None

        if mode == 'sequential':
            for i in range(1, len(self._tasks)):
                prev_name = self._tasks[i - 1].name
                if prev_name not in self._tasks[i].depends_on:
                    self._tasks[i].depends_on.append(prev_name)

    def max_concurrency(self, n: int) -> 'ConcurrencyBuilder':
        self._max_concurrency = n
        return self

    def continue_on_failure(self) -> 'ConcurrencyBuilder':
        for task in self._tasks:
            task.policy.continue_on_failure = True
        return self

    def build(self) -> list['Task']:
        return list(self._tasks)

    def submit(self) -> TaskGraph:
        graph = self._supervisor.submit(self.build())
        if self._max_concurrency is not None:
            graph.max_concurrency = self._max_concurrency
        return graph
