from __future__ import annotations

import asyncio
from pathlib import Path
from typing import override

from returns.result import Failure, Success

from armaden.framework.error.error import Error
from armaden.framework.runtime.supervisor.task.dto.task_graph_data import TaskGraph
from armaden.framework.protocols.task_runtime_protocol import (
    TaskRuntimeProtocol,
)
from armaden.framework.runtime.supervisor.task.task_runtime import TaskError
from armaden.framework.types.coroutine import AsyncStreamCallback
from armaden.framework.types.result import Result


class GraphTaskRuntime(TaskRuntimeProtocol):
    def __init__(
        self,
        task_name: str,
        graph_id: str,
        graph: TaskGraph,
        ready_event: asyncio.Event | None = None,
        main_loop: asyncio.AbstractEventLoop | None = None,
    ) -> None:
        self._task_name: str = task_name
        self._graph_id: str = graph_id
        self._graph: TaskGraph = graph
        self._ready_event: asyncio.Event = ready_event or asyncio.Event()
        self._main_loop: asyncio.AbstractEventLoop | None = main_loop
        self._signaled: bool = False

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
    async def dispatch_subprocess(
        self,
        argv: list[str],
        cwd: Path | str | None = None,
        handle_std_stream: AsyncStreamCallback | None = None,
    ) -> Result[str]:
        _ = argv
        _ = cwd
        _ = handle_std_stream
        return Failure(Error(TaskError.SUBPROCESS_ERROR, details={
            'task': self._task_name,
            'message': 'Subprocess dispatch is unavailable from graph runtime.',
        }))

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
        if name not in self._graph.outputs:
            return Failure(Error(TaskError.REQUEST_NOT_FULFILLED, details={
                'task': self._task_name,
                'name': name,
            }))
        return self._graph.outputs[name]
