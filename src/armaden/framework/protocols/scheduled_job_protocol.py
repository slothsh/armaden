from collections.abc import Awaitable
from typing import ClassVar, Protocol


class ScheduledJobProtocol(Protocol):
    connection: ClassVar[str | None]
    priority: ClassVar[int]
    queue: ClassVar[str | None]
    schedule: ClassVar[object | None]
    tags: ClassVar[tuple[str, ...]]

    def handle(self, *args: object, **kwargs: object) -> object | Awaitable[object]: ...
