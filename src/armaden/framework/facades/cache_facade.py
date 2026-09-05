from collections.abc import Callable
from typing import cast, override

from armaden.framework.facades.facade import Facade
from armaden.framework.protocols.cache_protocol import CacheProtocol
from armaden.framework.types.result import Result


class CacheFacade(Facade):
    @override
    @classmethod
    def get_facade_accessor(cls) -> object:
        return 'cache.store.default'


    @classmethod
    def add(cls, key: str, value: object, ttl: int | None = None) -> Result[bool]:
        return cls._default_store().add(key, value, ttl)


    @classmethod
    async def add_async(cls, key: str, value: object, ttl: int | None = None) -> Result[bool]:
        return await cls._default_store().add_async(key, value, ttl)


    @classmethod
    def decrement(cls, key: str, value: int = 1) -> Result[int]:
        return cls._default_store().decrement(key, value)


    @classmethod
    async def decrement_async(cls, key: str, value: int = 1) -> Result[int]:
        return await cls._default_store().decrement_async(key, value)


    @classmethod
    def forever(cls, key: str, value: object) -> Result[bool]:
        return cls._default_store().forever(key, value)


    @classmethod
    async def forever_async(cls, key: str, value: object) -> Result[bool]:
        return await cls._default_store().forever_async(key, value)


    @classmethod
    def flush(cls) -> Result[bool]:
        return cls._default_store().flush()


    @classmethod
    async def flush_async(cls) -> Result[bool]:
        return await cls._default_store().flush_async()


    @classmethod
    def forget(cls, key: str) -> Result[bool]:
        return cls._default_store().forget(key)


    @classmethod
    async def forget_async(cls, key: str) -> Result[bool]:
        return await cls._default_store().forget_async(key)


    @classmethod
    def get(cls, key: str, default: object = None) -> Result[object]:
        return cls._default_store().get(key, default)


    @classmethod
    async def get_async(cls, key: str, default: object = None) -> Result[object]:
        return await cls._default_store().get_async(key, default)


    @classmethod
    def get_default_cache_time(cls) -> int:
        return cls._default_store().get_default_cache_time()


    @classmethod
    def get_prefix(cls) -> str:
        return cls._default_store().get_prefix()


    @classmethod
    def has(cls, key: str) -> Result[bool]:
        return cls._default_store().has(key)


    @classmethod
    async def has_async(cls, key: str) -> Result[bool]:
        return await cls._default_store().has_async(key)


    @classmethod
    def increment(cls, key: str, value: int = 1) -> Result[int]:
        return cls._default_store().increment(key, value)


    @classmethod
    async def increment_async(cls, key: str, value: int = 1) -> Result[int]:
        return await cls._default_store().increment_async(key, value)


    @classmethod
    def many(cls, keys: list[str]) -> Result[dict[str, object]]:
        return cls._default_store().many(keys)


    @classmethod
    async def many_async(cls, keys: list[str]) -> Result[dict[str, object]]:
        return await cls._default_store().many_async(keys)


    @classmethod
    def missing(cls, key: str) -> Result[bool]:
        return cls._default_store().missing(key)


    @classmethod
    async def missing_async(cls, key: str) -> Result[bool]:
        return await cls._default_store().missing_async(key)


    @classmethod
    def pull(cls, key: str, default: object = None) -> Result[object]:
        return cls._default_store().pull(key, default)


    @classmethod
    async def pull_async(cls, key: str, default: object = None) -> Result[object]:
        return await cls._default_store().pull_async(key, default)


    @classmethod
    def put(cls, key: str, value: object, ttl: int | None = None) -> Result[bool]:
        return cls._default_store().put(key, value, ttl)


    @classmethod
    async def put_async(cls, key: str, value: object, ttl: int | None = None) -> Result[bool]:
        return await cls._default_store().put_async(key, value, ttl)


    @classmethod
    def put_many(cls, items: dict[str, object], ttl: int | None = None) -> Result[bool]:
        return cls._default_store().put_many(items, ttl)


    @classmethod
    async def put_many_async(cls, items: dict[str, object], ttl: int | None = None) -> Result[bool]:
        return await cls._default_store().put_many_async(items, ttl)


    @classmethod
    def remember(cls, key: str, ttl: int, callback: Callable[[], object]) -> Result[object]:
        return cls._default_store().remember(key, ttl, callback)


    @classmethod
    async def remember_async(cls, key: str, ttl: int, callback: Callable[[], object]) -> Result[object]:
        return await cls._default_store().remember_async(key, ttl, callback)


    @classmethod
    def remember_forever(cls, key: str, callback: Callable[[], object]) -> Result[object]:
        return cls._default_store().remember_forever(key, callback)


    @classmethod
    async def remember_forever_async(cls, key: str, callback: Callable[[], object]) -> Result[object]:
        return await cls._default_store().remember_forever_async(key, callback)


    @classmethod
    def set_default_cache_time(cls, seconds: int) -> None:
        cls._default_store().set_default_cache_time(seconds)


    @classmethod
    def store(cls, name: str | None = None) -> CacheProtocol:
        if name is None:
            return cls._default_store()
        application = cls.get_facade_application()
        if application is None:
            return cls._default_store()
        return cast(CacheProtocol, application.make(f'cache.store.{name}'))


    @classmethod
    def _default_store(cls) -> CacheProtocol:
        return cast(CacheProtocol, cls.get_facade_root())
