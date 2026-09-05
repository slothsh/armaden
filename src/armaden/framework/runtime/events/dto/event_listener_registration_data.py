from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class EventListenerRegistrationData:
    event_type: type[object]
    listener: object
    method: str
