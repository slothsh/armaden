from typing import Protocol

from armaden.framework.types.result import Result


class ScheduledJobDiscoveryProtocol(Protocol):
    def discover(self, paths: list[str]) -> Result[list[type[object]]]: ...
