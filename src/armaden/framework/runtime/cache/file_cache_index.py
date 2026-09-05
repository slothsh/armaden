from __future__ import annotations

import json
import logging
import threading
import time
from collections.abc import Mapping
from typing import cast, override

from returns.pipeline import is_successful

from armaden.framework.protocols.cache_index_protocol import CacheIndexProtocol
from armaden.framework.protocols.filesystem_protocol import FilesystemProtocol

logger = logging.getLogger(__name__)


class FileCacheIndex(CacheIndexProtocol):
    def __init__(self, filesystem: FilesystemProtocol, index_path: str) -> None:
        self._filesystem: FilesystemProtocol = filesystem
        self._index_path: str = index_path
        self._lock: threading.Lock = threading.Lock()
        self._index: dict[str, float | None] = {}
        self._load()


    @override
    def all_keys(self) -> list[str]:
        with self._lock:
            return list(self._index.keys())


    @override
    def expired_keys(self) -> list[str]:
        now = time.time()
        with self._lock:
            return [
                key
                for key, expires_at in self._index.items()
                if expires_at is not None and now > expires_at
            ]


    @override
    def flush(self) -> None:
        with self._lock:
            self._index = {}
            self._persist()


    @override
    def get_expiry(self, key: str) -> float | None:
        with self._lock:
            expires_at = self._index.get(key)
            if expires_at is None or time.time() > expires_at:
                return None
            return expires_at


    @override
    def has(self, key: str) -> bool:
        with self._lock:
            if key not in self._index:
                return False
            expires_at = self._index[key]
            return expires_at is None or time.time() <= expires_at


    @override
    def remove(self, key: str) -> None:
        with self._lock:
            if key in self._index:
                del self._index[key]
                self._persist()


    @override
    def set_expiry(self, key: str, expires_at: float | None) -> None:
        with self._lock:
            self._index[key] = expires_at
            self._persist()


    def _load(self) -> None:
        result = self._filesystem.get(self._index_path)
        if not is_successful(result):
            return
        raw = result.unwrap()
        if not raw:
            return
        if isinstance(raw, bytes):
            try:
                raw = raw.decode('utf-8')
            except UnicodeDecodeError:
                return
        try:
            data = json.loads(raw)
        except (json.JSONDecodeError, TypeError):
            logger.warning('Cache index file %s is corrupted; starting fresh', self._index_path)
            return
        if not isinstance(data, Mapping):
            return
        entries = cast(Mapping[str, object], data)
        for key, value in entries.items():
            if value is None:
                self._index[key] = None
            elif isinstance(value, (float, int)):
                self._index[key] = float(value)


    def _persist(self) -> None:
        try:
            data = json.dumps(self._index)
        except (TypeError, ValueError) as exception:
            logger.warning('Failed to serialize cache index: %s', exception)
            return
        result = self._filesystem.put(self._index_path, data)
        if not is_successful(result):
            logger.warning('Failed to persist cache index %s', self._index_path)
