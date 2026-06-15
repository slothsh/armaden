import asyncio
from collections.abc import Callable, Coroutine
from typing import List, Protocol, Any
from pathlib import Path

from server.lib.types import Result

type AsyncStreamArg = asyncio.StreamReader | None
type AsyncStreamCallback = Callable[[str], Coroutine[Any, Any, Result[None]]]


class QueueableSupervisor(Protocol):
    async def queue_start(self) -> None: ...
    async def queue_shutdown(self) -> None: ...
    async def queue_restart(self) -> None: ...
    async def queue_reload(self, config_path: str | Path) -> None: ...
    async def dispatch_subprocess(self, argv: List[str], cwd: Path | str | None = None, handle_std_stream: AsyncStreamCallback | None = None) -> Result[str]: ...
