from typing import cast, override

from armaden.framework.facades.facade import Facade
from armaden.framework.protocols.queue_driver_protocol import QueueDriverProtocol
from armaden.framework.protocols.queue_job_protocol import QueueJobProtocol
from armaden.framework.protocols.queue_resolver_protocol import QueueResolverProtocol
from armaden.framework.types.result import Result


class QueueFacade(Facade):
    @override
    @classmethod
    def get_facade_accessor(cls) -> object:
        return 'queue.connection.default'


    @classmethod
    def delete(cls, job_id: str, queue: str = 'default') -> Result[None]:
        return cls._default_driver().delete(job_id, queue)


    @classmethod
    def fail(
        cls,
        job_id: str,
        job: QueueJobProtocol,
        exception: Exception,
        queue: str = 'default',
    ) -> Result[None]:
        return cls._default_driver().fail(job_id, job, exception, queue)


    @classmethod
    def flush(cls, queue: str = 'default') -> Result[None]:
        return cls._default_driver().flush(queue)


    @classmethod
    def later(cls, delay: int, job: QueueJobProtocol, queue: str = 'default') -> Result[str]:
        return cls._default_driver().later(delay, job, queue)


    @classmethod
    def pop(cls, queue: str = 'default') -> Result[QueueJobProtocol | None]:
        return cls._default_driver().pop(queue)


    @classmethod
    def push(cls, job: QueueJobProtocol, queue: str = 'default') -> Result[str]:
        return cls._default_driver().push(job, queue)


    @classmethod
    def release(cls, job_id: str, delay: int = 0, queue: str = 'default') -> Result[None]:
        return cls._default_driver().release(job_id, delay, queue)


    @classmethod
    def size(cls, queue: str = 'default') -> Result[int]:
        return cls._default_driver().size(queue)


    @classmethod
    def connection(cls, name: str | None = None) -> QueueDriverProtocol:
        application = cls.get_facade_application()
        if application is None:
            return cls._default_driver()
        resolver = cast(
            QueueResolverProtocol,
            application.make(QueueResolverProtocol),
        )
        return resolver.connection(name)


    @classmethod
    def _default_driver(cls) -> QueueDriverProtocol:
        return cast(QueueDriverProtocol, cls.get_facade_root())
