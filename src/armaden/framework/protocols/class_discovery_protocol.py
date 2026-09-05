from typing import Protocol

from armaden.framework.types.result import Result


class ClassDiscoveryProtocol(Protocol):
    def discover(self, paths: list[str]) -> Result[list[type[object]]]: ...
