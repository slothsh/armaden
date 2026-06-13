from collections.abc import Callable

from server.lib import Result
from typing import List, Protocol
from pathlib import Path
from abc import ABC, abstractmethod


class QueueableSupervisor(Protocol):
    def queue_start(self) -> None: ...
    def queue_shutdown(self) -> None: ...
    def queue_restart(self) -> None: ...
    def queue_reload(self, config_path: str | Path) -> None: ...


class Executable(ABC):
    def __init__(
            self,
            resolve_executable: Callable[[], Result[Path]]
    ) -> None:
        self._params: List[str] = []

        executable = resolve_executable().value_or(None)
        self._executable: Path | None = executable


    def build_argv(self) -> List[str]:
        return [str(self._executable), *self._params]


    def push(self, flag: str, *values: str | int) -> None:
        self._params.append(flag)
        for value in values:
            self._params.append(str(value))


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
