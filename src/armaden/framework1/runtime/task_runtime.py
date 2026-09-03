import asyncio
import logging
from pathlib import Path
from typing import Any

from returns.result import Failure, Success

from armaden.framework.errors import Error
from armaden.framework.protocols.task_runtime import AsyncStreamCallback, Result
from armaden.framework.runtime.errors import TaskError
from armaden.framework.runtime.progress import ProgressChannel

logger = logging.getLogger(__name__)


class TaskRuntime:
    def __init__(
        self,
        task_name: str,
        graph_id: str,
        task_state: Any = None,
        progress: ProgressChannel | None = None,
        ready_event: asyncio.Event | None = None,
        graph: Any = None,
        main_loop: asyncio.AbstractEventLoop | None = None,
    ) -> None:
        self._task_name = task_name
        self._graph_id = graph_id
        self._task_state = task_state
        self._progress = progress or ProgressChannel()
        self._ready_event = ready_event or asyncio.Event()
        self._graph = graph
        self._main_loop = main_loop
        self._signaled = False

    @property
    def name(self) -> str | None:
        return self._task_name

    @property
    def graph_id(self) -> str:
        return self._graph_id

    @property
    def progress(self) -> ProgressChannel:
        return self._progress

    async def signal_ready(self) -> Result[None]:
        if self._signaled:
            logger.warning("Task '%s' signaled ready more than once; ignoring duplicate", self._task_name)
            return Success(None)
        self._signaled = True

        if self._graph is not None:
            self._graph.lifecycle_signals[self._task_name] = Success(None)

        if self._main_loop is not None and self._main_loop is not asyncio.get_running_loop():
            self._main_loop.call_soon_threadsafe(self._ready_event.set)
        else:
            self._ready_event.set()

        logger.info("Task '%s' signaled ready", self._task_name)
        return Success(None)

    @property
    def ready_event(self) -> asyncio.Event:
        return self._ready_event

    async def task_output(self, name: str) -> Result[Any]:
        if self._graph is None:
            return Failure(Error(TaskError.UNRESOLVED_DEPENDENCY, details={'name': name}))
        outputs = getattr(self._graph, 'outputs', {})
        if name not in outputs:
            return Failure(Error(TaskError.UNRESOLVED_DEPENDENCY, details={'name': name}))
        return outputs[name]

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
            async def drain(stream, callback: AsyncStreamCallback) -> None:
                if not stream:
                    return
                try:
                    while True:
                        line_bytes = await stream.readline()
                        if not line_bytes:
                            break
                        if line := line_bytes.decode(errors='replace').strip():
                            await callback(line)
                except asyncio.CancelledError:
                    raise

            tasks.append(asyncio.create_task(drain(process.stdout, handle_std_stream)))
            tasks.append(asyncio.create_task(drain(process.stderr, handle_std_stream)))

        try:
            return_code = await process.wait()
            await asyncio.gather(*tasks)
        except asyncio.CancelledError:
            for t in tasks:
                t.cancel()
            if tasks:
                await asyncio.gather(*tasks, return_exceptions=True)
            raise
        finally:
            for t in tasks:
                if not t.done():
                    t.cancel()
            if tasks:
                await asyncio.gather(*tasks, return_exceptions=True)

        if return_code == 0:
            return Success("Subprocess executed successfully")
        return Failure(Error(TaskError.SUBPROCESS_ERROR, details={
            'details': 'Subprocess failed. Check console for errors.'
        }))
