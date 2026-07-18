from __future__ import annotations

from typing import TYPE_CHECKING, Any, Callable

from ._registry import get_application

if TYPE_CHECKING:
    from armaden.framework.protocols.cache import CacheProtocol
    from armaden.framework.utils.types import Result


class Cache:

    @classmethod
    def store(cls, name: str | None = None) -> 'CacheProtocol':
        container = get_application().container
        if name is None:
            return container.get('cache.store.default')
        return container.get(f'cache.store.{name}')

    @classmethod
    def _default_store(cls) -> 'CacheProtocol':
        return cls.store(None)

    @classmethod
    def has(cls, key: str) -> 'Result[bool]':
        return cls._default_store().has(key)

    @classmethod
    def missing(cls, key: str) -> 'Result[bool]':
        return cls._default_store().missing(key)

    @classmethod
    def get(cls, key: str, default: Any = None) -> 'Result[Any]':
        return cls._default_store().get(key, default)

    @classmethod
    def pull(cls, key: str, default: Any = None) -> 'Result[Any]':
        return cls._default_store().pull(key, default)

    @classmethod
    def put(cls, key: str, value: Any, ttl: int | None = None) -> 'Result[bool]':
        return cls._default_store().put(key, value, ttl)

    @classmethod
    def add(cls, key: str, value: Any, ttl: int | None = None) -> 'Result[bool]':
        return cls._default_store().add(key, value, ttl)

    @classmethod
    def forever(cls, key: str, value: Any) -> 'Result[bool]':
        return cls._default_store().forever(key, value)

    @classmethod
    def forget(cls, key: str) -> 'Result[bool]':
        return cls._default_store().forget(key)

    @classmethod
    def flush(cls) -> 'Result[bool]':
        return cls._default_store().flush()

    @classmethod
    def increment(cls, key: str, value: int = 1) -> 'Result[int]':
        return cls._default_store().increment(key, value)

    @classmethod
    def decrement(cls, key: str, value: int = 1) -> 'Result[int]':
        return cls._default_store().decrement(key, value)

    @classmethod
    def remember(cls, key: str, ttl: int, callback: Callable[[], Any]) -> 'Result[Any]':
        return cls._default_store().remember(key, ttl, callback)

    @classmethod
    def remember_forever(cls, key: str, callback: Callable[[], Any]) -> 'Result[Any]':
        return cls._default_store().remember_forever(key, callback)

    @classmethod
    def many(cls, keys: list[str]) -> 'Result[dict[str, Any]]':
        return cls._default_store().many(keys)

    @classmethod
    def put_many(cls, items: dict[str, Any], ttl: int | None = None) -> 'Result[bool]':
        return cls._default_store().put_many(items, ttl)

    @classmethod
    def get_prefix(cls) -> str:
        return cls._default_store().get_prefix()

    @classmethod
    def get_default_cache_time(cls) -> int:
        return cls._default_store().get_default_cache_time()

    @classmethod
    def set_default_cache_time(cls, seconds: int) -> None:
        cls._default_store().set_default_cache_time(seconds)

    @classmethod
    async def has_async(cls, key: str) -> 'Result[bool]':
        return await cls._default_store().has_async(key)

    @classmethod
    async def missing_async(cls, key: str) -> 'Result[bool]':
        return await cls._default_store().missing_async(key)

    @classmethod
    async def get_async(cls, key: str, default: Any = None) -> 'Result[Any]':
        return await cls._default_store().get_async(key, default)

    @classmethod
    async def pull_async(cls, key: str, default: Any = None) -> 'Result[Any]':
        return await cls._default_store().pull_async(key, default)

    @classmethod
    async def put_async(cls, key: str, value: Any, ttl: int | None = None) -> 'Result[bool]':
        return await cls._default_store().put_async(key, value, ttl)

    @classmethod
    async def add_async(cls, key: str, value: Any, ttl: int | None = None) -> 'Result[bool]':
        return await cls._default_store().add_async(key, value, ttl)

    @classmethod
    async def forever_async(cls, key: str, value: Any) -> 'Result[bool]':
        return await cls._default_store().forever_async(key, value)

    @classmethod
    async def forget_async(cls, key: str) -> 'Result[bool]':
        return await cls._default_store().forget_async(key)

    @classmethod
    async def flush_async(cls) -> 'Result[bool]':
        return await cls._default_store().flush_async()

    @classmethod
    async def increment_async(cls, key: str, value: int = 1) -> 'Result[int]':
        return await cls._default_store().increment_async(key, value)

    @classmethod
    async def decrement_async(cls, key: str, value: int = 1) -> 'Result[int]':
        return await cls._default_store().decrement_async(key, value)

    @classmethod
    async def remember_async(cls, key: str, ttl: int, callback: Callable[[], Any]) -> 'Result[Any]':
        return await cls._default_store().remember_async(key, ttl, callback)

    @classmethod
    async def remember_forever_async(cls, key: str, callback: Callable[[], Any]) -> 'Result[Any]':
        return await cls._default_store().remember_forever_async(key, callback)

    @classmethod
    async def many_async(cls, keys: list[str]) -> 'Result[dict[str, Any]]':
        return await cls._default_store().many_async(keys)

    @classmethod
    async def put_many_async(cls, items: dict[str, Any], ttl: int | None = None) -> 'Result[bool]':
        return await cls._default_store().put_many_async(items, ttl)


def cache() -> 'CacheProtocol':
    return Cache.store()
