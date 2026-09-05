from typing import Protocol

from armaden.framework.types.result import Result


class EventListenerDiscoveryProtocol(Protocol):
    def discover(self, paths: list[str]) -> Result[list[object]]: ...
