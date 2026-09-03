from __future__ import annotations

import logging
import threading
import time
import traceback
import uuid
from typing import TYPE_CHECKING, Any

from returns.pipeline import is_successful
from returns.result import Failure, Result, Success

from armaden.framework.errors import Error
from armaden.framework.errors.generic import GenericError
from armaden.framework.queue.driver import QueueDriver

if TYPE_CHECKING:
    from armaden.framework.queue.job import Job

logger = logging.getLogger(__name__)


class CacheQueueDriver(QueueDriver):
    """Persists jobs to a Cache store with a queue-specific index for ordering
    and delayed availability."""

    def __init__(self, config: dict) -> None:
        self._config = config or {}
        self._store_name: str = self._config.get('store', 'file')
        self._default_queue: str = self._config.get('queue', 'default')
        self._retry_after: int = self._config.get('retry_after', 90)
        self._serializer: Any = None
        self._locks: dict[str, threading.Lock] = {}
        self._locks_guard = threading.Lock()

    def _cache(self):
        from armaden.framework.facades import Cache
        return Cache.store(self._store_name)

    def _lock_for(self, queue: str) -> threading.Lock:
        with self._locks_guard:
            lock = self._locks.get(queue)
            if lock is None:
                lock = threading.Lock()
                self._locks[queue] = lock
            return lock

    def _get_serializer(self):
        if self._serializer is None:
            from armaden.framework.cache.serializer import CacheSerializer
            try:
                from armaden.framework.facades._registry import get_application
                serializer_config = get_application().config('cache.serializer', {}) or {}
            except Exception:
                serializer_config = {}
            self._serializer = CacheSerializer(serializer_config or {
                'default': 'json', 'auto_detect_type': True, 'version': 1,
            })
        return self._serializer

    def _job_key(self, queue: str, job_id: str) -> str:
        return f'queue:{queue}:job:{job_id}'

    def _index_key(self, queue: str) -> str:
        return f'queue:{queue}:index'

    def _reserved_key(self, queue: str, job_id: str) -> str:
        return f'queue:{queue}:reserved:{job_id}'

    def _failed_key(self, job_id: str) -> str:
        return f'queue:failed:{job_id}'

    def _serialize(self, job: 'Job') -> Result[str]:
        try:
            return Success(self._get_serializer().serialize(job))
        except Exception as exception:
            logger.exception("Failed to serialize job %s: %s", type(job).__name__, exception)
            return Failure(Error(GenericError.EXCEPTION, details={'exception': exception}))

    def _deserialize(self, payload: str) -> Result['Job']:
        try:
            return Success(self._get_serializer().deserialize(payload))
        except Exception as exception:
            logger.exception("Failed to deserialize cache queue payload: %s", exception)
            return Failure(Error(GenericError.EXCEPTION, details={'exception': exception}))

    def _get_index(self, queue: str) -> list[str]:
        result = self._cache().get(self._index_key(queue), [])
        if not is_successful(result):
            return []
        value = result.unwrap()
        if isinstance(value, list):
            return value
        return []

    def _set_index(self, queue: str, job_ids: list[str]) -> Result[None]:
        return self._cache().forever(self._index_key(queue), job_ids).map(lambda _: None)

    def _store_job(self, queue: str, job_id: str, entry: dict) -> Result[None]:
        return self._cache().forever(self._job_key(queue, job_id), entry).map(lambda _: None)

    def push(self, job: 'Job', queue: str = 'default') -> Result[str]:
        target_queue = queue or self._default_queue
        job_id = uuid.uuid4().hex
        payload_result = self._serialize(job)
        if not is_successful(payload_result):
            return payload_result.map(lambda _: job_id)
        now = time.time()
        entry = {
            'payload': payload_result.unwrap(),
            'attempts': 0,
            'available_at': now,
            'created_at': now,
        }
        with self._lock_for(target_queue):
            store_result = self._store_job(target_queue, job_id, entry)
            if not is_successful(store_result):
                return store_result.map(lambda _: job_id)
            job_ids = self._get_index(target_queue)
            job_ids.append(job_id)
            index_result = self._set_index(target_queue, job_ids)
            if not is_successful(index_result):
                return index_result.map(lambda _: job_id)
        return Success(job_id)

    def later(self, delay: int, job: 'Job', queue: str = 'default') -> Result[str]:
        target_queue = queue or self._default_queue
        job_id = uuid.uuid4().hex
        payload_result = self._serialize(job)
        if not is_successful(payload_result):
            return payload_result.map(lambda _: job_id)
        now = time.time()
        entry = {
            'payload': payload_result.unwrap(),
            'attempts': 0,
            'available_at': now + max(0, delay),
            'created_at': now,
        }
        with self._lock_for(target_queue):
            store_result = self._store_job(target_queue, job_id, entry)
            if not is_successful(store_result):
                return store_result.map(lambda _: job_id)
            job_ids = self._get_index(target_queue)
            job_ids.append(job_id)
            index_result = self._set_index(target_queue, job_ids)
            if not is_successful(index_result):
                return index_result.map(lambda _: job_id)
        return Success(job_id)

    def pop(self, queue: str = 'default') -> Result['Job | None']:
        target_queue = queue or self._default_queue
        cache = self._cache()
        with self._lock_for(target_queue):
            job_ids = self._get_index(target_queue)
            now = time.time()
            for job_id in list(job_ids):
                entry_result = cache.get(self._job_key(target_queue, job_id))
                if not is_successful(entry_result):
                    continue
                entry = entry_result.unwrap()
                if entry is None:
                    continue
                if not isinstance(entry, dict):
                    continue
                available_at = entry.get('available_at')
                if available_at is not None and available_at > now:
                    continue
                reserved_result = cache.get(self._reserved_key(target_queue, job_id))
                reserved = reserved_result.unwrap() if is_successful(reserved_result) else None
                if isinstance(reserved, dict):
                    reserved_at = reserved.get('reserved_at')
                    if reserved_at is not None and (now - reserved_at) < self._retry_after:
                        continue
                attempts = entry.get('attempts', 0) or 0
                entry['attempts'] = attempts + 1
                cache.forever(self._job_key(target_queue, job_id), entry)
                cache.forever(self._reserved_key(target_queue, job_id), {'reserved_at': now})
                job_result = self._deserialize(entry.get('payload', ''))
                if not is_successful(job_result):
                    return job_result
                job = job_result.unwrap()
                job._job_id = job_id
                job._queue = target_queue
                job._attempts = attempts + 1
                return Success(job)
        return Success(None)

    def delete(self, job_id: str, queue: str = 'default') -> Result[None]:
        target_queue = queue or self._default_queue
        cache = self._cache()
        with self._lock_for(target_queue):
            cache.forget(self._job_key(target_queue, job_id))
            cache.forget(self._reserved_key(target_queue, job_id))
            job_ids = self._get_index(target_queue)
            if job_id in job_ids:
                job_ids.remove(job_id)
                self._set_index(target_queue, job_ids)
        return Success(None)

    def release(self, job_id: str, delay: int = 0, queue: str = 'default') -> Result[None]:
        target_queue = queue or self._default_queue
        cache = self._cache()
        with self._lock_for(target_queue):
            entry_result = cache.get(self._job_key(target_queue, job_id))
            if not is_successful(entry_result):
                return entry_result.map(lambda _: None)
            entry = entry_result.unwrap()
            if isinstance(entry, dict):
                entry['available_at'] = time.time() + max(0, delay)
                cache.forever(self._job_key(target_queue, job_id), entry)
            cache.forget(self._reserved_key(target_queue, job_id))
        return Success(None)

    def size(self, queue: str = 'default') -> Result[int]:
        target_queue = queue or self._default_queue
        with self._lock_for(target_queue):
            job_ids = self._get_index(target_queue)
        return Success(len(job_ids))

    def fail(self, job_id: str, job: 'Job', exception: Exception,
             queue: str = 'default') -> Result[None]:
        target_queue = queue or self._default_queue
        payload_result = self._serialize(job)
        payload = payload_result.unwrap() if is_successful(payload_result) else ''
        exception_text = ''.join(traceback.format_exception(type(exception), exception, exception.__traceback__))
        failed_entry = {
            'payload': payload,
            'exception': exception_text,
            'failed_at': time.time(),
            'connection': 'cache',
            'queue': target_queue,
        }
        cache = self._cache()
        cache.forever(self._failed_key(job_id), failed_entry)
        self.delete(job_id, target_queue)
        try:
            job.failed(exception)
        except Exception:
            logger.exception("Job failed() hook raised an exception")
        return Success(None)

    def flush(self, queue: str = 'default') -> Result[None]:
        target_queue = queue or self._default_queue
        cache = self._cache()
        with self._lock_for(target_queue):
            job_ids = self._get_index(target_queue)
            for job_id in job_ids:
                cache.forget(self._job_key(target_queue, job_id))
                cache.forget(self._reserved_key(target_queue, job_id))
            self._set_index(target_queue, [])
        return Success(None)
