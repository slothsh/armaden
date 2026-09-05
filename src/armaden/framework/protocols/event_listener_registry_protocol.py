from typing import Protocol

from armaden.framework.types.result import Result


class EventListenerRegistryProtocol(Protocol):
    def forget(self, event_type: type[object]) -> None: ...

    def has_listeners(self, event_type: type[object]) -> bool: ...

    def listeners(self, event_type: type[object]) -> list[object]: ...

    def register(
        self,
        event_type: type[object],
        listener: object,
        method: str,
    ) -> Result[None]: ...
