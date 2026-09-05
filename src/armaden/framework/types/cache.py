from collections.abc import Callable, Mapping

from armaden.framework.protocols.cache_protocol import CacheProtocol


type CacheConfiguration = Mapping[str, object]
type CacheDriverConstructor = Callable[..., CacheProtocol]
type CacheStoreResolver = Callable[[str], CacheProtocol]
