from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Awaitable
from typing import ClassVar, override

from armaden.framework.protocols.scheduled_job_protocol import ScheduledJobProtocol


class ScheduledJob(ScheduledJobProtocol, ABC):
    connection: ClassVar[str | None] = None
    priority: ClassVar[int] = 0
    schedule: ClassVar[object | None] = None
    queue: ClassVar[str | None] = None
    tags: ClassVar[tuple[str, ...]] = ()


    @override
    @abstractmethod
    def handle(self, *args: object, **kwargs: object) -> object | Awaitable[object]:
        raise NotImplementedError


    def __call__(self, *args: object, **kwargs: object) -> object | Awaitable[object]:
        return self.handle(*args, **kwargs)
