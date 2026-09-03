from armaden.framework.error.error import Error
from armaden.framework.runtime.supervisor.dto.process_info_data import ProcessInfoData
from armaden.framework.runtime.supervisor.dto.task_state_data import TaskStateData
from armaden.framework.types.coroutine import AsyncStreamArg, AsyncStreamCallback
from armaden.framework.types.result import Result
from enum import StrEnum
from pathlib import Path
from returns.result import Success, Failure
from typing import Any
import asyncio
import logging

logger = logging.getLogger(__name__)


class TaskRuntime:
    def __init__(self, task_state: TaskStateData) -> None:
        self._task_state: TaskStateData = task_state


    @property
    def name(self) -> str | None:
        return self._task_state.task.name


    @property
    def graph_id(self) -> str:
        return f'legacy-{self._task_state.task_id}'


    async def signal_ready(self) -> Result[None]:
        logger.warning("signal_ready() called on legacy TaskRuntime for task '%s'; no-op", self.name)
        return Success(None)


    async def task_output(self, name: str) -> Result[Any]:
        return Failure(Error(TaskError.REQUEST_NOT_FULFILLED, details={
            'message': f'task_output not available on legacy TaskRuntime', 'name': name,
        }))


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
            stderr=asyncio.subprocess.PIPE
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

            tasks.append(asyncio.create_task(
                drain(process.stdout, handle_std_stream)
            ))

            tasks.append(asyncio.create_task(
                drain(process.stderr, handle_std_stream)
            ))

        process_info = ProcessInfoData(name=self._task_state.thread_info.name, process=process)
        self._task_state.processes.append(process_info)

        return_code = await process.wait()
        _ = await asyncio.gather(*tasks)

        if return_code == 0:
            return Success("Subprocess executed successfully")
        else:
            return Failure(Error(TaskError.SUBPROCESS_ERROR, details={
                'details': 'Subprocess failed. Check console for errors.'
            }))


class TaskError(StrEnum):
    REQUEST_NOT_FULFILLED = "the specified request could not be fulfilled"
    SUBPROCESS_ERROR = "a non-zero exit code occurred when running a subprocess"
