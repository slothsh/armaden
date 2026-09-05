from dataclasses import dataclass

from armaden.framework.protocols.filesystem_protocol import FilesystemProtocol
from armaden.framework.types.cache import CacheStoreResolver


@dataclass(slots=True)
class CacheDriverDependenciesData:
    filesystem: FilesystemProtocol | None = None
    store_resolver: CacheStoreResolver | None = None
