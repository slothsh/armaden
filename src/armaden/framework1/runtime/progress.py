import asyncio
import logging
from dataclasses import dataclass
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class ProgressUpdate:
    step: str
    description: str
    progress: float | None = None
    timestamp: float = 0.0


class ProgressChannel:
    def __init__(self) -> None:
        self._current: ProgressUpdate | None = None
        self._lock = asyncio.Lock()

    @property
    def current(self) -> ProgressUpdate | None:
        return self._current

    async def send(self, update: ProgressUpdate) -> None:
        async with self._lock:
            self._current = update

    def send_sync(self, update: ProgressUpdate) -> None:
        self._current = update
