from __future__ import annotations

import asyncio
import hashlib
import logging
import threading
from typing import Any, Callable, TYPE_CHECKING

from returns.pipeline import is_successful
from returns.result import Failure, Result, Success

from armaden.framework.cache.index import CacheIndex, FileCacheIndex
from armaden.framework.cache.serializer import (
    CacheSerializationError,
    CacheSerializer,
)
from armaden.framework.errors import Error
from armaden.framework.errors.generic import GenericError
from armaden.framework.protocols.cache import CacheProtocol
from armaden.framework.protocols.error import ErrorInterface

if TYPE_CHECKING:
    from armaden.framework.protocols.filesystem import Filesystem

logger = logging.getLogger(__name__)


def _failure(operation: str, exception: Exception, **details: Any) -> Failure[ErrorInterface]:
    payload = {'operation': operation, 'exception': exception, **details}
    return Failure(Error(GenericError.EXCEPTION, details=payload))


def _failure_msg(operation: str, message: str, **details: Any) -> Failure[ErrorInterface]:
    payload = {'operation': operation, 'message': message, **details}
    return Failure(Error(GenericError.EXCEPTION, details=payload))


def _is_already_exists(failure: ErrorInterface) -> bool:
    details = getattr(failure, 'details', {}) or {}
    exception = details.get('exception')
    if isinstance(exception, FileExistsError):
        return True
    text = f'{failure!r}'
    return 'FileExistsError' in text or 'already exists' in text


def _is_not_found(failure: ErrorInterface) -> bool:
    details = getattr(failure, 'details', {}) or {}
    exception = details.get('exception')
    if isinstance(exception, FileNotFoundError):
        return True
    text = f'{failure!r}'
    return 'No such file' in text or 'FileNotFoundError' in text


