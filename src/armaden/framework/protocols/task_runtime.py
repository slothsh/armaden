import asyncio
from collections.abc import Callable, Coroutine
from pathlib import Path
from returns.result import Result as ReturnsResult
from typing import Any, Protocol

from armaden.framework.protocols.error import ErrorInterface

type Result[S] = ReturnsResult[S, ErrorInterface]
type AsyncStreamCallback = Callable[[str], Coroutine[Any, Any, Result[None]]]


class TaskRuntimeInterface(Protocol):
    @property
    def name(self) -> str | None: ...

    @property
    def graph_id(self) -> str: ...

    async def signal_ready(self) -> Result[None]: ...

    async def task_output(self, name: str) -> Result[Any]: ...

    async def dispatch_subprocess(
        self,
        argv: list[str],
        cwd: Path | str | None = None,
        handle_std_stream: AsyncStreamCallback | None = None,
    ) -> Result[str]: ...
