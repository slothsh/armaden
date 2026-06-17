from enum import StrEnum
from typing import Any, Mapping, Protocol

class SupervisorRequestInterface(Protocol):
    @property
    def kind(self) -> StrEnum: ...


    @property
    def args(self) -> Mapping[str, Any] | None: ...
