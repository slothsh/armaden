from typing import Protocol

from armaden.framework.types.result import Result


class SubprocessHandleProtocol(Protocol):
    pid: int | None

    async def stop(self) -> Result[None]: ...
