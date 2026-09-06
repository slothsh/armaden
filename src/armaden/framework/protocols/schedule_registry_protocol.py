from typing import Protocol

from armaden.framework.types.result import Result
from armaden.framework.types.schedule import ScheduleTag


class ScheduleRegistryProtocol[D, I](Protocol):
    def definitions(
        self,
        tag: ScheduleTag | None = None,
    ) -> list[I]: ...

    def register(
        self,
        definition: D,
    ) -> Result[I]: ...

    def pause(self, name: str) -> Result[None]: ...

    def remove(self, name: str) -> Result[None]: ...

    def resume(self, name: str) -> Result[None]: ...

    def shutdown(self) -> Result[None]: ...

    def start(self) -> Result[None]: ...
