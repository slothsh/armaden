from __future__ import annotations

import time
import traceback
import uuid
from collections.abc import Mapping
from typing import cast, override

from returns.pipeline import is_successful
from returns.result import Failure, Success

from armaden.framework.protocols.cache_serializer_protocol import CacheSerializerProtocol
from armaden.framework.protocols.database_resolver_protocol import DatabaseResolverProtocol
from armaden.framework.protocols.queue_driver_protocol import QueueDriverProtocol
from armaden.framework.protocols.queue_job_protocol import QueueJobProtocol
from armaden.framework.runtime.cache.cache_serializer import CacheSerializer
from armaden.framework.runtime.error.error import Error
from armaden.framework.runtime.queue.dto.queue_driver_dependencies_data import (
    QueueDriverDependenciesData,
)
from armaden.framework.runtime.queue.exceptions.queue_driver_error import QueueDriverError
from armaden.framework.types.queue import QueueConfiguration
from armaden.framework.types.result import Result


class DatabaseQueueDriver(QueueDriverProtocol):
    def __init__(
        self,
        config: QueueConfiguration,
        dependencies: QueueDriverDependenciesData,
    ) -> None:
        resolver = dependencies.database
        if resolver is None:
            raise ValueError('database queue driver requires a database resolver')
        self._resolver: DatabaseResolverProtocol = resolver
        self._connection: str = self._string(config.get('connection'), 'sqlite')
        self._default_queue: str = self._string(config.get('queue'), 'default')
        self._failed_table: str = self._string(config.get('failed_table'), 'failed_jobs')
        self._table: str = self._string(config.get('table'), 'jobs')
        self._serializer: CacheSerializerProtocol = CacheSerializer({})
        self._tables_ready: bool = False


    @override
    def delete(self, job_id: str, queue: str = 'default') -> Result[None]:
        _ = queue
        return self._execute(
            f'DELETE FROM {self._table} WHERE id = ?',
            (job_id,),
        ).map(lambda _: None)


    @override
    def fail(self, job_id: str, job: QueueJobProtocol, exception: Exception, queue: str = 'default') -> Result[None]:
        ensure = self._ensure_tables()
        if not is_successful(ensure):
            return ensure
        payload = self._serialize(job)
        if not is_successful(payload):
            return payload.map(lambda _: None)
        exception_text = ''.join(traceback.format_exception(type(exception), exception, exception.__traceback__))
        insert = self._execute(
            f'INSERT INTO {self._failed_table} (connection, queue, payload, exception, failed_at) VALUES (?, ?, ?, ?, ?)',
            (self._connection, queue or self._default_queue, payload.unwrap(), exception_text, int(time.time())),
        )
        if not is_successful(insert):
            return insert.map(lambda _: None)
        _ = self.delete(job_id, queue)
        try:
            job.failed(exception)
        except Exception:
            pass
        return Success(None)


    @override
    def flush(self, queue: str = 'default') -> Result[None]:
        return self._execute(
            f'DELETE FROM {self._table} WHERE queue = ?',
            (queue or self._default_queue,),
        ).map(lambda _: None)


    @override
    def later(self, delay: int, job: QueueJobProtocol, queue: str = 'default') -> Result[str]:
        return self._insert(job, queue, max(0, delay))


    @override
    def pop(self, queue: str = 'default') -> Result[QueueJobProtocol | None]:
        ensure = self._ensure_tables()
        if not is_successful(ensure):
            return ensure.map(lambda _: None)
        target = queue or self._default_queue
        now = int(time.time())
        selected = self._execute(
            f'SELECT id, payload, attempts FROM {self._table} WHERE queue = ? AND reserved_at IS NULL AND available_at <= ? ORDER BY priority DESC, available_at ASC, id ASC LIMIT 1',
            (target, now),
        )
        if not is_successful(selected):
            return selected.map(lambda _: None)
        rows_object = selected.unwrap()
        if not isinstance(rows_object, list) or not rows_object:
            return Success(None)
        rows = cast(list[object], rows_object)
        raw_row: object = rows[0]
        if not isinstance(raw_row, Mapping):
            return Failure(Error(QueueDriverError.OPERATION_FAILED, details={
                'exception': TypeError('database queue row is invalid'),
            }))
        row_data = cast(Mapping[str, object], raw_row)
        job_id = row_data.get('id')
        payload = row_data.get('payload')
        if not isinstance(job_id, str) or not isinstance(payload, str):
            return Failure(Error(QueueDriverError.OPERATION_FAILED, details={
                'exception': TypeError('database queue row is incomplete'),
            }))
        attempts_value = row_data.get('attempts', 0)
        attempts = attempts_value + 1 if isinstance(attempts_value, int) else 1
        reserved = self._execute(
            f'UPDATE {self._table} SET reserved_at = ?, attempts = ? WHERE id = ?',
            (now, attempts, job_id),
        )
        if not is_successful(reserved):
            return reserved.map(lambda _: None)
        job_result = self._deserialize(payload)
        if not is_successful(job_result):
            return job_result
        job = job_result.unwrap()
        object.__setattr__(job, '_queue_job_id', job_id)
        object.__setattr__(job, '_queue_attempts', attempts)
        return Success(job)


    @override
    def push(self, job: QueueJobProtocol, queue: str = 'default') -> Result[str]:
        return self._insert(job, queue, 0)


    @override
    def release(self, job_id: str, delay: int = 0, queue: str = 'default') -> Result[None]:
        _ = queue
        return self._execute(
            f'UPDATE {self._table} SET reserved_at = NULL, available_at = ? WHERE id = ?',
            (int(time.time()) + max(0, delay), job_id),
        ).map(lambda _: None)


    @override
    def size(self, queue: str = 'default') -> Result[int]:
        result = self._execute(
            f'SELECT COUNT(*) AS c FROM {self._table} WHERE queue = ?',
            (queue or self._default_queue,),
        )
        if not is_successful(result):
            return result.map(lambda _: 0)
        rows = result.unwrap()
        if isinstance(rows, list) and rows and isinstance(rows[0], Mapping):
            count = cast(Mapping[str, object], rows[0]).get('c', 0)
            return Success(count if isinstance(count, int) else 0)
        return Success(0)


    def _deserialize(self, payload: str) -> Result[QueueJobProtocol]:
        try:
            return Success(cast(QueueJobProtocol, self._serializer.deserialize(payload)))
        except Exception as exception:
            return self._failure(exception)


    def _ensure_tables(self) -> Result[None]:
        if self._tables_ready:
            return Success(None)
        statements = (
            f'CREATE TABLE IF NOT EXISTS {self._table} (id VARCHAR(36) PRIMARY KEY, queue VARCHAR(255), payload TEXT, priority INTEGER DEFAULT 0, attempts INTEGER DEFAULT 0, reserved_at INTEGER NULL, available_at INTEGER DEFAULT 0, created_at INTEGER)',
            f'CREATE TABLE IF NOT EXISTS {self._failed_table} (id INTEGER PRIMARY KEY, connection VARCHAR(255), queue VARCHAR(255), payload TEXT, exception TEXT, failed_at INTEGER)',
        )
        for statement in statements:
            result = self._execute(statement, ())
            if not is_successful(result):
                return result.map(lambda _: None)
        self._tables_ready = True
        return Success(None)


    def _execute(self, query: str, bindings: tuple[object, ...]) -> Result[object]:
        try:
            return Success(self._resolver.statement(query, bindings, self._connection))
        except Exception as exception:
            return self._failure(exception)


    def _failure(self, exception: Exception) -> Failure[Error]:
        return Failure(Error(QueueDriverError.OPERATION_FAILED, details={
            'exception': exception,
        }))


    def _insert(self, job: QueueJobProtocol, queue: str, delay: int) -> Result[str]:
        ensure = self._ensure_tables()
        if not is_successful(ensure):
            return ensure.map(lambda _: '')
        job_id = uuid.uuid4().hex
        payload = self._serialize(job)
        if not is_successful(payload):
            return payload.map(lambda _: job_id)
        result = self._execute(
            f'INSERT INTO {self._table} (id, queue, payload, priority, attempts, reserved_at, available_at, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
            (
                job_id,
                queue or self._default_queue,
                payload.unwrap(),
                self._priority(job),
                0,
                None,
                int(time.time()) + delay,
                int(time.time()),
            ),
        )
        return result.map(lambda _: job_id)


    def _serialize(self, job: QueueJobProtocol) -> Result[str]:
        try:
            return Success(self._serializer.serialize(job))
        except Exception as exception:
            return self._failure(exception)


    @staticmethod
    def _priority(job: QueueJobProtocol) -> int:
        value = getattr(job, 'priority', 0)
        return value if isinstance(value, int) else 0


    @staticmethod
    def _string(value: object, default: str) -> str:
        return value if isinstance(value, str) else default
