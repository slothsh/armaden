from __future__ import annotations

from pathlib import Path
from typing import Protocol

from armaden.framework.types.coroutine import AsyncStreamCallback
from armaden.framework.types.result import Result


class TaskRuntimeProtocol(Protocol):
    async def dispatch_subprocess(
        self,
        argv: list[str],
        cwd: Path | str | None = None,
        handle_std_stream: AsyncStreamCallback | None = None,
    ) -> Result[str]: ...

    @property
    def graph_id(self) -> str: ...

    @property
    def name(self) -> str: ...

    async def signal_ready(self) -> Result[None]: ...

    async def task_output(self, name: str) -> Result[object]: ...
