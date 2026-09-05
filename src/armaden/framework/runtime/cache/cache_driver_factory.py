from armaden.framework.protocols.cache_protocol import CacheProtocol
from armaden.framework.runtime.cache.dto.cache_driver_dependencies_data import (
    CacheDriverDependenciesData,
)
from armaden.framework.runtime.cache.exceptions.cache_driver_factory_error import (
    CacheDriverFactoryError,
)
from armaden.framework.runtime.cache.file_cache_driver import FileCacheDriver
from armaden.framework.types.cache import (
    CacheConfiguration,
    CacheDriverConstructor,
)


DRIVER_MAP: dict[str, CacheDriverConstructor] = {
    'file': FileCacheDriver,
}


def create_cache_driver(
    config: CacheConfiguration,
    application_config: CacheConfiguration,
    dependencies: CacheDriverDependenciesData,
) -> CacheProtocol:
    driver = config.get('driver')
    if not isinstance(driver, str) or not driver:
        raise ValueError(CacheDriverFactoryError.MISSING_DRIVER.value)
    constructor = DRIVER_MAP.get(driver)
    if constructor is None:
        supported = ', '.join(sorted(DRIVER_MAP))
        raise ValueError(f'{CacheDriverFactoryError.UNSUPPORTED_DRIVER.value}: {driver}. Supported drivers: {supported}')
    return constructor(
        config=config,
        application_config=application_config,
        dependencies=dependencies,
    )
