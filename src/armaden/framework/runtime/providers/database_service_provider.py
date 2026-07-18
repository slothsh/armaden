from __future__ import annotations

import logging

from returns.result import Result, Success

from armaden.framework.classes.service_provider import ServiceProvider

logger = logging.getLogger(__name__)

SUPPORTED_DRIVERS = ('sqlite', 'pgsql', 'mysql', 'mssql')


class DatabaseServiceProvider(ServiceProvider):
    name = 'database'

    def __init__(self, container) -> None:
        super().__init__(container)
        self._registered = False

    def register(self) -> Result[None]:
        if self._build_connections():
            self._registered = True
        return Success(None)

    def boot(self) -> Result[None]:
        if not self._registered:
            if self._build_connections():
                self._registered = True
        return Success(None)

    def _build_connections(self) -> bool:
        application = self._container.make('app')
        config = application.config('database', {}) or {}

        if not config or not config.get('connections'):
            return False

        try:
            from masoniteorm.connections import ConnectionResolver
        except ImportError as exception:
            logger.error(
                "masonite-framework-orm is not installed; skipping database "
                "registration: %s", exception,
            )
            return False

        masonite_db = self._map_config(config)

        if masonite_db is None:
            return False

        resolver = ConnectionResolver(connection_details=masonite_db)

        self._container.instance('database.resolver', resolver)
        self._container.instance('database.connection_details', masonite_db)
        self._container.instance('database.default', masonite_db.get('default'))

        import os
        import armaden.framework.runtime.config.database as db_config_module
        db_config_module.DB = resolver
        os.environ['DB_CONFIG_PATH'] = 'armaden.framework.runtime.config.database'

        registered = [
            name for name in masonite_db
            if name != 'default' and isinstance(masonite_db[name], dict)
        ]
        logger.info(
            "Registered database connections: %s (default: %s)",
            ', '.join(registered) or 'none',
            masonite_db.get('default', 'none'),
        )

        return True

    def _map_config(self, config: dict) -> dict | None:
        default = config.get('default')
        connections = config.get('connections', {}) or {}

        if not connections:
            logger.warning("No database connections configured")
            return None

        masonite_db: dict = {'default': default}

        for name, conn in connections.items():
            conn = conn or {}
            driver = conn.get('driver')

            if driver not in SUPPORTED_DRIVERS:
                logger.error(
                    "Unsupported database driver '%s' for connection '%s'; "
                    "skipping this connection", driver, name,
                )
                continue

            masonite_conn: dict = {
                'driver': driver,
                'database': conn.get('database', ''),
            }

            if driver != 'sqlite':
                masonite_conn.update({
                    'host': conn.get('host', ''),
                    'port': conn.get('port', ''),
                    'user': conn.get('username', ''),
                    'password': conn.get('password', ''),
                    'prefix': conn.get('prefix', ''),
                })
            else:
                foreign_keys = conn.get('foreign_key_constraints')
                if foreign_keys is not None:
                    masonite_conn['foreign_keys'] = foreign_keys

            masonite_db[name] = masonite_conn

        if default and default not in masonite_db:
            logger.error(
                "Default database connection '%s' is not configured", default,
            )

        return masonite_db
