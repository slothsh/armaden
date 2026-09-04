from enum import Enum
from typing import Protocol, Self

from armaden.framework.protocols.task_protocol import TaskProtocol


class ConcurrencyBuilderProtocol[E: Enum, G](Protocol):
    def build(self) -> list[TaskProtocol[E]]: ...

    def continue_on_failure(self) -> Self: ...

    def max_concurrency(self, value: int) -> Self: ...

    def submit(self) -> G: ...