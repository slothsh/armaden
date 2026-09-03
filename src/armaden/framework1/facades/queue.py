from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from returns.pipeline import is_successful
from returns.result import Result, Success

from ._registry import get_application

if TYPE_CHECKING:
    from armaden.framework.queue.driver import QueueDriver
    from armaden.framework.queue.job import Job

logger = logging.getLogger(__name__)


class Queue:

    @classmethod
    def _driver(cls, name: str | None = None) -> 'QueueDriver':
        container = get_application().container
        return container.get(f'queue.driver.{name or "default"}')

    @classmethod
    def _resolve_connection(cls, job: 'Job', connection: str | None) -> str | None:
        if connection is not None and connection != 'sync':
            return connection

        from armaden.framework.queue.job import ShouldQueue
        if not isinstance(job, ShouldQueue):
            return connection

        container = get_application().container
        default_name = container.get('queue.default') if container.has('queue.default') else None
        effective = connection or default_name

        if effective is not None and effective != 'sync':
            return effective

        if container.has('queue.drivers'):
            drivers = container.get('queue.drivers')
            for name in drivers:
                if name != 'sync':
                    logger.info(
                        "ShouldQueue job %s routed to async connection '%s' "
                        "(sync driver overridden)",
                        type(job).__name__, name,
                    )
                    return name

        logger.warning(
            "No async queue driver available for ShouldQueue job %s; "
            "falling back to sync (job will run on the dispatching thread)",
            type(job).__name__,
        )
        return effective or 'sync'

    @classmethod
    def connection(cls, name: str | None = None) -> 'QueueDriver':
        return cls._driver(name)

    @classmethod
    def push(cls, job: 'Job', queue: str = 'default',
             connection: str | None = None) -> Result[str]:
        resolved = cls._resolve_connection(job, connection)
        delay = getattr(job, '__delay__', None)
        if delay is not None and delay > 0:
            return cls._driver(resolved).later(delay, job, queue)
        return cls._driver(resolved).push(job, queue)

    @classmethod
    def later(cls, delay: int, job: 'Job', queue: str = 'default',
              connection: str | None = None) -> Result[str]:
        resolved = cls._resolve_connection(job, connection)
        return cls._driver(resolved).later(delay, job, queue)

    @classmethod
    def bulk(cls, jobs: list['Job'], queue: str = 'default',
             connection: str | None = None) -> Result[list[str]]:
        job_ids: list[str] = []
        for job in jobs:
            resolved = cls._resolve_connection(job, connection)
            driver = cls._driver(resolved)
            delay = getattr(job, '__delay__', None)
            if delay is not None and delay > 0:
                result = driver.later(delay, job, queue)
            else:
                result = driver.push(job, queue)
            if not is_successful(result):
                return result.map(lambda _: job_ids)
            job_ids.append(result.unwrap())
        return Success(job_ids)

    @classmethod
    def size(cls, queue: str = 'default', connection: str | None = None) -> Result[int]:
        return cls._driver(connection).size(queue)

    @classmethod
    def pop(cls, queue: str = 'default', connection: str | None = None) -> Result['Job | None']:
        return cls._driver(connection).pop(queue)

    @classmethod
    def flush(cls, queue: str = 'default', connection: str | None = None) -> Result[None]:
        return cls._driver(connection).flush(queue)


def queue() -> 'QueueDriver':
    return Queue.connection()
