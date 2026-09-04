from enum import Enum
from typing import Protocol, Self

from armaden.framework.protocols.task_protocol import TaskProtocol
from armaden.framework.types.task import TaskCallback


class ScheduleBuilderProtocol[E: Enum, G](Protocol):
    def action(self, callback: TaskCallback) -> Self: ...

    def awaits(self, *references: str | type[object]) -> Self: ...

    def build(self) -> TaskProtocol[E]: ...

    def depends_on(self, *references: str | type[object]) -> Self: ...

    def retries(
        self,
        count: int,
        delay: float = 1.0,
        backoff: float = 2.0,
    ) -> Self: ...

    def submit(self) -> G: ...

    def timeout(self, seconds: float) -> Self: ...