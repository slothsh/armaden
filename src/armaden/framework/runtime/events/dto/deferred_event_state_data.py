from dataclasses import dataclass

from armaden.framework.protocols.event_protocol import EventProtocol


@dataclass(slots=True)
class DeferredEventStateData:
    events: list[EventProtocol]
    event_types: frozenset[type[EventProtocol]] | None = None
