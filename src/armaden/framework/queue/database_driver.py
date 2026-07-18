from __future__ import annotations

import logging
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


class DatabaseQueueDriver(QueueDriver):
    """Persists jobs to a database table via the ORM, supports delayed jobs,
    tracks attempts, and stores failed jobs in a separate table."""

    def __init__(self, config: dict) -> None:
        self._config = config or {}
        self._connection: str = self._config.get('connection', 'sqlite')
        self._table: str = self._config.get('table', 'jobs')
        self._failed_table: str = self._config.get('failed_table', 'failed_jobs')
        self._retry_after: int = self._config.get('retry_after', 90)
        self._default_queue: str = self._config.get('queue', 'default')
        self._serializer: Any = None
        self._tables_ready = False

    def _resolver(self):
        from armaden.framework.facades import DB
        return DB._resolver()

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

    def _ensure_tables(self) -> Result[None]:
        if self._tables_ready:
            return Success(None)
        from armaden.framework.facades import Schema

        has_jobs = Schema.has_table(self._table, connection=self._connection)
        if not is_successful(has_jobs):
            return has_jobs.map(lambda _: None)
        if not has_jobs.unwrap():
            result = Schema.create(self._table, self._define_jobs_table, connection=self._connection)
            if not is_successful(result):
                return result

        has_failed = Schema.has_table(self._failed_table, connection=self._connection)
        if not is_successful(has_failed):
            return has_failed.map(lambda _: None)
        if not has_failed.unwrap():
            result = Schema.create(self._failed_table, self._define_failed_table, connection=self._connection)
            if not is_successful(result):
                return result

        self._tables_ready = True
        return Success(None)

    def _define_jobs_table(self, t) -> None:
        t.string('id', length=36)
        t.primary('id')
        t.string('queue').index()
        t.text('payload')
        t.integer('attempts').default(0)
        t.integer('reserved_at').nullable()
        t.integer('available_at').default(0)
        t.integer('created_at')

    def _define_failed_table(self, t) -> None:
        t.increments('id')
        t.string('connection')
        t.string('queue').index()
        t.text('payload')
        t.text('exception')
        t.integer('failed_at')

    def _execute(self, query: str, bindings: tuple) -> Result[Any]:
        try:
            result = self._resolver().statement(query, bindings, connection=self._connection)
            return Success(result)
        except Exception as exception:
            logger.exception("Database queue query failed: %s", exception)
            return Failure(Error(GenericError.EXCEPTION, details={
                'exception': exception, 'query': query,
            }))

    def _serialize(self, job: 'Job') -> Result[str]:
        try:
            payload = self._get_serializer().serialize(job)
            return Success(payload)
        except Exception as exception:
            logger.exception("Failed to serialize job %s: %s", type(job).__name__, exception)
            return Failure(Error(GenericError.EXCEPTION, details={'exception': exception}))

    def _deserialize(self, payload: str) -> Result['Job']:
        try:
            job = self._get_serializer().deserialize(payload)
            return Success(job)
        except Exception as exception:
            logger.exception("Failed to deserialize queue payload: %s", exception)
            return Failure(Error(GenericError.EXCEPTION, details={'exception': exception}))

    def _insert(self, job: 'Job', queue: str, available_at: int) -> Result[str]:
        job_id = uuid.uuid4().hex
        payload_result = self._serialize(job)
        if not is_successful(payload_result):
            return payload_result.map(lambda _: job_id)
        payload = payload_result.unwrap()
        now = int(time.time())
        result = self._execute(
            f'INSERT INTO {self._table} (id, queue, payload, attempts, reserved_at, available_at, created_at) '
            f'VALUES (?, ?, ?, ?, ?, ?, ?)',
            (job_id, queue, payload, 0, None, available_at, now),
        )
        if not is_successful(result):
            return result.map(lambda _: job_id)
        return Success(job_id)

    def push(self, job: 'Job', queue: str = 'default') -> Result[str]:
        ensure = self._ensure_tables()
        if not is_successful(ensure):
            return ensure.map(lambda _: '')
        return self._insert(job, queue or self._default_queue, int(time.time()))

    def later(self, delay: int, job: 'Job', queue: str = 'default') -> Result[str]:
        ensure = self._ensure_tables()
        if not is_successful(ensure):
            return ensure.map(lambda _: '')
        return self._insert(job, queue or self._default_queue, int(time.time()) + max(0, delay))

    def pop(self, queue: str = 'default') -> Result['Job | None']:
        ensure = self._ensure_tables()
        if not is_successful(ensure):
            return ensure.map(lambda _: None)
        now = int(time.time())
        select_result = self._execute(
            f'SELECT id, payload, attempts, available_at FROM {self._table} '
            f'WHERE queue = ? AND reserved_at IS NULL AND available_at <= ? '
            f'ORDER BY available_at ASC, id ASC LIMIT 1',
            (queue or self._default_queue, now),
        )
        if not is_successful(select_result):
            return select_result.map(lambda _: None)
        rows = select_result.unwrap()
        if not rows:
            return Success(None)
        row = rows[0] if isinstance(rows, list) else rows
        job_id = row['id']
        attempts = row.get('attempts', 0) or 0
        reserve_result = self._execute(
            f'UPDATE {self._table} SET reserved_at = ?, attempts = ? WHERE id = ?',
            (now, attempts + 1, job_id),
        )
        if not is_successful(reserve_result):
            return reserve_result.map(lambda _: None)
        payload = row['payload']
        job_result = self._deserialize(payload)
        if not is_successful(job_result):
            return job_result
        job = job_result.unwrap()
        job._job_id = job_id
        job._queue = queue or self._default_queue
        job._attempts = attempts + 1
        return Success(job)

    def delete(self, job_id: str, queue: str = 'default') -> Result[None]:
        result = self._execute(
            f'DELETE FROM {self._table} WHERE id = ?', (job_id,),
        )
        return result.map(lambda _: None)

    def release(self, job_id: str, delay: int = 0, queue: str = 'default') -> Result[None]:
        available_at = int(time.time()) + max(0, delay)
        result = self._execute(
            f'UPDATE {self._table} SET reserved_at = NULL, available_at = ? WHERE id = ?',
            (available_at, job_id),
        )
        return result.map(lambda _: None)

    def size(self, queue: str = 'default') -> Result[int]:
        result = self._execute(
            f'SELECT COUNT(*) AS c FROM {self._table} WHERE queue = ?',
            (queue or self._default_queue,),
        )
        if not is_successful(result):
            return result.map(lambda _: 0)
        rows = result.unwrap()
        if isinstance(rows, list) and rows:
            count = rows[0].get('c', 0)
        elif isinstance(rows, dict):
            count = rows.get('c', 0)
        else:
            count = 0
        try:
            return Success(int(count))
        except (TypeError, ValueError):
            return Success(0)

    def fail(self, job_id: str, job: 'Job', exception: Exception,
             queue: str = 'default') -> Result[None]:
        ensure = self._ensure_tables()
        if not is_successful(ensure):
            return ensure
        payload_result = self._serialize(job)
        payload = payload_result.unwrap() if is_successful(payload_result) else ''
        exception_text = ''.join(traceback.format_exception(type(exception), exception, exception.__traceback__))
        now = int(time.time())
        insert_result = self._execute(
            f'INSERT INTO {self._failed_table} (connection, queue, payload, exception, failed_at) '
            f'VALUES (?, ?, ?, ?, ?)',
            (self._connection, queue or self._default_queue, payload, exception_text, now),
        )
        if not is_successful(insert_result):
            return insert_result.map(lambda _: None)
        self._execute(f'DELETE FROM {self._table} WHERE id = ?', (job_id,))
        try:
            job.failed(exception)
        except Exception:
            logger.exception("Job failed() hook raised an exception")
        return Success(None)

    def flush(self, queue: str = 'default') -> Result[None]:
        result = self._execute(
            f'DELETE FROM {self._table} WHERE queue = ?', (queue or self._default_queue,),
        )
        return result.map(lambda _: None)
