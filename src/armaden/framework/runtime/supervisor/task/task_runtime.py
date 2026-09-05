from __future__ import annotations

import asyncio
import logging
from enum import StrEnum
from pathlib import Path
from typing import override

from returns.result import Failure, Success

from armaden.framework.runtime.error.error import Error
from armaden.framework.protocols.task_runtime_protocol import TaskRuntimeProtocol
from armaden.framework.runtime.supervisor.dto.process_info_data import ProcessInfoData
from armaden.framework.runtime.supervisor.dto.task_state_data import TaskStateData
from armaden.framework.types.coroutine import AsyncStreamArg, AsyncStreamCallback
from armaden.framework.types.result import Result

logger = logging.getLogger(__name__)


class TaskRuntime(TaskRuntimeProtocol):
    def __init__(self, task_state: TaskStateData) -> None:
        self._task_state: TaskStateData = task_state


    @override
    async def dispatch_subprocess(
        self,
        argv: list[str],
        cwd: Path | str | None = None,
        handle_std_stream: AsyncStreamCallback | None = None,
    ) -> Result[str]:
        logger.info('Executing command in subprocess: %s', ' '.join(argv))

        process = await asyncio.create_subprocess_exec(
            argv[0], *argv[1:],
            cwd=cwd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        tasks: list[asyncio.Task[None]] = []
        if handle_std_stream:
            async def drain(stream: AsyncStreamArg, callback: AsyncStreamCallback) -> None:
                if not stream:
                    return

                try:
                    while True:
                        line_bytes = await stream.readline()
                        if not line_bytes:
                            break
                        if line := line_bytes.decode(errors='replace').strip():
                            _ = await callback(line)
                except asyncio.CancelledError:
                    raise

            tasks.append(asyncio.create_task(drain(process.stdout, handle_std_stream)))
            tasks.append(asyncio.create_task(drain(process.stderr, handle_std_stream)))

        process_info = ProcessInfoData(
            name=self._task_state.thread_info.name,
            process=process,
        )
        self._task_state.processes.append(process_info)

        try:
            return_code = await process.wait()
            _ = await asyncio.gather(*tasks)
        except asyncio.CancelledError:
            for task in tasks:
                _ = task.cancel()
            if tasks:
                _ = await asyncio.gather(*tasks, return_exceptions=True)
            raise
        finally:
            for task in tasks:
                if not task.done():
                    _ = task.cancel()
            if tasks:
                _ = await asyncio.gather(*tasks, return_exceptions=True)

        if return_code == 0:
            return Success('Subprocess executed successfully')
        return Failure(Error(TaskRuntimeError.SUBPROCESS_ERROR, details={
            'details': 'Subprocess failed. Check console for errors.',
        }))


    @property
    @override
    def graph_id(self) -> str:
        return f'legacy-{self._task_state.task_id}'


    @property
    @override
    def name(self) -> str:
        return self._task_state.task.name


    @override
    async def signal_ready(self) -> Result[None]:
        logger.warning("signal_ready() called on legacy TaskRuntime for task '%s'; no-op", self.name)
        return Success(None)


    @override
    async def task_output(self, name: str) -> Result[object]:
        return Failure(Error(TaskRuntimeError.REQUEST_NOT_FULFILLED, details={
            'message': 'task_output not available on legacy TaskRuntime',
            'name': name,
        }))


class TaskRuntimeError(StrEnum):
    MAX_RETRIES_EXCEEDED = 'maximum task retries exceeded'
    READY_TIMEOUT = 'task did not signal readiness before the timeout'
    REQUEST_NOT_FULFILLED = 'the specified request could not be fulfilled'
    SUBPROCESS_ERROR = 'a non-zero exit code occurred when running a subprocess'
    TIMEOUT = 'task execution timed out'
    UNRESOLVED_DEPENDENCY = 'task dependency could not be resolved'
