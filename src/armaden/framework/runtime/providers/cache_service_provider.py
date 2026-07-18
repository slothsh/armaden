from __future__ import annotations

import logging

from returns.pipeline import is_successful
from returns.result import Failure, Result, Success

from armaden.framework.cache import create_cache_driver
from armaden.framework.classes.service_provider import ServiceProvider
from armaden.framework.protocols.cache import CacheProtocol

logger = logging.getLogger(__name__)


class CacheServiceProvider(ServiceProvider):
    name = 'cache'

    def register(self) -> Result[None]:
        application = self._container.make('app')
        config = application.config('cache', {}) or {}

        if not config:
            logger.warning("No cache configuration found; skipping cache registration")
            return Success(None)

        stores_config = config.get('stores', {}) or {}
        default_name = config.get('default')

        if not stores_config:
            logger.warning("No cache stores configured; skipping cache registration")
            return Success(None)

        if not self._container.has('filesystem.disk.default'):
            logger.warning(
                "Storage subsystem is not available; skipping cache registration "
                "(CacheServiceProvider must boot after FilesystemServiceProvider)"
            )
            return Success(None)

        driver_map: dict[str, CacheProtocol] = {}
        default_driver: CacheProtocol | None = None
        default_driver_name: str | None = default_name

        for store_name, store_config in stores_config.items():
            try:
                driver = create_cache_driver(store_config or {}, config)
            except Exception as exception:
                logger.warning(
                    "Failed to create cache store '%s': %s",
                    store_name, exception,
                )
                continue

            driver_map[store_name] = driver
            self._container.instance(f'cache.store.{store_name}', driver)

            if store_name == default_name:
                default_driver = driver

        if default_driver is None and driver_map:
            default_driver_name = next(iter(driver_map))
            default_driver = driver_map[default_driver_name]

        if default_driver is not None and default_driver_name is not None:
            self._container.instance('cache.store.default', default_driver)
            self._container.instance(CacheProtocol, default_driver)
            self._container.instance('cache.default', default_driver_name)
        else:
            logger.warning("No cache stores were registered")

        self._container.instance('cache.stores', driver_map)

        logger.info(
            "Registered cache stores: %s (default: %s)",
            ', '.join(driver_map) or 'none',
            default_driver_name if default_driver else 'none',
        )

        return Success(None)

    def boot(self) -> Result[None]:
        try:
            default_driver = self._container.get('cache.store.default')
        except Exception:
            return Success(None)

        if default_driver is None:
            return Success(None)

        cache_dir = getattr(default_driver, '_cache_dir', None)
        if cache_dir is None:
            return Success(None)

        disk = getattr(default_driver, '_disk', None)
        if disk is None:
            return Success(None)

        ensure = disk.make_directory(cache_dir)
        if not is_successful(ensure):
            failure = ensure.failure()
            details = getattr(failure, 'details', {}) or {}
            exception = details.get('exception')
            if not isinstance(exception, FileExistsError):
                logger.warning(
                    "Failed to create cache directory '%s': %s",
                    cache_dir, failure,
                )

        return Success(None)