class CacheStorageDriver(CacheProtocol):

    def __init__(
        self,
        config: dict,
        storage_disk: 'Filesystem',
        serializer: CacheSerializer | None = None,
        index: CacheIndex | None = None,
        *,
        prefix: str = 'armaden_cache',
        hash_keys: bool = True,
        default_ttl: int = 3600,
        serializer_config: dict | None = None,
    ) -> None:
        self._config = config
        self._disk = storage_disk
        self._cache_dir = config.get('path', 'storage/framework/cache/data')
        self._prefix = prefix
        self._hash_keys = hash_keys
        self._default_ttl = default_ttl
        self._serializer = serializer or CacheSerializer(serializer_config or {'default': 'json', 'auto_detect_type': True, 'version': 1})
        import os
        index_path = config.get('index_path') or os.path.join(
            os.path.dirname(self._cache_dir.rstrip('/')), 'index.json'
        )
        self._index = index or FileCacheIndex(storage_disk, index_path)
        self._locks: dict[str, threading.Lock] = {}
        self._locks_guard = threading.Lock()
        self._async_locks: dict[str, asyncio.Lock] = {}

    # -- Key & path resolution --------------------------------------------

    @staticmethod
    def _sanitize(name: str) -> str:
        return name.replace('/', '_').replace('\x00', '')

    def _key_path(self, key: str) -> str:
        composed = f'{self._prefix}{key}'
        if self._hash_keys:
            digest = hashlib.sha256(composed.encode('utf-8')).hexdigest()
            return f'{self._cache_dir}/{digest}'
        return f'{self._cache_dir}/{self._sanitize(composed)}'

    def _lock_for(self, key: str) -> threading.Lock:
        with self._locks_guard:
            lock = self._locks.get(key)
            if lock is None:
                lock = threading.Lock()
                self._locks[key] = lock
            return lock

    def _async_lock_for(self, key: str) -> asyncio.Lock:
        lock = self._async_locks.get(key)
        if lock is None:
            lock = asyncio.Lock()
            self._async_locks[key] = lock
        return lock

    def _ensure_cache_dir(self) -> Result[bool, ErrorInterface]:
        exists_result = self._disk.exists(self._cache_dir)
        if is_successful(exists_result) and exists_result.unwrap():
            return Success(True)
        result = self._disk.make_directory(self._cache_dir)
        if not is_successful(result):
            if _is_already_exists(result.failure()):
                return Success(True)
            return result
        return Success(True)

    # -- Internal read/write ---------------------------------------------

    def _read_entry(self, key: str) -> Result[Any, ErrorInterface]:
        path = self._key_path(key)
        if not self._index.has(key):
            return _failure_msg('get', 'cache key not found', key=key)
        read = self._disk.get(path)
        if not is_successful(read):
            return read
        try:
            value = self._serializer.deserialize(read.unwrap())
        except CacheSerializationError as exception:
            return _failure('get', exception, key=key, path=path)
        return Success(value)

    def _write_entry(self, key: str, value: Any, ttl: int | None, forever: bool = False) -> Result[bool, ErrorInterface]:
        path = self._key_path(key)
        try:
            payload = self._serializer.serialize(value)
        except CacheSerializationError as exception:
            return _failure('put', exception, key=key, path=path)

        ensure = self._ensure_cache_dir()
        if not is_successful(ensure):
            return ensure

        write = self._disk.put(path, payload)
        if not is_successful(write):
            return write

        if forever or ttl is None:
            self._index.set_expiry(key, None)
        else:
            import time
            self._index.set_expiry(key, time.time() + ttl)
        return Success(True)

    # -- Synchronous API --------------------------------------------------

    def has(self, key: str) -> Result[bool, ErrorInterface]:
        if not self._index.has(key):
            return Success(False)
        path = self._key_path(key)
        result = self._disk.exists(path)
        if not is_successful(result):
            return result
        return Success(result.unwrap())

    def missing(self, key: str) -> Result[bool, ErrorInterface]:
        result = self.has(key)
        if not is_successful(result):
            return result
        return Success(not result.unwrap())

    def get(self, key: str, default: Any = None) -> Result[Any, ErrorInterface]:
        if not self._index.has(key):
            return Success(default)
        result = self._read_entry(key)
        if not is_successful(result):
            return Success(default)
        return result

    def pull(self, key: str, default: Any = None) -> Result[Any, ErrorInterface]:
        result = self._read_entry(key)
        if not is_successful(result):
            return Success(default)
        value = result.unwrap()
        forget_result = self.forget(key)
        if not is_successful(forget_result):
            return forget_result
        return Success(value)

    def put(self, key: str, value: Any, ttl: int | None = None) -> Result[bool, ErrorInterface]:
        effective_ttl = ttl if ttl is not None else self._default_ttl
        return self._write_entry(key, value, effective_ttl, forever=False)

    def add(self, key: str, value: Any, ttl: int | None = None) -> Result[bool, ErrorInterface]:
        has_result = self.has(key)
        if not is_successful(has_result):
            return has_result
        if has_result.unwrap():
            return Success(False)
        return self.put(key, value, ttl)

    def forever(self, key: str, value: Any) -> Result[bool, ErrorInterface]:
        return self._write_entry(key, value, None, forever=True)

    def forget(self, key: str) -> Result[bool, ErrorInterface]:
        path = self._key_path(key)
        result = self._disk.delete(path)
        if not is_successful(result):
            if not _is_not_found(result.failure()):
                return result
        self._index.remove(key)
        return Success(True)

    def flush(self) -> Result[bool, ErrorInterface]:
        files_result = self._disk.files(self._cache_dir)
        if is_successful(files_result):
            for filename in files_result.unwrap():
                self._disk.delete(f'{self._cache_dir}/{filename}')
        else:
            dirs_result = self._disk.directories(self._cache_dir)
            if not is_successful(dirs_result):
                return files_result
        self._index.flush()
        return Success(True)

    def _modify_numeric(self, key: str, delta: int) -> Result[int, ErrorInterface]:
        with self._lock_for(key):
            current = 0
            if self._index.has(key):
                read = self._read_entry(key)
                if is_successful(read):
                    value = read.unwrap()
                    if not isinstance(value, (int, float)) or isinstance(value, bool):
                        return _failure_msg('increment', 'cached value is not numeric', key=key, value=value)
                    current = int(value)
                else:
                    current = 0
            new_value = current + delta
            write = self._write_entry(key, new_value, None, forever=True)
            if not is_successful(write):
                return write
            return Success(new_value)

    def increment(self, key: str, value: int = 1) -> Result[int, ErrorInterface]:
        return self._modify_numeric(key, value)

    def decrement(self, key: str, value: int = 1) -> Result[int, ErrorInterface]:
        return self._modify_numeric(key, -value)

    def remember(self, key: str, ttl: int, callback: Callable[[], Any]) -> Result[Any, ErrorInterface]:
        result = self._read_entry(key)
        if is_successful(result):
            return result
        try:
            computed = callback()
        except Exception as exception:
            return _failure('remember', exception, key=key)
        put_result = self.put(key, computed, ttl)
        if not is_successful(put_result):
            return put_result
        return Success(computed)

    def remember_forever(self, key: str, callback: Callable[[], Any]) -> Result[Any, ErrorInterface]:
        result = self._read_entry(key)
        if is_successful(result):
            return result
        try:
            computed = callback()
        except Exception as exception:
            return _failure('remember_forever', exception, key=key)
        forever_result = self.forever(key, computed)
        if not is_successful(forever_result):
            return forever_result
        return Success(computed)

    def many(self, keys: list[str]) -> Result[dict[str, Any], ErrorInterface]:
        results: dict[str, Any] = {}
        for key in keys:
            result = self.get(key)
            if not is_successful(result):
                return result
            results[key] = result.unwrap()
        return Success(results)

    def put_many(self, items: dict[str, Any], ttl: int | None = None) -> Result[bool, ErrorInterface]:
        for key, value in items.items():
            result = self.put(key, value, ttl)
            if not is_successful(result):
                return result
        return Success(True)

    def store(self, name: str | None = None) -> 'CacheProtocol':
        if name is None:
            return self
        from armaden.framework.facades._registry import get_application
        return get_application().container.get(f'cache.store.{name}')

    def get_prefix(self) -> str:
        return self._prefix

    def get_default_cache_time(self) -> int:
        return self._default_ttl

    def set_default_cache_time(self, seconds: int) -> None:
        self._default_ttl = seconds

    # -- Async API --------------------------------------------------------

    async def _read_entry_async(self, key: str) -> Result[Any, ErrorInterface]:
        path = self._key_path(key)
        if not self._index.has(key):
            return _failure_msg('get', 'cache key not found', key=key)
        read = await self._disk.get_async(path)
        if not is_successful(read):
            return read
        try:
            value = self._serializer.deserialize(read.unwrap())
        except CacheSerializationError as exception:
            return _failure('get', exception, key=key, path=path)
        return Success(value)

    async def _write_entry_async(
        self, key: str, value: Any, ttl: int | None, forever: bool = False
    ) -> Result[bool, ErrorInterface]:
        path = self._key_path(key)
        try:
            payload = self._serializer.serialize(value)
        except CacheSerializationError as exception:
            return _failure('put', exception, key=key, path=path)

        ensure = await self._disk.make_directory_async(self._cache_dir)
        if not is_successful(ensure):
            if not _is_already_exists(ensure.failure()):
                return ensure

        write = await self._disk.put_async(path, payload)
        if not is_successful(write):
            return write

        if forever or ttl is None:
            self._index.set_expiry(key, None)
        else:
            import time
            self._index.set_expiry(key, time.time() + ttl)
        return Success(True)

    async def has_async(self, key: str) -> Result[bool, ErrorInterface]:
        if not self._index.has(key):
            return Success(False)
        path = self._key_path(key)
        result = await self._disk.exists_async(path)
        if not is_successful(result):
            return result
        return Success(result.unwrap())

    async def missing_async(self, key: str) -> Result[bool, ErrorInterface]:
        result = await self.has_async(key)
        if not is_successful(result):
            return result
        return Success(not result.unwrap())

    async def get_async(self, key: str, default: Any = None) -> Result[Any, ErrorInterface]:
        if not self._index.has(key):
            return Success(default)
        result = await self._read_entry_async(key)
        if not is_successful(result):
            return Success(default)
        return result

    async def pull_async(self, key: str, default: Any = None) -> Result[Any, ErrorInterface]:
        result = await self._read_entry_async(key)
        if not is_successful(result):
            return Success(default)
        value = result.unwrap()
        forget_result = await self.forget_async(key)
        if not is_successful(forget_result):
            return forget_result
        return Success(value)

    async def put_async(self, key: str, value: Any, ttl: int | None = None) -> Result[bool, ErrorInterface]:
        effective_ttl = ttl if ttl is not None else self._default_ttl
        return await self._write_entry_async(key, value, effective_ttl, forever=False)

    async def add_async(self, key: str, value: Any, ttl: int | None = None) -> Result[bool, ErrorInterface]:
        has_result = await self.has_async(key)
        if not is_successful(has_result):
            return has_result
        if has_result.unwrap():
            return Success(False)
        return await self.put_async(key, value, ttl)

    async def forever_async(self, key: str, value: Any) -> Result[bool, ErrorInterface]:
        return await self._write_entry_async(key, value, None, forever=True)

    async def forget_async(self, key: str) -> Result[bool, ErrorInterface]:
        path = self._key_path(key)
        result = await self._disk.delete_async(path)
        if not is_successful(result):
            if not _is_not_found(result.failure()):
                return result
        self._index.remove(key)
        return Success(True)

    async def flush_async(self) -> Result[bool, ErrorInterface]:
        files_result = await self._disk.files_async(self._cache_dir)
        if is_successful(files_result):
            for filename in files_result.unwrap():
                await self._disk.delete_async(f'{self._cache_dir}/{filename}')
        else:
            dirs_result = await self._disk.directories_async(self._cache_dir)
            if not is_successful(dirs_result):
                return files_result
        self._index.flush()
        return Success(True)

    async def _modify_numeric_async(self, key: str, delta: int) -> Result[int, ErrorInterface]:
        async with self._async_lock_for(key):
            current = 0
            if self._index.has(key):
                read = await self._read_entry_async(key)
                if is_successful(read):
                    value = read.unwrap()
                    if not isinstance(value, (int, float)) or isinstance(value, bool):
                        return _failure_msg('increment', 'cached value is not numeric', key=key, value=value)
                    current = int(value)
                else:
                    current = 0
            new_value = current + delta
            write = await self._write_entry_async(key, new_value, None, forever=True)
            if not is_successful(write):
                return write
            return Success(new_value)

    async def increment_async(self, key: str, value: int = 1) -> Result[int, ErrorInterface]:
        return await self._modify_numeric_async(key, value)

    async def decrement_async(self, key: str, value: int = 1) -> Result[int, ErrorInterface]:
        return await self._modify_numeric_async(key, -value)

    async def remember_async(self, key: str, ttl: int, callback: Callable[[], Any]) -> Result[Any, ErrorInterface]:
        result = await self._read_entry_async(key)
        if is_successful(result):
            return result
        try:
            computed = callback()
        except Exception as exception:
            return _failure('remember', exception, key=key)
        put_result = await self.put_async(key, computed, ttl)
        if not is_successful(put_result):
            return put_result
        return Success(computed)

    async def remember_forever_async(self, key: str, callback: Callable[[], Any]) -> Result[Any, ErrorInterface]:
        result = await self._read_entry_async(key)
        if is_successful(result):
            return result
        try:
            computed = callback()
        except Exception as exception:
            return _failure('remember_forever', exception, key=key)
        forever_result = await self.forever_async(key, computed)
        if not is_successful(forever_result):
            return forever_result
        return Success(computed)

    async def many_async(self, keys: list[str]) -> Result[dict[str, Any], ErrorInterface]:
        results: dict[str, Any] = {}
        for key in keys:
            result = await self.get_async(key)
            if not is_successful(result):
                return result
            results[key] = result.unwrap()
        return Success(results)

    async def put_many_async(self, items: dict[str, Any], ttl: int | None = None) -> Result[bool, ErrorInterface]:
        for key, value in items.items():
            result = await self.put_async(key, value, ttl)
            if not is_successful(result):
                return result
        return Success(True)
