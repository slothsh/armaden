from collections.abc import Callable

from server.lib import Result
from typing import List, Protocol, Self
from pathlib import Path
from abc import ABC, abstractmethod


class QueueableSupervisor(Protocol):
    async def queue_start(self) -> None: ...
    async def queue_shutdown(self) -> None: ...
    async def queue_restart(self) -> None: ...
    async def queue_reload(self, config_path: str | Path) -> None: ...
    async def dispatch_subprocess(self, argv: List[str]) -> Result[str]: ...


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
        return [str(self._executable), *self._params]


    def consume_argv(self) -> List[str]:
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


    def push(self, flag: str, *values: str | int) -> None:
        self._params.append(flag)
        for value in values:
            self._params.append(str(value))


    def reset_params(self) -> None:
        self._params.clear()


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
