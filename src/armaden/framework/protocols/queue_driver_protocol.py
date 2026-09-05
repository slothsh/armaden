from typing import Protocol

from armaden.framework.protocols.queue_job_protocol import QueueJobProtocol
from armaden.framework.types.result import Result


class QueueDriverProtocol(Protocol):
    def delete(self, job_id: str, queue: str = 'default') -> Result[None]: ...

    def fail(
        self,
        job_id: str,
        job: QueueJobProtocol,
        exception: Exception,
        queue: str = 'default',
    ) -> Result[None]: ...

    def flush(self, queue: str = 'default') -> Result[None]: ...

    def later(self, delay: int, job: QueueJobProtocol, queue: str = 'default') -> Result[str]: ...

    def pop(self, queue: str = 'default') -> Result[QueueJobProtocol | None]: ...

    def push(self, job: QueueJobProtocol, queue: str = 'default') -> Result[str]: ...

    def release(self, job_id: str, delay: int = 0, queue: str = 'default') -> Result[None]: ...

    def size(self, queue: str = 'default') -> Result[int]: ...
