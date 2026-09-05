from typing import Protocol

from armaden.framework.protocols.event_dispatcher_protocol import (
    EventDispatcherProtocol,
)


class EventSubscriberProtocol(Protocol):
    def subscribe(self, dispatcher: EventDispatcherProtocol) -> object: ...
