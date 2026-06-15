import asyncio
from collections.abc import Callable, Coroutine
from typing import List, Protocol, Self, Any
from pathlib import Path
from abc import ABC, abstractmethod

from server.lib import Result
from server.lib.facades import env

type PushValue = str | bool | int | float | Path | list[PushValue]
type AsyncStreamArg = asyncio.StreamReader | None
type AsyncStreamCallback = Callable[[str], Coroutine[Any, Any, Result[None]]]


class QueueableSupervisor(Protocol):
    async def queue_start(self) -> None: ...
    async def queue_shutdown(self) -> None: ...
    async def queue_restart(self) -> None: ...
    async def queue_reload(self, config_path: str | Path) -> None: ...
    async def dispatch_subprocess(self, argv: List[str], cwd: Path | str | None = None, handle_std_stream: AsyncStreamCallback | None = None) -> Result[str]: ...


class Executable(ABC):
    def __init__(
            self,
            resolve_executable: Callable[[], Result[Path]]
    ) -> None:
        self._params: List[str] = []
        self._scratch_params: List[str] = []

        executable = resolve_executable().value_or(None)
        self._executable: Path | None = executable


    def build_argv(self) -> List[str]:
        if env('APP_ENV') in ['testing', 'local']:
            return [str(Path("scripts/loop_echo.sh").absolute()), "-n", "3"]

        return [str(self._executable), *self._params]


    def consume_argv(self) -> List[str]:
        if env('APP_ENV') in ['testing', 'local']:
            return [str(Path("scripts/loop_echo.sh").absolute()), "-n", "3"]

        argv = self.build_argv()
        self.reset_params()
        return argv


    def save_params(self) -> Self:
        self._scratch_params = self._params
        self._params.clear()
        return self


    def clear_params(self) -> Self:
        self.reset_params()
        return self


    def restore_params(self) -> None:
        self._params = self._scratch_params
        self._scratch_params.clear()



    def push(self, flag: str, *values: PushValue) -> None:
        truthy_values: list[str] = []
        for v in values:
            serialized = self._serialize_value(v)
            if serialized is not None:
                truthy_values.append(serialized)
        if values and not truthy_values:
            return
        self._params.append(flag)
        self._params.extend(truthy_values)


    def reset_params(self) -> None:
        self._params.clear()


    def _serialize_value(self, value: PushValue) -> str | None:
        if value is None or value == "":
            return None
        if isinstance(value, bool):
            return "true" if value else "false"
        if isinstance(value, list):
            parts: list[str] = []
            for item in value:
                serialized = self._serialize_value(item)
                if serialized is not None:
                    parts.append(serialized)
            return ",".join(parts) if parts else None
        if isinstance(value, Path):
            return str(value)
        return str(value)


class Server(ABC):
    @abstractmethod
    async def initialize(self) -> Result[None]:
        pass


    @abstractmethod
    async def run(self) -> Result[None]:
        pass


    @abstractmethod
    async def shutdown(self) -> Result[None]:
        pass
