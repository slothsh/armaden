from armaden.framework.protocols.queue_driver_protocol import QueueDriverProtocol
from armaden.framework.runtime.queue.cache_queue_driver import CacheQueueDriver
from armaden.framework.runtime.queue.dto.queue_driver_dependencies_data import (
    QueueDriverDependenciesData,
)
from armaden.framework.runtime.queue.exceptions.queue_factory_error import QueueFactoryError
from armaden.framework.runtime.queue.sync_queue_driver import SyncQueueDriver
from armaden.framework.types.queue import QueueConfiguration, QueueDriverConstructor


DRIVER_MAP: dict[str, QueueDriverConstructor] = {
    'cache': CacheQueueDriver,
    'sync': SyncQueueDriver,
}


def create_queue_driver(
    config: QueueConfiguration,
    dependencies: QueueDriverDependenciesData | None = None,
) -> QueueDriverProtocol:
    driver = config.get('driver')
    if not isinstance(driver, str) or not driver:
        raise ValueError(QueueFactoryError.MISSING_DRIVER.value)
    constructor = DRIVER_MAP.get(driver)
    if constructor is None:
        supported = ', '.join(sorted(DRIVER_MAP))
        raise ValueError(f'{QueueFactoryError.UNSUPPORTED_DRIVER.value}: {driver}. Supported drivers: {supported}')
    return constructor(
        config=config,
        dependencies=dependencies or QueueDriverDependenciesData(),
    )
