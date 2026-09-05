from typing import Protocol, runtime_checkable

from armaden.framework.protocols.container_protocol import ContainerProtocol
from armaden.framework.protocols.queue_job_protocol import QueueJobProtocol


@runtime_checkable
class ContainerAwareQueueJobProtocol(QueueJobProtocol, Protocol):
    def bind_container(self, container: ContainerProtocol) -> None: ...
