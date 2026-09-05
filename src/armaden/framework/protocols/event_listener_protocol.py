from typing import Protocol


class EventListenerProtocol(Protocol):
    def handle(self, event: object) -> object: ...
