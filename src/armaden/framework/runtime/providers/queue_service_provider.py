from __future__ import annotations

import inspect
import logging
from importlib import import_module
from typing import Any

from returns.pipeline import is_successful
from returns.result import Result, Success

from armaden.framework.classes.service_provider import ServiceProvider
from armaden.framework.protocols.supervisor import SupervisorInterface
from armaden.framework.queue import DRIVER_MAP
from armaden.framework.queue.driver import QueueDriver
from armaden.framework.queue.job import Job
from armaden.framework.queue.worker import QueueWorker
from armaden.framework.runtime.module_loader import ModuleLoader
from armaden.framework.runtime.task_builder import TaskBuilder

logger = logging.getLogger(__name__)


class QueueServiceProvider(ServiceProvider):
    name = 'queue'

    def __init__(self, container) -> None:
        super().__init__(container)
        self._registered = False
        self._workers: dict[str, QueueWorker] = {}

    def register(self) -> Result[None]:
        if self._build_drivers():
            self._registered = True
        return Success(None)

    def boot(self) -> Result[None]:
        if not self._registered:
            if self._build_drivers():
                self._registered = True
            else:
                application = self._container.make('app')
                config = application.config('queue', {}) or {}
                if not config or not config.get('connections'):
                    logger.warning("No queue connections configured; skipping queue registration")

        self._discover_jobs()
        self._spawn_workers()
        return Success(None)

    def _build_drivers(self) -> bool:
        application = self._container.make('app')
        config = application.config('queue', {}) or {}

        if not config or not config.get('connections'):
            return False

        connections = config.get('connections', {}) or {}
        default_name = config.get('default')

        driver_map: dict[str, QueueDriver] = {}
        default_driver: QueueDriver | None = None

        for name, conn_config in connections.items():
            conn_config = conn_config or {}
            driver_key = conn_config.get('driver')
            if not driver_key:
                logger.warning("Queue connection '%s' has no 'driver' key; skipping", name)
                continue

            driver_class_path = DRIVER_MAP.get(driver_key)
            if driver_class_path is None:
                logger.error(
                    "Unsupported queue driver '%s' for connection '%s'; skipping",
                    driver_key, name,
                )
                continue

            try:
                driver_class = self._resolve_driver_class(driver_class_path)
            except Exception as exception:
                logger.error(
                    "Failed to resolve queue driver class '%s' for connection '%s': %s",
                    driver_class_path, name, exception,
                )
                continue

            if driver_key == 'database' and not self._container.has('database.resolver'):
                logger.error(
                    "Database queue driver configured for '%s' but ORM is not available; "
                    "skipping (QueueServiceProvider must boot after DatabaseServiceProvider)",
                    name,
                )
                continue

            if driver_key == 'cache' and not self._container.has('cache.store.default'):
                logger.error(
                    "Cache queue driver configured for '%s' but Cache store is not available; "
                    "skipping (QueueServiceProvider must boot after CacheServiceProvider)",
                    name,
                )
                continue

            try:
                driver = driver_class(conn_config)
            except Exception as exception:
                logger.error(
                    "Failed to instantiate queue driver '%s' for connection '%s': %s",
                    driver_key, name, exception,
                )
                continue

            driver_map[name] = driver
            self._container.instance(f'queue.driver.{name}', driver)

            if name == default_name:
                default_driver = driver

        if default_driver is None and driver_map:
            default_name = next(iter(driver_map))
            default_driver = driver_map[default_name]

        if default_driver is not None and default_name is not None:
            self._container.instance('queue.driver.default', default_driver)
            self._container.instance(QueueDriver, default_driver)
            self._container.instance('queue.default', default_name)
        else:
            logger.warning("No queue drivers were registered")

        self._container.instance('queue.drivers', driver_map)

        logger.info(
            "Registered queue drivers: %s (default: %s)",
            ', '.join(driver_map) or 'none',
            default_name if default_driver else 'none',
        )

        return bool(driver_map)

    def _resolve_driver_class(self, class_path: str):
        module_path, class_name = class_path.rsplit('.', 1)
        module = import_module(module_path)
        return getattr(module, class_name)

    def _discover_jobs(self) -> None:
        application = self._container.make('app')
        config = application.config('queue', {}) or {}
        paths = (config.get('discovery', {}) or {}).get('paths', ['app/jobs']) or []

        discovered: list[type[Job]] = []

        for path in paths:
            result = ModuleLoader.try_discover_user_modules(path)
            if not is_successful(result):
                logger.debug("Queue job discovery failed for path '%s': %s", path, result.failure())
                continue

            for module in result.unwrap():
                for _, obj in inspect.getmembers(module, inspect.isclass):
                    if not issubclass(obj, Job):
                        continue
                    if obj is Job:
                        continue
                    if obj.__module__ != getattr(module, '__name__', obj.__module__):
                        continue
                    if obj in discovered:
                        continue
                    discovered.append(obj)

        if discovered:
            logger.info(
                "Discovered %d queue job(s): %s",
                len(discovered), ', '.join(c.__name__ for c in discovered),
            )
        else:
            logger.debug("No queue jobs discovered in paths: %s", paths)

        self._container.instance('queue.discovered_jobs', discovered)

    def _spawn_workers(self) -> None:
        application = self._container.make('app')
        config = application.config('queue', {}) or {}
        connections = config.get('connections', {}) or {}
        driver_map = self._container.get('queue.drivers') if self._container.has('queue.drivers') else {}

        if not driver_map:
            return

        try:
            supervisor = self._container.make(SupervisorInterface)
        except Exception:
            logger.warning("Supervisor not available; queue workers were not spawned")
            return

        for name, driver in driver_map.items():
            conn_config = connections.get(name, {}) or {}
            driver_key = conn_config.get('driver')
            if driver_key == 'sync':
                continue

            worker = QueueWorker(name, driver, config)
            self._workers[name] = worker
            self._container.instance(f'queue.worker.{name}', worker)

            task = (
                TaskBuilder()
                .name(f'queue_worker_{name}')
                .description(f'Queue worker for {name} connection')
                .on_run(worker.run)
                .on_shutdown(worker.shutdown)
                .shared_thread()
                .long_running()
                .ready_timeout(10.0)
                .build()
            )
            supervisor.submit([task])
            logger.info("Submitted queue worker task for connection '%s'", name)

    async def status(self) -> Result[dict[str, Any]]:
        drivers = {}
        if self._container.has('queue.drivers'):
            for name, driver in self._container.get('queue.drivers').items():
                drivers[name] = type(driver).__name__

        workers = {
            name: {'connection': name}
            for name in self._workers
        }

        return Success({
            'drivers': drivers,
            'workers': workers,
        })
