from collections.abc import Mapping
from typing import override

from armaden.framework.protocols.queue_driver_protocol import QueueDriverProtocol
from armaden.framework.protocols.queue_resolver_protocol import QueueResolverProtocol
from armaden.framework.runtime.queue.exceptions.queue_resolver_error import (
    QueueResolverError,
)


class QueueResolver(QueueResolverProtocol):
    def __init__(
        self,
        connections: Mapping[str, QueueDriverProtocol],
        default: str,
    ) -> None:
        self._connections: dict[str, QueueDriverProtocol] = dict(connections)
        self._default: str = default


    @override
    def connection(self, name: str | None = None) -> QueueDriverProtocol:
        connection_name = name or self._default
        driver = self._connections.get(connection_name)
        if driver is None:
            error = (
                QueueResolverError.DEFAULT_CONNECTION_NOT_FOUND
                if name is None
                else QueueResolverError.CONNECTION_NOT_FOUND
            )
            raise LookupError(f'{error.value}: {connection_name}')
        return driver
