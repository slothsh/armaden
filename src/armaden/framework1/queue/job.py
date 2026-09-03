from __future__ import annotations

import logging
import uuid
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Self

from returns.pipeline import is_successful
from returns.result import Failure, Result, Success

from armaden.framework.classes.instance_container import MultiImplementation
from armaden.framework.errors import Error
from armaden.framework.errors.generic import GenericError

if TYPE_CHECKING:
    pass

logger = logging.getLogger(__name__)


class ShouldQueue(ABC):
    """Marker interface. Jobs that implement this are dispatched asynchronously
    to the queue. Jobs that do NOT implement this run synchronously on the
    calling thread."""
    pass


class PendingChain:
    """Stub for chained job dispatch. Full chaining support is deferred to a
    later epic."""

    def __init__(self, jobs: list['Job']) -> None:
        self._jobs = list(jobs)

    def dispatch(self) -> Result[str | None]:
        logger.debug("PendingChain.dispatch() called with %d jobs", len(self._jobs))
        return Success(None)


class Job(ABC, MultiImplementation):
    """Base class for all queue jobs. Users subclass this and implement handle()."""

    __queue__: str = 'default'
    __connection__: str | None = None
    __delay__: int | None = None
    __tries__: int | None = None
    __timeout__: int | None = None
    __backoff__: int | None = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        pass

    @abstractmethod
    def handle(self) -> None:
        raise NotImplementedError

    def before(self) -> None:
        logger.debug("Job before() hook: %s", type(self).__name__)

    def after(self) -> None:
        logger.debug("Job after() hook: %s", type(self).__name__)

    def failed(self, exception: Exception) -> None:
        logger.warning(
            "Job %s failed: %s: %s",
            type(self).__name__,
            type(exception).__name__,
            exception,
        )

    @classmethod
    def dispatch(cls, *args: Any, **kwargs: Any) -> Result[str | None]:
        instance = cls(*args, **kwargs)
        if isinstance(instance, ShouldQueue):
            from armaden.framework.facades import Queue
            delay = instance.__delay__
            if delay is not None and delay > 0:
                result = Queue.later(delay, instance, queue=instance.__queue__,
                                     connection=instance.__connection__)
            else:
                result = Queue.push(instance, queue=instance.__queue__,
                                    connection=instance.__connection__)
            if not is_successful(result):
                return result
            return Success(result.unwrap())
        try:
            instance.before()
            instance.handle()
            instance.after()
        except Exception as exception:
            instance.failed(exception)
            return Failure(Error(GenericError.EXCEPTION, details={'exception': exception}))
        return Success(None)

    @classmethod
    def dispatch_sync(cls, *args: Any, **kwargs: Any) -> Result[None]:
        instance = cls(*args, **kwargs)
        try:
            instance.before()
            instance.handle()
            instance.after()
        except Exception as exception:
            instance.failed(exception)
            return Failure(Error(GenericError.EXCEPTION, details={'exception': exception}))
        return Success(None)

    @classmethod
    def dispatch_if(cls, condition: bool, *args: Any, **kwargs: Any) -> Result[str | None]:
        if not condition:
            return Success(None)
        return cls.dispatch(*args, **kwargs)

    @classmethod
    def dispatch_unless(cls, condition: bool, *args: Any, **kwargs: Any) -> Result[str | None]:
        if condition:
            return Success(None)
        return cls.dispatch(*args, **kwargs)

    @classmethod
    def with_chain(cls, jobs: list['Job']) -> PendingChain:
        return PendingChain(jobs)

    def delay(self, seconds: int) -> Self:
        self.__delay__ = seconds
        return self

    def on_queue(self, queue: str) -> Self:
        self.__queue__ = queue
        return self

    def on_connection(self, connection: str) -> Self:
        self.__connection__ = connection
        return self

    def __getstate__(self) -> dict:
        return dict(self.__dict__)

    def __setstate__(self, state: dict) -> None:
        self.__dict__.update(state)

    def _job_id(self) -> str:
        return uuid.uuid4().hex
