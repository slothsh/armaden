from typing import Protocol

from armaden.framework.types.result import Result


class DiscoveryBinderProtocol(Protocol):
    def bind(self, classes: list[type[object]]) -> Result[None]: ...
