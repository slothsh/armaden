from typing import Protocol

from armaden.framework.protocols.queue_driver_protocol import QueueDriverProtocol


class QueueResolverProtocol(Protocol):
    def connection(self, name: str | None = None) -> QueueDriverProtocol: ...
