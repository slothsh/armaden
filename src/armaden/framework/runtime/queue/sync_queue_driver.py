from __future__ import annotations

import uuid
from typing import override

from returns.result import Failure, Success

from armaden.framework.protocols.container_aware_queue_job_protocol import (
    ContainerAwareQueueJobProtocol,
)
from armaden.framework.protocols.container_protocol import ContainerProtocol
from armaden.framework.protocols.queue_driver_protocol import QueueDriverProtocol
from armaden.framework.protocols.queue_job_protocol import QueueJobProtocol
from armaden.framework.runtime.error.error import Error
from armaden.framework.runtime.queue.dto.queue_driver_dependencies_data import (
    QueueDriverDependenciesData,
)
from armaden.framework.runtime.queue.exceptions.queue_driver_error import QueueDriverError
from armaden.framework.runtime.queue.job_invoker import invoke_job_handle_sync
from armaden.framework.types.queue import QueueConfiguration
from armaden.framework.types.result import Result


class SyncQueueDriver(QueueDriverProtocol):
    def __init__(
        self,
        config: QueueConfiguration,
        dependencies: QueueDriverDependenciesData | None = None,
    ) -> None:
        self._container: ContainerProtocol | None = (
            dependencies.container
            if dependencies is not None
            else None
        )
        self._config: QueueConfiguration = config


    @override
    def delete(self, job_id: str, queue: str = 'default') -> Result[None]:
        _ = job_id
        _ = queue
        return Success(None)


    @override
    def fail(
        self,
        job_id: str,
        job: QueueJobProtocol,
        exception: Exception,
        queue: str = 'default',
    ) -> Result[None]:
        _ = job_id
        _ = queue
        try:
            job.failed(exception)
        except Exception as hook_exception:
            return Failure(Error(QueueDriverError.OPERATION_FAILED, details={
                'exception': hook_exception,
            }))
        return Success(None)


    @override
    def flush(self, queue: str = 'default') -> Result[None]:
        _ = queue
        return Success(None)


    @override
    def later(self, delay: int, job: QueueJobProtocol, queue: str = 'default') -> Result[str]:
        _ = delay
        return self.push(job, queue)


    @override
    def pop(self, queue: str = 'default') -> Result[QueueJobProtocol | None]:
        _ = queue
        return Success(None)


    @override
    def push(self, job: QueueJobProtocol, queue: str = 'default') -> Result[str]:
        _ = queue
        job_id = uuid.uuid4().hex
        try:
            self._prepare_job(job)
            job.before()
            _ = invoke_job_handle_sync(job)
            job.after()
        except Exception as exception:
            try:
                job.failed(exception)
            except Exception as hook_exception:
                return Failure(Error(QueueDriverError.OPERATION_FAILED, details={
                    'exception': hook_exception,
                }))
            return Failure(Error(QueueDriverError.OPERATION_FAILED, details={
                'exception': exception,
            }))
        return Success(job_id)


    @override
    def release(self, job_id: str, delay: int = 0, queue: str = 'default') -> Result[None]:
        _ = job_id
        _ = delay
        _ = queue
        return Success(None)


    def _prepare_job(self, job: QueueJobProtocol) -> None:
        if self._container is None:
            return
        if isinstance(job, ContainerAwareQueueJobProtocol):
            job.bind_container(self._container)


    @override
    def size(self, queue: str = 'default') -> Result[int]:
        _ = queue
        return Success(0)
