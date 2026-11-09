from __future__ import annotations

from collections.abc import Callable, Coroutine
from pathlib import Path
from typing import Any, Protocol

from armaden.framework.protocols.subprocess_handle_protocol import (
    SubprocessHandleProtocol,
)
from armaden.framework.types.coroutine import AsyncStreamCallback
from armaden.framework.types.result import Result

type SubprocessLaunchCallback = Callable[[SubprocessHandleProtocol], Coroutine[Any, Any, Result[None]]]


class TaskRuntimeProtocol(Protocol):
    async def dispatch_subprocess(
        self,
        argv: list[str],
        cwd: Path | str | None = None,
        handle_std_stream: AsyncStreamCallback | None = None,
        env: dict[str, str] | None = None,
        on_launch: SubprocessLaunchCallback | None = None,
    ) -> Result[str]: ...

    @property
    def graph_id(self) -> str: ...

    @property
    def name(self) -> str: ...

    async def signal_ready(self) -> Result[None]: ...

    async def task_output(self, name: str) -> Result[object]: ...
