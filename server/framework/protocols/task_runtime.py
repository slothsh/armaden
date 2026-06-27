from collections.abc import Callable, Coroutine
from pathlib import Path
from returns.result import Result as ReturnsResult
from typing import Any, Protocol

from framework.protocols.error import ErrorInterface

type Result[S] = ReturnsResult[S, ErrorInterface]
type AsyncStreamCallback = Callable[[str], Coroutine[Any, Any, Result[None]]]


class TaskRuntimeInterface(Protocol):
    @property
    def name(self) -> str: ...

    async def dispatch_subprocess(
        self,
        argv: list[str],
        cwd: Path | str | None = None,
        handle_std_stream: AsyncStreamCallback | None = None,
    ) -> Result[str]: ...
