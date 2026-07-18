from __future__ import annotations

import logging
import uuid
from typing import TYPE_CHECKING

from returns.result import Failure, Result, Success

from armaden.framework.errors import Error
from armaden.framework.errors.generic import GenericError
from armaden.framework.queue.driver import QueueDriver

if TYPE_CHECKING:
    from armaden.framework.queue.job import Job

logger = logging.getLogger(__name__)


class SyncQueueDriver(QueueDriver):
    """Runs jobs immediately on the calling thread with no persistence."""

    def __init__(self, config: dict) -> None:
        self._config = config or {}

    def push(self, job: 'Job', queue: str = 'default') -> Result[str]:
        job_id = uuid.uuid4().hex
        try:
            job.before()
            job.handle()
            job.after()
        except Exception as exception:
            job.failed(exception)
            return Failure(Error(GenericError.EXCEPTION, details={'exception': exception}))
        return Success(job_id)

    def later(self, delay: int, job: 'Job', queue: str = 'default') -> Result[str]:
        logger.debug(
            "Sync driver ignoring delay=%ss for job %s",
            delay, type(job).__name__,
        )
        return self.push(job, queue)

    def pop(self, queue: str = 'default') -> Result['Job | None']:
        return Success(None)

    def delete(self, job_id: str, queue: str = 'default') -> Result[None]:
        return Success(None)

    def release(self, job_id: str, delay: int = 0, queue: str = 'default') -> Result[None]:
        return Success(None)

    def size(self, queue: str = 'default') -> Result[int]:
        return Success(0)

    def fail(self, job_id: str, job: 'Job', exception: Exception,
             queue: str = 'default') -> Result[None]:
        logger.warning(
            "Sync driver job %s (%s) failed: %s: %s",
            job_id, type(job).__name__, type(exception).__name__, exception,
        )
        return Success(None)

    def flush(self, queue: str = 'default') -> Result[None]:
        return Success(None)
