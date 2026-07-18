from __future__ import annotations

from typing import TYPE_CHECKING

from returns.result import Result, Success

from ._registry import get_application

if TYPE_CHECKING:
    from armaden.framework.queue.driver import QueueDriver
    from armaden.framework.queue.job import Job


class Queue:

    @classmethod
    def _driver(cls, name: str | None = None) -> 'QueueDriver':
        container = get_application().container
        return container.get(f'queue.driver.{name or "default"}')

    @classmethod
    def connection(cls, name: str | None = None) -> 'QueueDriver':
        return cls._driver(name)

    @classmethod
    def push(cls, job: 'Job', queue: str = 'default',
             connection: str | None = None) -> Result[str]:
        return cls._driver(connection).push(job, queue)

    @classmethod
    def later(cls, delay: int, job: 'Job', queue: str = 'default',
              connection: str | None = None) -> Result[str]:
        return cls._driver(connection).later(delay, job, queue)

    @classmethod
    def bulk(cls, jobs: list['Job'], queue: str = 'default',
             connection: str | None = None) -> Result[list[str]]:
        driver = cls._driver(connection)
        job_ids: list[str] = []
        for job in jobs:
            result = driver.push(job, queue)
            from returns.pipeline import is_successful
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
