from __future__ import annotations

import logging
from collections.abc import Mapping
from typing import cast, override

from returns.result import Success

from armaden.framework.protocols.container_protocol import ContainerProtocol
from armaden.framework.protocols.core_application_protocol import CoreApplicationProtocol
from armaden.framework.protocols.cache_protocol import CacheProtocol
from armaden.framework.protocols.filesystem_protocol import FilesystemProtocol
from armaden.framework.runtime.cache.cache_driver_factory import create_cache_driver
from armaden.framework.runtime.cache.dto.cache_driver_dependencies_data import (
    CacheDriverDependenciesData,
)
from armaden.framework.runtime.service_provider.service_provider import ServiceProvider
from armaden.framework.runtime.supervisor.task.dto.task_graph_data import TaskGraphData
from armaden.framework.types.cache import CacheConfiguration
from armaden.framework.types.result import Result

logger = logging.getLogger(__name__)


class CacheServiceProvider(ServiceProvider):
    name: str = 'cache'

    def __init__(self, container: ContainerProtocol) -> None:
        super().__init__(container)
        self._registered: bool = False


    @override
    def boot(self) -> Result[None]:
        if not self._registered:
            self._build_stores()
            self._registered = True
        return Success(None)


    @override
    def register(self) -> Result[None]:
        return Success(None)


    def _build_stores(self) -> None:
        application = cast(
            CoreApplicationProtocol[TaskGraphData],
            self._container.make('app'),
        )
        raw_configuration = application.config('cache', {})
        configuration: CacheConfiguration = (
            cast(CacheConfiguration, raw_configuration)
            if isinstance(raw_configuration, Mapping)
            else {}
        )
        raw_stores = configuration.get('stores', {})
        stores_configuration: Mapping[str, object] = (
            cast(Mapping[str, object], raw_stores)
            if isinstance(raw_stores, Mapping)
            else {}
        )
        driver_map: dict[str, CacheProtocol] = {}

        def resolve_store(name: str) -> CacheProtocol:
            return driver_map[name]

        for store_name, raw_store in stores_configuration.items():
            if not isinstance(raw_store, Mapping):
                continue
            store_configuration = cast(CacheConfiguration, raw_store)
            disk_name = store_configuration.get('disk', 'local')
            filesystem: FilesystemProtocol | None = None
            if isinstance(disk_name, str):
                disk_key = f'filesystem.disk.{disk_name}'
                if self._container.has(disk_key):
                    filesystem = cast(FilesystemProtocol, self._container.make(disk_key))
            try:
                driver = create_cache_driver(
                    store_configuration,
                    configuration,
                    CacheDriverDependenciesData(
                        filesystem=filesystem,
                        store_resolver=resolve_store,
                    ),
                )
            except Exception as exception:
                logger.warning(
                    "Failed to create cache store '%s': %s",
                    store_name,
                    exception,
                )
                continue
            driver_map[store_name] = driver
            _ = self._container.instance(f'cache.store.{store_name}', driver)

        default_name = configuration.get('default')
        configured_default = default_name if isinstance(default_name, str) else 'file'
        default_driver = driver_map.get(configured_default)
        default_driver_name = configured_default
        if default_driver is None and driver_map:
            default_driver_name, default_driver = next(iter(driver_map.items()))

        if default_driver is not None:
            _ = self._container.instance('cache.store.default', default_driver)
            _ = self._container.instance('cache.default', default_driver_name)
            _ = self._container.instance(CacheProtocol, default_driver)
        else:
            logger.warning('No cache stores were registered')

        _ = self._container.instance('cache.stores', driver_map)
        logger.info(
            'Registered cache stores: %s (default: %s)',
            ', '.join(driver_map) or 'none',
            default_driver_name if default_driver is not None else 'none',
        )
