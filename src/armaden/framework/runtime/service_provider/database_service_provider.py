from __future__ import annotations

import logging
from collections.abc import Callable, Mapping
from importlib import import_module
from typing import ClassVar, cast, override

from returns.result import Success

from armaden.framework.protocols.container_protocol import ContainerProtocol
from armaden.framework.protocols.core_application_protocol import CoreApplicationProtocol
from armaden.framework.protocols.database_resolver_protocol import DatabaseResolverProtocol
from armaden.framework.runtime.database.exceptions.database_provider_error import (
    DatabaseProviderError,
)
from armaden.framework.runtime.database.model import Model
from armaden.framework.runtime.service_provider.service_provider import ServiceProvider
from armaden.framework.runtime.supervisor.task.dto.task_graph_data import TaskGraphData
from armaden.framework.types.database import DatabaseConfiguration
from armaden.framework.types.result import Result

logger = logging.getLogger(__name__)


class DatabaseServiceProvider(ServiceProvider):
    name: str = 'database'
    SUPPORTED_DRIVERS: ClassVar[tuple[str, ...]] = (
        'mssql',
        'mysql',
        'pgsql',
        'sqlite',
    )

    def __init__(self, container: ContainerProtocol) -> None:
        super().__init__(container)
        self._registered: bool = False


    @override
    def boot(self) -> Result[None]:
        if not self._registered:
            self._build_connections()
            self._registered = True
        return Success(None)


    @override
    def register(self) -> Result[None]:
        return Success(None)


    def _build_connections(self) -> None:
        application = cast(
            CoreApplicationProtocol[TaskGraphData],
            self._container.make('app'),
        )
        raw_configuration = application.config('database', {})
        configuration: DatabaseConfiguration = (
            cast(DatabaseConfiguration, raw_configuration)
            if isinstance(raw_configuration, Mapping)
            else {}
        )
        masonite_configuration = self._map_configuration(configuration)
        if masonite_configuration is None:
            return
        try:
            module = import_module('masoniteorm.connections')
            resolver_factory = cast(
                Callable[..., object],
                getattr(module, 'ConnectionResolver'),
            )
            resolver = cast(
                DatabaseResolverProtocol,
                resolver_factory(connection_details=masonite_configuration),
            )
        except Exception as exception:
            logger.error(
                '%s: %s',
                DatabaseProviderError.CONNECTION_RESOLVER_UNAVAILABLE.value,
                exception,
            )
            return

        default_name = masonite_configuration.get('default')
        Model.set_database_resolver(resolver)
        _ = self._container.instance('database.resolver', resolver)
        _ = self._container.instance(
            'database.connection_details',
            masonite_configuration,
        )
        _ = self._container.instance(
            'database.default',
            default_name if isinstance(default_name, str) else 'sqlite',
        )
        logger.info(
            'Registered database connections: %s (default: %s)',
            ', '.join(
                name
                for name, value in masonite_configuration.items()
                if name != 'default' and isinstance(value, Mapping)
            ),
            default_name if isinstance(default_name, str) else 'none',
        )


    def _map_configuration(
        self,
        configuration: DatabaseConfiguration,
    ) -> dict[str, object] | None:
        raw_connections = configuration.get('connections')
        if not isinstance(raw_connections, Mapping):
            logger.warning(DatabaseProviderError.INVALID_CONFIGURATION.value)
            return None
        connections = cast(Mapping[str, object], raw_connections)
        default_name = configuration.get('default')
        masonite_configuration: dict[str, object] = {
            'default': default_name,
        }
        for name, raw_connection in connections.items():
            if not isinstance(raw_connection, Mapping):
                continue
            connection = cast(Mapping[str, object], raw_connection)
            driver = connection.get('driver')
            if not isinstance(driver, str) or driver not in self.SUPPORTED_DRIVERS:
                logger.error(
                    '%s: %s for connection %s',
                    DatabaseProviderError.UNSUPPORTED_DRIVER.value,
                    driver,
                    name,
                )
                continue
            mapped: dict[str, object] = {
                'driver': driver,
                'database': connection.get('database', ''),
            }
            if driver == 'sqlite':
                mapped['foreign_keys'] = connection.get(
                    'foreign_key_constraints',
                )
            else:
                mapped.update({
                    'host': connection.get('host', ''),
                    'port': connection.get('port', ''),
                    'user': connection.get('username', ''),
                    'password': connection.get('password', ''),
                    'prefix': connection.get('prefix', ''),
                })
            masonite_configuration[name] = mapped
        if isinstance(default_name, str) and default_name not in masonite_configuration:
            logger.error(
                'Default database connection %s is not configured',
                default_name,
            )
        return masonite_configuration
