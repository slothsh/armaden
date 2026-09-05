from __future__ import annotations

import asyncio
import hashlib
import posixpath
import threading
import time
from collections.abc import Mapping
from typing import Callable, cast, override

from returns.pipeline import is_successful
from returns.result import Failure, Success

from armaden.framework.protocols.cache_protocol import CacheProtocol
from armaden.framework.protocols.cache_serializer_protocol import CacheSerializerProtocol
from armaden.framework.protocols.filesystem_protocol import FilesystemProtocol
from armaden.framework.runtime.cache.cache_serializer import CacheSerializer
from armaden.framework.runtime.cache.dto.cache_driver_dependencies_data import (
    CacheDriverDependenciesData,
)
from armaden.framework.runtime.cache.exceptions.cache_serializer_error import (
    CacheSerializerError,
)
from armaden.framework.runtime.cache.exceptions.file_cache_driver_error import (
    FileCacheDriverError,
)
from armaden.framework.runtime.cache.file_cache_index import FileCacheIndex
from armaden.framework.runtime.error.error import Error
from armaden.framework.protocols.error_protocol import ErrorProtocol
from armaden.framework.types.result import Result


class FileCacheDriver(CacheProtocol):
    def __init__(
        self,
        config: Mapping[str, object],
        application_config: Mapping[str, object],
        dependencies: CacheDriverDependenciesData,
    ) -> None:
        filesystem = dependencies.filesystem
        if filesystem is None:
            raise ValueError(FileCacheDriverError.MISSING_FILESYSTEM.value)
        store_resolver = dependencies.store_resolver
        if store_resolver is None:
            raise ValueError(FileCacheDriverError.MISSING_STORE_RESOLVER.value)
        self._filesystem: FilesystemProtocol = filesystem
        self._store_resolver: Callable[[str], CacheProtocol] = store_resolver
        cache_dir = config.get('path', 'storage/framework/cache/data')
        self._cache_dir: str = cache_dir if isinstance(cache_dir, str) else 'storage/framework/cache/data'
        prefix = application_config.get('prefix', 'armaden_cache')
        self._prefix: str = prefix if isinstance(prefix, str) else 'armaden_cache'
        hash_keys = application_config.get('hash_keys', True)
        self._hash_keys: bool = hash_keys if isinstance(hash_keys, bool) else True
        ttl = application_config.get('ttl', 3600)
        self._default_ttl: int = ttl if isinstance(ttl, int) else 3600
        serializer_configuration = application_config.get('serializer', {})
        serializer_config: Mapping[str, object] = (
            cast(Mapping[str, object], serializer_configuration)
            if isinstance(serializer_configuration, Mapping)
            else {}
        )
        self._serializer: CacheSerializerProtocol = CacheSerializer(serializer_config)
        index_path = config.get('index_path')
        resolved_index_path = (
            index_path
            if isinstance(index_path, str) and index_path
            else f'{posixpath.dirname(self._cache_dir.rstrip("/"))}/index.json'
        )
        self._index: FileCacheIndex = FileCacheIndex(
            self._filesystem,
            resolved_index_path,
        )
        self._locks: dict[str, threading.Lock] = {}
        self._locks_guard: threading.Lock = threading.Lock()


    @override
    def add(self, key: str, value: object, ttl: int | None = None) -> Result[bool]:
        has_result = self.has(key)
        if not is_successful(has_result):
            return has_result
        if has_result.unwrap():
            return Success(False)
        return self.put(key, value, ttl)


    @override
    async def add_async(self, key: str, value: object, ttl: int | None = None) -> Result[bool]:
        return await asyncio.to_thread(self.add, key, value, ttl)


    @override
    def decrement(self, key: str, value: int = 1) -> Result[int]:
        return self._modify_numeric(key, -value)


    @override
    async def decrement_async(self, key: str, value: int = 1) -> Result[int]:
        return await asyncio.to_thread(self.decrement, key, value)


    @override
    def forever(self, key: str, value: object) -> Result[bool]:
        return self._write_entry(key, value, None)


    @override
    async def forever_async(self, key: str, value: object) -> Result[bool]:
        return await asyncio.to_thread(self.forever, key, value)


    @override
    def flush(self) -> Result[bool]:
        files_result = self._filesystem.files(self._cache_dir)
        if not is_successful(files_result):
            return files_result.map(lambda _: False)
        for filename in files_result.unwrap():
            delete_result = self._filesystem.delete(filename)
            if not is_successful(delete_result):
                return delete_result
        self._index.flush()
        return Success(True)


    @override
    async def flush_async(self) -> Result[bool]:
        return await asyncio.to_thread(self.flush)


    @override
    def forget(self, key: str) -> Result[bool]:
        result = self._filesystem.delete(self._key_path(key))
        if not is_successful(result):
            failure = result.failure()
            details_object = getattr(failure, 'details', {})
            details: Mapping[str, object] = (
                cast(Mapping[str, object], details_object)
                if isinstance(details_object, Mapping)
                else {}
            )
            exception = details.get('exception')
            if not isinstance(exception, FileNotFoundError):
                return result
        self._index.remove(key)
        return Success(True)


    @override
    async def forget_async(self, key: str) -> Result[bool]:
        return await asyncio.to_thread(self.forget, key)


    @override
    def get(self, key: str, default: object = None) -> Result[object]:
        if not self._index.has(key):
            return Success(default)
        result = self._read_entry(key)
        if not is_successful(result):
            return Success(default)
        return result


    @override
    async def get_async(self, key: str, default: object = None) -> Result[object]:
        return await asyncio.to_thread(self.get, key, default)


    @override
    def get_default_cache_time(self) -> int:
        return self._default_ttl


    @override
    def get_prefix(self) -> str:
        return self._prefix


    @override
    def has(self, key: str) -> Result[bool]:
        if not self._index.has(key):
            return Success(False)
        result = self._filesystem.exists(self._key_path(key))
        if not is_successful(result):
            return result
        return Success(result.unwrap())


    @override
    async def has_async(self, key: str) -> Result[bool]:
        return await asyncio.to_thread(self.has, key)


    @override
    def increment(self, key: str, value: int = 1) -> Result[int]:
        return self._modify_numeric(key, value)


    @override
    async def increment_async(self, key: str, value: int = 1) -> Result[int]:
        return await asyncio.to_thread(self.increment, key, value)


    @override
    def many(self, keys: list[str]) -> Result[dict[str, object]]:
        results: dict[str, object] = {}
        for key in keys:
            result = self.get(key)
            if not is_successful(result):
                return result.map(lambda _: {})
            results[key] = result.unwrap()
        return Success(results)


    @override
    async def many_async(self, keys: list[str]) -> Result[dict[str, object]]:
        return await asyncio.to_thread(self.many, keys)


    @override
    def missing(self, key: str) -> Result[bool]:
        result = self.has(key)
        if not is_successful(result):
            return result
        return Success(not result.unwrap())


    @override
    async def missing_async(self, key: str) -> Result[bool]:
        return await asyncio.to_thread(self.missing, key)


    @override
    def pull(self, key: str, default: object = None) -> Result[object]:
        result = self._read_entry(key)
        if not is_successful(result):
            return Success(default)
        value = result.unwrap()
        forget_result = self.forget(key)
        if not is_successful(forget_result):
            return forget_result
        return Success(value)


    @override
    async def pull_async(self, key: str, default: object = None) -> Result[object]:
        return await asyncio.to_thread(self.pull, key, default)


    @override
    def put(self, key: str, value: object, ttl: int | None = None) -> Result[bool]:
        effective_ttl = ttl if ttl is not None else self._default_ttl
        return self._write_entry(key, value, effective_ttl)


    @override
    async def put_async(self, key: str, value: object, ttl: int | None = None) -> Result[bool]:
        return await asyncio.to_thread(self.put, key, value, ttl)


    @override
    def put_many(self, items: dict[str, object], ttl: int | None = None) -> Result[bool]:
        for key, value in items.items():
            result = self.put(key, value, ttl)
            if not is_successful(result):
                return result
        return Success(True)


    @override
    async def put_many_async(self, items: dict[str, object], ttl: int | None = None) -> Result[bool]:
        return await asyncio.to_thread(self.put_many, items, ttl)


    @override
    def remember(self, key: str, ttl: int, callback: Callable[[], object]) -> Result[object]:
        result = self._read_entry(key)
        if is_successful(result):
            return result
        try:
            value = callback()
        except Exception as exception:
            return self._failure('remember', exception, key=key)
        write_result = self.put(key, value, ttl)
        if not is_successful(write_result):
            return write_result
        return Success(value)


    @override
    async def remember_async(self, key: str, ttl: int, callback: Callable[[], object]) -> Result[object]:
        return await asyncio.to_thread(self.remember, key, ttl, callback)


    @override
    def remember_forever(self, key: str, callback: Callable[[], object]) -> Result[object]:
        result = self._read_entry(key)
        if is_successful(result):
            return result
        try:
            value = callback()
        except Exception as exception:
            return self._failure('remember_forever', exception, key=key)
        write_result = self.forever(key, value)
        if not is_successful(write_result):
            return write_result
        return Success(value)


    @override
    async def remember_forever_async(self, key: str, callback: Callable[[], object]) -> Result[object]:
        return await asyncio.to_thread(self.remember_forever, key, callback)


    @override
    def set_default_cache_time(self, seconds: int) -> None:
        self._default_ttl = seconds


    @override
    def store(self, name: str | None = None) -> CacheProtocol:
        if name is None:
            return self
        return self._store_resolver(name)


    def _ensure_cache_directory(self) -> Result[bool]:
        exists_result = self._filesystem.exists(self._cache_dir)
        if is_successful(exists_result) and exists_result.unwrap():
            return Success(True)
        return self._filesystem.make_directory(self._cache_dir)


    def _failure(
        self,
        operation: str,
        exception: Exception,
        **details: object,
    ) -> Failure[ErrorProtocol]:
        payload = {'operation': operation, 'exception': exception, **details}
        return Failure(Error(FileCacheDriverError.OPERATION_FAILED, details=payload))


    def _key_path(self, key: str) -> str:
        composed = f'{self._prefix}{key}'
        if self._hash_keys:
            digest = hashlib.sha256(composed.encode('utf-8')).hexdigest()
            return f'{self._cache_dir}/{digest}'
        sanitized = composed.replace('/', '_').replace('\x00', '')
        return f'{self._cache_dir}/{sanitized}'


    def _lock_for(self, key: str) -> threading.Lock:
        with self._locks_guard:
            lock = self._locks.get(key)
            if lock is None:
                lock = threading.Lock()
                self._locks[key] = lock
            return lock


    def _modify_numeric(self, key: str, delta: int) -> Result[int]:
        with self._lock_for(key):
            current = 0
            if self._index.has(key):
                read_result = self._read_entry(key)
                if is_successful(read_result):
                    value = read_result.unwrap()
                    if not isinstance(value, (int, float)) or isinstance(value, bool):
                        return self._failure(
                            'increment',
                            TypeError('cached value is not numeric'),
                            key=key,
                            value=value,
                        )
                    current = int(value)
            new_value = current + delta
            write_result = self._write_entry(key, new_value, None)
            if not is_successful(write_result):
                return write_result
            return Success(new_value)


    def _read_entry(self, key: str) -> Result[object]:
        if not self._index.has(key):
            return self._failure('get', KeyError(key), key=key)
        result = self._filesystem.get(self._key_path(key))
        if not is_successful(result):
            return result
        try:
            return Success(self._serializer.deserialize(result.unwrap()))
        except CacheSerializerError as exception:
            return self._failure('get', exception, key=key)


    def _write_entry(self, key: str, value: object, ttl: int | None) -> Result[bool]:
        try:
            payload = self._serializer.serialize(value)
        except CacheSerializerError as exception:
            return self._failure('put', exception, key=key)
        ensure_result = self._ensure_cache_directory()
        if not is_successful(ensure_result):
            return ensure_result
        write_result = self._filesystem.put(self._key_path(key), payload)
        if not is_successful(write_result):
            return write_result
        self._index.set_expiry(
            key,
            None if ttl is None else time.time() + ttl,
        )
        return Success(True)
