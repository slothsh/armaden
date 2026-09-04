from __future__ import annotations

import asyncio
import logging
import os
import signal
from enum import StrEnum
from pathlib import Path

from returns.result import Failure, Success

from armaden.framework.error.error import Error
from armaden.framework.runtime.supervisor.task.enums.subprocess_handle_state import (
    SubprocessHandleState,
)
from armaden.framework.types.result import Result

logger = logging.getLogger(__name__)


class SubprocessHandleError(StrEnum):
    SUBPROCESS_ERROR = 'a subprocess handle could not start the process'


class SubprocessHandle:
    def __init__(self, name: str) -> None:
        self.name: str = name
        self.process: asyncio.subprocess.Process | None = None
        self.pid: int | None = None
        self.state: SubprocessHandleState = SubprocessHandleState.STARTING


    async def restart(self) -> Result[None]:
        _ = await self.stop()
        raise NotImplementedError('SubprocessHandle.restart requires stored argv')


    async def start(
        self,
        argv: list[str],
        cwd: Path | str | None = None,
        env: dict[str, str] | None = None,
    ) -> Result[None]:
        try:
            full_env = os.environ.copy()
            if env is not None:
                full_env.update(env)
            self.process = await asyncio.create_subprocess_exec(
                argv[0],
                *argv[1:],
                cwd=cwd,
                env=full_env,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            self.pid = self.process.pid
            self.state = SubprocessHandleState.RUNNING
            return Success(None)
        except Exception as exception:
            return Failure(Error(SubprocessHandleError.SUBPROCESS_ERROR, details={
                'name': self.name,
                'error': str(exception),
            }))


    def send_signal(self, sig: int) -> None:
        if self.process is not None:
            self.process.send_signal(sig)


    async def stop(self, timeout: float = 30.0) -> Result[None]:
        process = self.process
        if process is None or self.state == SubprocessHandleState.STOPPED:
            return Success(None)
        self.state = SubprocessHandleState.STOPPING
        try:
            try:
                _ = process.send_signal(signal.SIGINT)
                _ = await asyncio.wait_for(process.wait(), timeout=timeout)
            except asyncio.TimeoutError:
                logger.warning(
                    "Process '%s' did not exit on SIGINT; escalating to SIGTERM",
                    self.name,
                )
                _ = process.terminate()
                try:
                    _ = await asyncio.wait_for(process.wait(), timeout=timeout)
                except asyncio.TimeoutError:
                    logger.warning(
                        "Process '%s' did not exit on SIGTERM; escalating to SIGKILL",
                        self.name,
                    )
                    _ = process.kill()
                    _ = await process.wait()
            except ProcessLookupError:
                pass
        finally:
            self.state = SubprocessHandleState.STOPPED
            self.process = None
            self.pid = None
        return Success(None)
