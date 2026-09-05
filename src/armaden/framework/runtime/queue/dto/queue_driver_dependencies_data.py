from dataclasses import dataclass

from armaden.framework.protocols.cache_protocol import CacheProtocol
from armaden.framework.protocols.container_protocol import ContainerProtocol
from armaden.framework.protocols.database_resolver_protocol import DatabaseResolverProtocol


@dataclass(slots=True)
class QueueDriverDependenciesData:
    cache: CacheProtocol | None = None
    container: ContainerProtocol | None = None
    database: DatabaseResolverProtocol | None = None
