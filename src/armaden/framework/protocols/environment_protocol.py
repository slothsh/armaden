from typing import Protocol

from armaden.framework.types.result import Result


class EnvironmentProtocol(Protocol):
    @property
    def environment(self) -> str: ...

    def get(self, name: str, default: str | None = None) -> str | None: ...

    def initialize(self) -> Result[None]: ...