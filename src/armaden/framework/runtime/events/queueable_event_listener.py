from collections.abc import Callable
from typing import Self, override

from armaden.framework.protocols.event_queueable_listener_protocol import (
    QueueableEventListenerProtocol,
)


class QueueableEventListener(QueueableEventListenerProtocol):
    def __init__(self, callback: Callable[..., object]) -> None:
        self._callback: Callable[..., object] = callback
        self.connection: str | None = None
        self.delay: int | None = None
        self.queue: str = 'default'


    @override
    def __call__(self, event: object) -> object:
        return self._callback(event)


    @override
    def on_connection(self, connection: str) -> Self:
        self.connection = connection
        return self


    @override
    def on_queue(self, queue: str) -> Self:
        self.queue = queue
        return self


    @override
    def with_delay(self, delay: int) -> Self:
        self.delay = delay
        return self


    @property
    @override
    def callback(self) -> Callable[..., object]:
        return self._callback
