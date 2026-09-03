from armaden.framework.types.coroutine import AsyncStreamCallback
from armaden.framework.types.result import Result
from pathlib import Path
from typing import Any, Protocol

class TaskRuntimeProtocol(Protocol):
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
