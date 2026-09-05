from collections.abc import Callable
from typing import Protocol, Self


class QueueableEventListenerProtocol(Protocol):
    connection: str | None
    delay: int | None
    queue: str

    @property
    def callback(self) -> Callable[..., object]: ...

    def __call__(self, event: object) -> object: ...

    def on_connection(self, connection: str) -> Self: ...

    def on_queue(self, queue: str) -> Self: ...

    def with_delay(self, delay: int) -> Self: ...
