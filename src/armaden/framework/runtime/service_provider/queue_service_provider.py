from __future__ import annotations

import logging
from collections.abc import Mapping
from typing import cast, override

from returns.result import Success

from armaden.framework.protocols.cache_protocol import CacheProtocol
from armaden.framework.protocols.container_protocol import ContainerProtocol
from armaden.framework.protocols.core_application_protocol import CoreApplicationProtocol
from armaden.framework.protocols.queue_driver_protocol import QueueDriverProtocol
from armaden.framework.runtime.queue.dto.queue_driver_dependencies_data import (
    QueueDriverDependenciesData,
)
from armaden.framework.runtime.queue.queue_driver_factory import create_queue_driver
from armaden.framework.runtime.service_provider.service_provider import ServiceProvider
from armaden.framework.runtime.supervisor.task.dto.task_graph_data import TaskGraphData
from armaden.framework.types.queue import QueueConfiguration
from armaden.framework.types.result import Result

logger = logging.getLogger(__name__)


class QueueServiceProvider(ServiceProvider):
    name: str = 'queue'

    def __init__(self, container: ContainerProtocol) -> None:
        super().__init__(container)
        self._registered: bool = False


    @override
    def boot(self) -> Result[None]:
        if not self._registered:
            self._build_drivers()
            self._registered = True
        return Success(None)


    @override
    def register(self) -> Result[None]:
        return Success(None)


    def _build_drivers(self) -> None:
        application = cast(
            CoreApplicationProtocol[TaskGraphData],
            self._container.make('app'),
        )
        raw_configuration = application.config('queue', {})
        configuration: QueueConfiguration = (
            cast(QueueConfiguration, raw_configuration)
            if isinstance(raw_configuration, Mapping)
            else {}
        )
        raw_connections = configuration.get('connections', {})
        connections: Mapping[str, object] = (
            cast(Mapping[str, object], raw_connections)
            if isinstance(raw_connections, Mapping)
            else {}
        )
        drivers: dict[str, QueueDriverProtocol] = {}
        for name, raw_connection in connections.items():
            if not isinstance(raw_connection, Mapping):
                continue
            connection = cast(QueueConfiguration, raw_connection)
            cache_name = connection.get('store', 'file')
            cache: CacheProtocol | None = None
            if isinstance(cache_name, str):
                cache_key = f'cache.store.{cache_name}'
                if self._container.has(cache_key):
                    cache = cast(CacheProtocol, self._container.make(cache_key))
            try:
                driver = create_queue_driver(
                    connection,
                    QueueDriverDependenciesData(cache=cache),
                )
            except Exception as exception:
                logger.warning("Failed to create queue connection '%s': %s", name, exception)
                continue
            drivers[name] = driver
            _ = self._container.instance(f'queue.connection.{name}', driver)

        default_name = configuration.get('default')
        configured_default = default_name if isinstance(default_name, str) else 'sync'
        default_driver = drivers.get(configured_default)
        default_driver_name = configured_default
        if default_driver is None and drivers:
            default_driver_name, default_driver = next(iter(drivers.items()))
        if default_driver is not None:
            _ = self._container.instance('queue.connection.default', default_driver)
            _ = self._container.instance('queue.default', default_driver_name)
            _ = self._container.instance(QueueDriverProtocol, default_driver)
        _ = self._container.instance('queue.connections', drivers)
