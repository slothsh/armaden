from collections.abc import Mapping
from typing import Protocol

from armaden.framework.types.result import Result


class ConfigurationProtocol(Protocol):
    def all(self) -> Mapping[str, object]: ...

    def get(self, key: str, default: object | None = None) -> object | None: ...

    def load(self) -> Result[None]: ...