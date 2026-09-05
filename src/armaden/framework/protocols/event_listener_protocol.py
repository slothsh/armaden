from typing import Protocol

from armaden.framework.protocols.event_protocol import EventProtocol


class EventListenerProtocol[E: EventProtocol](Protocol):
    def handle(self, event: E) -> object: ...
