from __future__ import annotations

import asyncio
import inspect
from enum import StrEnum
from pathlib import Path
from typing import override

from returns.pipeline import is_successful
from returns.result import Failure, Success

from armaden.framework.runtime.error.error import Error
from armaden.framework.runtime.supervisor.task.dto.task_policy_data import TaskPolicyData
from armaden.framework.runtime.supervisor.task.task import Task
from armaden.framework.runtime.supervisor.task.subprocess_handle import SubprocessHandle
from armaden.framework.protocols.task_runtime_protocol import TaskRuntimeProtocol
from armaden.framework.types.process import ProcessStreamCallback
from armaden.framework.types.result import Result


class ProcessTaskError(StrEnum):
    SUBPROCESS_ERROR = 'a non-zero exit code occurred in a process task'


class ProcessTask(Task):
    def __init__(
        self,
        name: str,
        argv: list[str],
        cwd: Path | str | None = None,
        env: dict[str, str] | None = None,
        on_stdout: ProcessStreamCallback | None = None,
        on_stderr: ProcessStreamCallback | None = None,
        policy: TaskPolicyData | None = None,
        depends_on: list[str | type[object]] | None = None,
        awaits: list[str | type[object]] | None = None,
        long_running: bool = False,
    ) -> None:
        super().__init__(
            name=name,
            policy=policy,
            depends_on=depends_on,
            awaits=awaits,
            long_running=long_running,
        )
        self._argv: list[str] = list(argv)
        self._cwd: Path | str | None = cwd
        self._env: dict[str, str] | None = None if env is None else dict(env)
        self._handle: SubprocessHandle | None = None
        self._on_stderr: ProcessStreamCallback | None = on_stderr
        self._on_stdout: ProcessStreamCallback | None = on_stdout


    @property
    def handle(self) -> SubprocessHandle | None:
        return self._handle


    async def _drain(
        self,
        stream: asyncio.StreamReader,
        callback: ProcessStreamCallback | None,
    ) -> None:
        while True:
            line_bytes = await stream.readline()
            if not line_bytes:
                return
            if not (line := line_bytes.decode(errors='replace').strip()):
                continue
            if callback is None:
                continue
            result = callback(line)
            if inspect.isawaitable(result):
                await result


    @override
    async def run(
        self,
        runtime: TaskRuntimeProtocol,
        **kwargs: object,
    ) -> Result[object]:
        _ = kwargs
        handle = SubprocessHandle(self.name)
        self._handle = handle
        start_result = await handle.start(self._argv, cwd=self._cwd, env=self._env)
        if not is_successful(start_result):
            return start_result

        process = handle.process
        if process is None:
            return Failure(Error(ProcessTaskError.SUBPROCESS_ERROR, details={
                'name': self.name,
                'message': 'Subprocess handle did not retain its process.',
            }))
        if self.long_running:
            _ = await runtime.signal_ready()

        pump_tasks = [
            asyncio.create_task(self._drain(process.stdout, self._on_stdout))
            if process.stdout is not None
            else None,
            asyncio.create_task(self._drain(process.stderr, self._on_stderr))
            if process.stderr is not None
            else None,
        ]
        active_pump_tasks = [task for task in pump_tasks if task is not None]
        try:
            return_code = await process.wait()
            _ = await asyncio.gather(*active_pump_tasks, return_exceptions=True)
        except asyncio.CancelledError:
            for task in active_pump_tasks:
                _ = task.cancel()
            if active_pump_tasks:
                _ = await asyncio.gather(*active_pump_tasks, return_exceptions=True)
            _ = await handle.stop()
            raise
        finally:
            for task in active_pump_tasks:
                if not task.done():
                    _ = task.cancel()
            if active_pump_tasks:
                _ = await asyncio.gather(*active_pump_tasks, return_exceptions=True)

        if return_code == 0:
            return Success(return_code)
        return Failure(Error(ProcessTaskError.SUBPROCESS_ERROR, details={
            'name': self.name,
            'exit_code': return_code,
        }))


    @override
    async def shutdown(
        self,
        runtime: TaskRuntimeProtocol,
        **kwargs: object,
    ) -> Result[None]:
        _ = kwargs
        _ = runtime
        if self._handle is not None:
            _ = await self._handle.stop()
        return Success(None)