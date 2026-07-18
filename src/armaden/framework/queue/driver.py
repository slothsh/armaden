from __future__ import annotations

import time
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from returns.result import Result

if TYPE_CHECKING:
    from armaden.framework.queue.job import Job


class QueueDriver(ABC):
    """Contract for queue backend drivers. Sync, Database, and Cache drivers
    implement this."""

    @abstractmethod
    def push(self, job: 'Job', queue: str = 'default') -> Result[str]:
        raise NotImplementedError

    @abstractmethod
    def later(self, delay: int, job: 'Job', queue: str = 'default') -> Result[str]:
        raise NotImplementedError

    @abstractmethod
    def pop(self, queue: str = 'default') -> Result['Job | None']:
        raise NotImplementedError

    @abstractmethod
    def delete(self, job_id: str, queue: str = 'default') -> Result[None]:
        raise NotImplementedError

    @abstractmethod
    def release(self, job_id: str, delay: int = 0, queue: str = 'default') -> Result[None]:
        raise NotImplementedError

    @abstractmethod
    def size(self, queue: str = 'default') -> Result[int]:
        raise NotImplementedError

    @abstractmethod
    def fail(self, job_id: str, job: 'Job', exception: Exception,
             queue: str = 'default') -> Result[None]:
        raise NotImplementedError

    @abstractmethod
    def flush(self, queue: str = 'default') -> Result[None]:
        raise NotImplementedError

    def is_due(self, available_at: float | None) -> bool:
        return available_at is None or available_at <= time.time()
