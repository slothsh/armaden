from typing import ClassVar, Protocol


class EventProtocol(Protocol):
    event_marker: ClassVar[bool]
