from __future__ import annotations

import json
import logging
import threading
import time
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from returns.pipeline import is_successful

if TYPE_CHECKING:
    from armaden.framework.protocols.filesystem import Filesystem

logger = logging.getLogger(__name__)


class CacheIndex(ABC):

    @abstractmethod
    def get_expiry(self, key: str) -> float | None: ...

    @abstractmethod
    def set_expiry(self, key: str, expires_at: float | None) -> None: ...

    @abstractmethod
    def remove(self, key: str) -> None: ...

    @abstractmethod
    def flush(self) -> None: ...

    @abstractmethod
    def expired_keys(self) -> list[str]: ...

    @abstractmethod
    def all_keys(self) -> list[str]: ...

    @abstractmethod
    def has(self, key: str) -> bool: ...


class FileCacheIndex(CacheIndex):

    def __init__(self, storage_disk: 'Filesystem', index_path: str) -> None:
        self._disk = storage_disk
        self._index_path = index_path
        self._lock = threading.Lock()
        self._index: dict[str, float | None] = {}
        self._load()

    def _load(self) -> None:
        result = self._disk.get(self._index_path)
        if not is_successful(result):
            self._index = {}
            return

        raw = result.unwrap()
        if not raw:
            self._index = {}
            return

        try:
            data = json.loads(raw)
        except (json.JSONDecodeError, TypeError) as exception:
            logger.warning(
                "Cache index file '%s' is corrupted (%s); starting fresh",
                self._index_path, exception,
            )
            self._index = {}
            return

        if not isinstance(data, dict):
            logger.warning(
                "Cache index file '%s' did not contain a JSON object; starting fresh",
                self._index_path,
            )
            self._index = {}
            return

        normalized: dict[str, float | None] = {}
        for key, value in data.items():
            if value is None:
                normalized[key] = None
            else:
                try:
                    normalized[key] = float(value)
                except (TypeError, ValueError):
                    logger.warning(
                        "Cache index entry '%s' has invalid expiry %r; dropping",
                        key, value,
                    )
        self._index = normalized

    def _persist(self) -> None:
        try:
            data = json.dumps(self._index)
        except (TypeError, ValueError) as exception:
            logger.warning("Failed to serialize cache index: %s", exception)
            return

        result = self._disk.put(self._index_path, data)
        if not is_successful(result):
            logger.warning(
                "Failed to persist cache index '%s': %s",
                self._index_path, result.failure(),
            )

    def get_expiry(self, key: str) -> float | None:
        with self._lock:
            if key not in self._index:
                return None
            expires_at = self._index[key]
            if expires_at is None:
                return None
            if time.time() > expires_at:
                return None
            return expires_at

    def set_expiry(self, key: str, expires_at: float | None) -> None:
        with self._lock:
            self._index[key] = expires_at
            self._persist()

    def remove(self, key: str) -> None:
        with self._lock:
            if key in self._index:
                del self._index[key]
                self._persist()

    def flush(self) -> None:
        with self._lock:
            self._index = {}
            self._persist()

    def expired_keys(self) -> list[str]:
        now = time.time()
        with self._lock:
            return [
                key for key, expires_at in self._index.items()
                if expires_at is not None and now > expires_at
            ]

    def all_keys(self) -> list[str]:
        with self._lock:
            return list(self._index.keys())

    def has(self, key: str) -> bool:
        with self._lock:
            if key not in self._index:
                return False
            expires_at = self._index[key]
            if expires_at is None:
                return True
            return time.time() <= expires_at
