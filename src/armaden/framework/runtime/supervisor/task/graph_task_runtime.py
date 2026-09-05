from __future__ import annotations

import asyncio
import logging
from enum import StrEnum
from pathlib import Path
from typing import cast, override

from returns.result import Failure, Success

from armaden.framework.runtime.error.error import Error
from armaden.framework.protocols.task_runtime_protocol import TaskRuntimeProtocol
from armaden.framework.runtime.supervisor.task.dto.task_graph_data import TaskGraphData
from armaden.framework.types.coroutine import AsyncStreamArg, AsyncStreamCallback
from armaden.framework.types.result import Result

logger = logging.getLogger(__name__)


class GraphTaskRuntimeError(StrEnum):
    REQUEST_NOT_FULFILLED = 'the specified graph task runtime request could not be fulfilled'
    SUBPROCESS_ERROR = 'a graph task runtime subprocess failed'


class GraphTaskRuntime(TaskRuntimeProtocol):
    def __init__(
        self,
        task_name: str,
        graph_id: str,
        graph: TaskGraphData,
        ready_event: asyncio.Event | None = None,
        main_loop: asyncio.AbstractEventLoop | None = None,
    ) -> None:
        self._graph: TaskGraphData = graph
        self._graph_id: str = graph_id
        self._main_loop: asyncio.AbstractEventLoop | None = main_loop
        self._ready_event: asyncio.Event = ready_event or asyncio.Event()
        self._signaled: bool = False
        self._task_name: str = task_name


    @override
    async def dispatch_subprocess(
        self,
        argv: list[str],
        cwd: Path | str | None = None,
        handle_std_stream: AsyncStreamCallback | None = None,
    ) -> Result[str]:
        logger.info('Executing command in subprocess: %s', ' '.join(argv))
        process = await asyncio.create_subprocess_exec(
            argv[0],
            *argv[1:],
            cwd=cwd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        stream_tasks: list[asyncio.Task[None]] = []
        if handle_std_stream is not None:
            async def drain(stream: AsyncStreamArg) -> None:
                if stream is None:
                    return
                while True:
                    line_bytes = await stream.readline()
                    if not line_bytes:
                        return
                    if line := line_bytes.decode(errors='replace').strip():
                        _ = await handle_std_stream(line)

            stream_tasks.append(asyncio.create_task(drain(process.stdout)))
            stream_tasks.append(asyncio.create_task(drain(process.stderr)))

        try:
            return_code = await process.wait()
            _ = await asyncio.gather(*stream_tasks)
        except asyncio.CancelledError:
            for stream_task in stream_tasks:
                _ = stream_task.cancel()
            if stream_tasks:
                _ = await asyncio.gather(*stream_tasks, return_exceptions=True)
            raise
        finally:
            for stream_task in stream_tasks:
                if not stream_task.done():
                    _ = stream_task.cancel()
            if stream_tasks:
                _ = await asyncio.gather(*stream_tasks, return_exceptions=True)

        if return_code == 0:
            return Success('Subprocess executed successfully')
        return Failure(Error(GraphTaskRuntimeError.SUBPROCESS_ERROR, details={
            'task': self._task_name,
            'message': 'Subprocess failed. Check console for errors.',
        }))


    @property
    @override
    def graph_id(self) -> str:
        return self._graph_id


    @property
    @override
    def name(self) -> str:
        return self._task_name


    @property
    def ready_event(self) -> asyncio.Event:
        return self._ready_event


    @override
    async def signal_ready(self) -> Result[None]:
        if self._signaled:
            return Success(None)
        self._signaled = True
        self._graph.lifecycle_signals[self._task_name] = Success(None)
        if self._main_loop is not None and self._main_loop is not asyncio.get_running_loop():
            _ = self._main_loop.call_soon_threadsafe(self._ready_event.set)
        else:
            self._ready_event.set()
        return Success(None)


    @override
    async def task_output(self, name: str) -> Result[object]:
        if name in self._graph.outputs:
            return self._graph.outputs[name]
        if name in self._graph.lifecycle_signals:
            return cast(Result[object], self._graph.lifecycle_signals[name])
        return Failure(Error(GraphTaskRuntimeError.REQUEST_NOT_FULFILLED, details={
            'task': self._task_name,
            'name': name,
        }))
