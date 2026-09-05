from __future__ import annotations

from typing import cast, override

from returns.result import Success

from armaden.framework.protocols.event_listener_registry_protocol import (
    EventListenerRegistryProtocol,
)
from armaden.framework.runtime.events.dto.event_listener_registration_data import (
    EventListenerRegistrationData,
)
from armaden.framework.types.result import Result


class EventListenerRegistry(EventListenerRegistryProtocol):
    def __init__(self) -> None:
        self._listeners: dict[type[object], list[EventListenerRegistrationData]] = {}


    @override
    def forget(self, event_type: type[object]) -> None:
        _ = self._listeners.pop(event_type, None)


    @override
    def has_listeners(self, event_type: type[object]) -> bool:
        return bool(self._listeners.get(event_type))


    @override
    def listeners(self, event_type: type[object]) -> list[object]:
        registrations = self._listeners.get(event_type, [])
        return cast(list[object], list(registrations))


    @override
    def register(
        self,
        event_type: type[object],
        listener: object,
        method: str,
    ) -> Result[None]:
        registration = EventListenerRegistrationData(
            event_type=event_type,
            listener=listener,
            method=method,
        )
        self._listeners.setdefault(event_type, []).append(registration)
        return Success(None)
