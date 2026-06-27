from enum import StrEnum
from typing import Any, Mapping, Protocol

class SupervisorRequestInterface(Protocol):
    @property
    def kind(self) -> StrEnum: ...

    @property
    def task_id(self) -> int: ...

    @property
    def args(self) -> Mapping[str, Any] | None: ...
