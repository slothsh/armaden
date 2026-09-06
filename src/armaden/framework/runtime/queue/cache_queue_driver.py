from __future__ import annotations

import threading
import time
import uuid
from collections.abc import Mapping
from typing import cast, override

from returns.pipeline import is_successful
from returns.result import Failure, Success

from armaden.framework.protocols.cache_protocol import CacheProtocol
from armaden.framework.protocols.queue_driver_protocol import QueueDriverProtocol
from armaden.framework.protocols.queue_job_protocol import QueueJobProtocol
from armaden.framework.runtime.error.error import Error
from armaden.framework.runtime.queue.dto.queue_driver_dependencies_data import (
    QueueDriverDependenciesData,
)
from armaden.framework.runtime.queue.exceptions.queue_driver_error import QueueDriverError
from armaden.framework.types.queue import QueueConfiguration
from armaden.framework.types.result import Result


class CacheQueueDriver(QueueDriverProtocol):
    def __init__(
        self,
        config: QueueConfiguration,
        dependencies: QueueDriverDependenciesData,
    ) -> None:
        cache = dependencies.cache
        if cache is None:
            raise ValueError('cache queue driver requires a cache store')
        self._cache: CacheProtocol = cache
        self._default_queue: str = self._string(config.get('queue'), 'default')
        retry_after = config.get('retry_after', 90)
        self._retry_after: int = retry_after if isinstance(retry_after, int) else 90
        self._locks: dict[str, threading.Lock] = {}
        self._locks_guard: threading.Lock = threading.Lock()


    @override
    def delete(self, job_id: str, queue: str = 'default') -> Result[None]:
        target = queue or self._default_queue
        _ = self._cache.forget(self._job_key(target, job_id))
        _ = self._cache.forget(self._reserved_key(target, job_id))
        return Success(None)


    @override
    def fail(self, job_id: str, job: QueueJobProtocol, exception: Exception, queue: str = 'default') -> Result[None]:
        target = queue or self._default_queue
        _ = self._cache.forever(self._failed_key(job_id), {
            'job': job,
            'exception': str(exception),
            'failed_at': time.time(),
            'queue': target,
        })
        _ = self.delete(job_id, target)
        try:
            job.failed(exception)
        except Exception as hook_exception:
            return self._failure(hook_exception)
        return Success(None)


    @override
    def flush(self, queue: str = 'default') -> Result[None]:
        target = queue or self._default_queue
        index = self._get_index(target)
        for job_id in index:
            _ = self.delete(job_id, target)
        _ = self._cache.forget(self._index_key(target))
        return Success(None)


    @override
    def later(self, delay: int, job: QueueJobProtocol, queue: str = 'default') -> Result[str]:
        return self._store(job, queue, max(0, delay))


    @override
    def pop(self, queue: str = 'default') -> Result[QueueJobProtocol | None]:
        target = queue or self._default_queue
        now = time.time()
        with self._lock_for(target):
            candidates: list[tuple[int, int, str, dict[str, object]]] = []
            for index, job_id in enumerate(self._get_index(target)):
                entry_result = self._cache.get(self._job_key(target, job_id))
                if not is_successful(entry_result):
                    continue
                entry = entry_result.unwrap()
                if not isinstance(entry, dict):
                    continue
                entry = cast(dict[str, object], entry)
                available_at = entry.get('available_at')
                if isinstance(available_at, (float, int)) and available_at > now:
                    continue
                reserved_result = self._cache.get(self._reserved_key(target, job_id))
                reserved = reserved_result.unwrap() if is_successful(reserved_result) else None
                if isinstance(reserved, Mapping):
                    reserved_at = reserved.get('reserved_at')
                    if isinstance(reserved_at, (float, int)) and now - reserved_at < self._retry_after:
                        continue
                priority = entry.get('priority', 0)
                candidates.append((priority if isinstance(priority, int) else 0, index, job_id, entry))

            if candidates:
                _, _, job_id, entry = max(candidates, key=lambda value: (value[0], -value[1]))
                job_object = entry.get('job')
                if job_object is None:
                    return self._failure(TypeError('cached queue entry has no job'))
                job = cast(QueueJobProtocol, job_object)
                attempts_object = entry.get('attempts', 0)
                attempts = attempts_object + 1 if isinstance(attempts_object, int) else 1
                entry['attempts'] = attempts
                object.__setattr__(job, '_queue_job_id', job_id)
                object.__setattr__(job, '_queue_attempts', attempts)
                _ = self._cache.forever(
                    self._reserved_key(target, job_id),
                    {'reserved_at': now},
                )
                return Success(job)
        return Success(None)


    @override
    def push(self, job: QueueJobProtocol, queue: str = 'default') -> Result[str]:
        return self._store(job, queue, 0)


    @override
    def release(self, job_id: str, delay: int = 0, queue: str = 'default') -> Result[None]:
        target = queue or self._default_queue
        result = self._cache.get(self._job_key(target, job_id))
        if not is_successful(result):
            return result.map(lambda _: None)
        entry = result.unwrap()
        if isinstance(entry, dict):
            entry['available_at'] = time.time() + max(0, delay)
            _ = self._cache.forever(
                self._job_key(target, job_id),
                cast(dict[str, object], entry),
            )
        _ = self._cache.forget(self._reserved_key(target, job_id))
        return Success(None)


    @override
    def size(self, queue: str = 'default') -> Result[int]:
        return Success(len(self._get_index(queue or self._default_queue)))


    def _failure(self, exception: Exception) -> Failure[Error]:
        return Failure(Error(QueueDriverError.OPERATION_FAILED, details={
            'exception': exception,
        }))


    def _get_index(self, queue: str) -> list[str]:
        result = self._cache.get(self._index_key(queue), [])
        if not is_successful(result):
            return []
        value = result.unwrap()
        items = cast(list[object], value)
        return [item for item in items if isinstance(item, str)] if isinstance(value, list) else []


    def _failed_key(self, job_id: str) -> str:
        return f'queue:failed:{job_id}'


    def _index_key(self, queue: str) -> str:
        return f'queue:{queue}:index'


    def _job_key(self, queue: str, job_id: str) -> str:
        return f'queue:{queue}:job:{job_id}'


    def _lock_for(self, queue: str) -> threading.Lock:
        with self._locks_guard:
            lock = self._locks.get(queue)
            if lock is None:
                lock = threading.Lock()
                self._locks[queue] = lock
            return lock


    def _reserved_key(self, queue: str, job_id: str) -> str:
        return f'queue:{queue}:reserved:{job_id}'


    def _store(self, job: QueueJobProtocol, queue: str, delay: int) -> Result[str]:
        target = queue or self._default_queue
        job_id = uuid.uuid4().hex
        with self._lock_for(target):
            result = self._cache.forever(self._job_key(target, job_id), {
                'job': job,
                'attempts': 0,
                'available_at': time.time() + delay,
                'priority': self._priority(job),
            })
            if not is_successful(result):
                return result.map(lambda _: job_id)
            index = self._get_index(target)
            index.append(job_id)
            index_result = self._cache.forever(self._index_key(target), index)
            if not is_successful(index_result):
                return index_result.map(lambda _: job_id)
        return Success(job_id)


    @staticmethod
    def _priority(job: QueueJobProtocol) -> int:
        value = getattr(job, 'priority', 0)
        return value if isinstance(value, int) else 0


    @staticmethod
    def _string(value: object, default: str) -> str:
        return value if isinstance(value, str) else default
