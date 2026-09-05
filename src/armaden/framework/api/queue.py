from __future__ import annotations

import logging
import uuid
from abc import ABC, abstractmethod
from typing import ClassVar, Self, override

from returns.result import Failure, Success

from armaden.framework.facades.queue_facade import QueueFacade
from armaden.framework.protocols.queue_driver_protocol import QueueDriverProtocol
from armaden.framework.protocols.queue_job_protocol import QueueJobProtocol
from armaden.framework.protocols.queue_worker_protocol import QueueWorkerProtocol
from armaden.framework.protocols.task_runtime_protocol import TaskRuntimeProtocol
from armaden.framework.runtime.error.error import Error
from armaden.framework.runtime.queue.exceptions.queue_driver_error import QueueDriverError
from armaden.framework.runtime.queue.queue_worker import QueueWorker
from armaden.framework.types.result import Result

logger = logging.getLogger(__name__)


class ShouldQueueTag:
    pass


class QueueJob(QueueJobProtocol, ABC):
    queue: ClassVar[str] = 'default'
    connection: ClassVar[str | None] = None
    delay: ClassVar[int | None] = None

    def __init__(self, *args: object, **kwargs: object) -> None:
        _ = args
        _ = kwargs


    @classmethod
    def dispatch(cls, *args: object, **kwargs: object) -> Result[str | None]:
        instance = cls(*args, **kwargs)
        if isinstance(instance, ShouldQueueTag):
            delay = instance._delay_override()
            queue_name = instance._queue_override()
            if delay is not None and delay > 0:
                return QueueFacade.later(delay, instance, queue_name)
            return QueueFacade.push(instance, queue_name)
        return cls._dispatch_instance(instance)


    @classmethod
    def dispatch_if(
        cls,
        condition: bool,
        *args: object,
        **kwargs: object,
    ) -> Result[str | None]:
        if not condition:
            return Success(None)
        return cls.dispatch(*args, **kwargs)


    @classmethod
    def dispatch_sync(cls, *args: object, **kwargs: object) -> Result[None]:
        return cls._dispatch_instance(cls(*args, **kwargs)).map(lambda _: None)


    @classmethod
    def dispatch_unless(
        cls,
        condition: bool,
        *args: object,
        **kwargs: object,
    ) -> Result[str | None]:
        return Success(None) if condition else cls.dispatch(*args, **kwargs)


    @override
    def after(self) -> None:
        pass


    @override
    def before(self) -> None:
        pass


    @override
    @abstractmethod
    def handle(self) -> None:
        raise NotImplementedError


    @override
    def failed(self, exception: Exception) -> None:
        logger.warning(
            'Queue job %s failed: %s: %s',
            type(self).__name__,
            type(exception).__name__,
            exception,
        )


    def with_delay(self, seconds: int) -> Self:
        object.__setattr__(self, '_delay_value', seconds)
        return self


    def on_connection(self, connection: str) -> Self:
        object.__setattr__(self, '_connection_value', connection)
        return self


    def on_queue(self, queue_name: str) -> Self:
        object.__setattr__(self, '_queue_value', queue_name)
        return self


    def _delay_override(self) -> int | None:
        value = getattr(self, '_delay_value', None)
        return value if isinstance(value, int) else type(self).delay


    @classmethod
    def _dispatch_instance(cls, instance: QueueJob) -> Result[str | None]:
        try:
            instance.before()
            instance.handle()
            instance.after()
        except Exception as exception:
            instance.failed(exception)
            return Failure(Error(QueueDriverError.OPERATION_FAILED, details={
                'exception': exception,
            }))
        return Success(None)


    def _job_id(self) -> str:
        return uuid.uuid4().hex


    def _queue_override(self) -> str:
        value = getattr(self, '_queue_value', None)
        return value if isinstance(value, str) else type(self).queue


__all__ = [
    'QueueFacade',
    'QueueJob',
    'QueueDriverProtocol',
    'QueueWorker',
    'QueueWorkerProtocol',
    'ShouldQueueTag',
    'TaskRuntimeProtocol',
]
