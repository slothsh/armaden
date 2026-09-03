from __future__ import annotations

from typing import TYPE_CHECKING

from .index import CacheIndex, FileCacheIndex
from .serializer import CacheSerializationError, CacheSerializer
from .storage_driver import CacheStorageDriver

if TYPE_CHECKING:
    from armaden.framework.protocols.cache import CacheProtocol


DRIVER_MAP = {
    'file': CacheStorageDriver,
}


def create_cache_driver(config: dict, app_config: dict) -> 'CacheProtocol':
    driver_name = config.get('driver')
    if not driver_name:
        raise ValueError("Cache store config is missing a 'driver' key")

    driver_class = DRIVER_MAP.get(driver_name)
    if driver_class is None:
        supported = ', '.join(sorted(DRIVER_MAP))
        raise ValueError(
            f"Unsupported cache driver '{driver_name}'. "
            f"Supported drivers: {supported}"
        )

    if driver_name == 'file':
        from armaden.framework.facades import Storage
        disk_name = config.get('disk', 'local')
        disk = Storage.disk(disk_name)

        serializer_config = app_config.get('serializer', {}) or {}
        serializer = CacheSerializer(serializer_config)

        import os
        cache_path = config.get('path', 'storage/framework/cache/data')
        index_path = config.get('index_path') or os.path.join(
            os.path.dirname(cache_path.rstrip('/')), 'index.json'
        )
        index = FileCacheIndex(disk, index_path)

        prefix = app_config.get('prefix', 'armaden_cache')
        hash_keys = app_config.get('hash_keys', True)
        default_ttl = app_config.get('ttl', 3600)

        return CacheStorageDriver(
            config=config,
            storage_disk=disk,
            serializer=serializer,
            index=index,
            prefix=prefix,
            hash_keys=hash_keys,
            default_ttl=default_ttl,
        )

    raise ValueError(f"Cache driver '{driver_name}' is not wired up in create_cache_driver")


__all__ = [
    'CacheStorageDriver',
    'CacheSerializer',
    'CacheSerializationError',
    'CacheIndex',
    'FileCacheIndex',
    'DRIVER_MAP',
    'create_cache_driver',
]
