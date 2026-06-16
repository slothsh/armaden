import asyncio
from collections.abc import Callable, Coroutine
from returns.result import Result
from typing import Protocol, List, Self, Any
from pathlib import Path
from .server import ServerInterface
from .error import ErrorInterface

# NOTE: Be sure to update these in utils.types
type AsyncStreamArg = asyncio.StreamReader | None
type AsyncStreamCallback = Callable[[str], Coroutine[Any, Any, Result[None, ErrorInterface]]]


class SupervisorInterface(Protocol):
    def with_server(self, server: ServerInterface) -> Self: ...

    async def initialize(self) -> Result[None, ErrorInterface]: ...
    async def run(self) -> Result[None, ErrorInterface]: ...
    async def shutdown(self) -> Result[None, ErrorInterface]: ...

    async def queue_start(self) -> None: ...
    async def queue_shutdown(self) -> None: ...
    async def queue_restart(self) -> None: ...
    async def queue_reload(self, config_path: str | Path) -> None: ...

    async def dispatch_subprocess(
        self,
        argv: List[str],
        cwd: Path | str | None = None,
        handle_std_stream: AsyncStreamCallback | None = None,
    ) -> Result[str, ErrorInterface]: ...
