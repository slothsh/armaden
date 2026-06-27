import asyncio
from asyncio.subprocess import Process
from datetime import datetime
from enum import StrEnum
import logging
import signal
import threading
from asyncio.queues import Queue
from typing import Any, Dict, Generator, List, Self, Set, cast
from threading import Thread
from concurrent.futures import Future

from dataclasses import dataclass, field
from returns.pipeline import is_successful
from returns.result import Failure, Success
from pathlib import Path

from armaden.framework.enums.supervisor_request_kind import SupervisorRequestKind
from armaden.framework.protocols.supervisor_request_interface import SupervisorRequestInterface

from armaden.framework.dto.supervisor_request_data import SupervisorRequestData
from armaden.framework.utils.types import Result, AsyncStreamArg, AsyncStreamCallback
from armaden.framework.errors import Error
from armaden.framework.protocols import TaskInterface

logger = logging.getLogger(__name__)


class Supervisor:
    def __init__(self, event_loop: asyncio.AbstractEventLoop) -> None:
        self._running = False
        self._shutdown_event = asyncio.Event()
        self._main_loop = event_loop

        self._requests_unique: Set[RequestInfoData] = set()
        self._requests_enqueued: Queue[RequestInfoData] = Queue()

        self._task_states: Dict[int, TaskStateData] = {}
        self._task_records: Dict[int, TaskRecord] = {}
        self._processes: List[ProcessInfoData] = []

        self._initialize_signal_handlers()

        self._thread_info_generator = self._new_thread_info_generator()
        self._task_id_generator = self._new_task_id_generator()

        def generate_thread_info() -> ThreadInfoData:
            return next(self._thread_info_generator)
        self._generate_thread_info = generate_thread_info

        def generate_task_id() -> int:
            return next(self._task_id_generator)
        self._generate_task_id = generate_task_id


    # -- Builder Methods ------------------------------------------------------

    def add_task(self, task: TaskInterface) -> Self:
        task_id = self._generate_task_id()
        thread_info = self._generate_thread_info()
        self._task_states[task_id] = self._new_task_state(task_id, thread_info, task, asyncio.new_event_loop())
        self._task_records[task_id] = TaskRecord(
            task_id=task_id,
            name=task.name,
            description=task.description,
            status="pending",
        )
        return self


    def add_tasks(self, tasks: List[TaskInterface]) -> Self:
        for task in tasks:
            self.add_task(task)
        return self


    # -- Lifecycle ------------------------------------------------------------

    async def initialize(self) -> Result[None]:
        for task_state in self._task_states.values():
            self._task_initialize(task_state)

        return Success(None)


    async def run(self) -> Result[None]:
        self._running = True
        self._start_ready_tasks()

        if self._task_states and not any(s.started for s in self._task_states.values()):
            logger.warning("No tasks are running, waiting until shutdown signal is received")

        while not self._shutdown_event.is_set():
            try:
                await self._process_requests_queue()
                await asyncio.wait_for(self._shutdown_event.wait(), timeout=5.0)
            except asyncio.TimeoutError:
                self._start_ready_tasks()
            except Exception as exception:
                logger.error(f"Error in supervisor main event loop: {exception}")

        logger.info('Supervisor event loop finished. Shutting down now...')
        return await self.shutdown()


    async def shutdown(self) -> Result[None]:
        for task_state in self._task_states.values():
            try:
                await self._shutdown_task(task_state)
            except Exception as exception:
                logger.error("An error occurred trying to shutdown task on thread %s: %s", task_state.thread_info.name, exception)

        logger.info("Shutting down supervisor tasks")
        futures = [asyncio.wrap_future(task_state.future) for task_state in self._task_states.values() if task_state.future]
        if futures:
            try:
                await asyncio.wait_for(asyncio.gather(*futures), timeout=30.0)
            except asyncio.TimeoutError:
                logger.warning("Background tasks timed out during exit phase.")
            except Exception as e:
                logger.error(f"Error during background task cleanup: {e}")

        for process_info in self._processes:
            logger.info("Sending interrupt to sub-process PID %s, running on thread %s", process_info.process.pid, threading.current_thread().name)
            process_info.process.send_signal(signal.SIGINT)

        try:
            join_threads = []
            for task_state in self._task_states.values():
                task_state.event_loop.call_soon_threadsafe(task_state.event_loop.stop)
                join_threads.append(task_state.thread)
            for thread in join_threads:
                thread.join(timeout=30.0)
        except Exception as e:
            logger.error(f"Error while waiting for task threads to join: {e}")

        self._running = False

        return Success(None)


    # -- SupervisorLike Protocol Interface-------------------------------------

    async def enqueue_request(self, request: SupervisorRequestInterface) -> Result[None]:
        if not isinstance(request, SupervisorRequestData):
            return Failure(Error(SupervisorError.BAD_REQUEST_DATA, details={
                'request': request
            }))

        asyncio.run_coroutine_threadsafe(self._enqueue_request(cast(SupervisorRequestData, request)), self._main_loop)

        return Success(None)


    async def list_tasks(self) -> Result[List[TaskRecord]]:
        return Success(list(self._task_records.values()))


    # -- Signal Handling ------------------------------------------------------

    def _initialize_signal_handlers(self) -> None:
        for sig in (signal.SIGINT, signal.SIGTERM, signal.SIGQUIT):
            signal.signal(sig, self._handle_os_signal)


    def _handle_os_signal(self, signum: int, frame: Any) -> None:
        logger.info("OS signal caught. Handling signal %s", signal.Signals(signum).name)
        self._shutdown_event.set()


    # -- Helpers --------------------------------------------------------------

    def _start_ready_tasks(self) -> None:
        for task_state in self._task_states.values():
            if task_state.initialized and not task_state.started:
                if not is_successful(result := self._task_run(task_state)):
                    logger.error("Failed to run task on worker thread %s: %s", task_state.thread_info.name, result.failure())
                    continue
                task_state.started = True
                self._update_task_status(task_state.task_id, "running")


    async def _process_requests_queue(self) -> None:
        if self._requests_enqueued.empty():
            return

        async def shutdown_task(task_id: int) -> TaskStateData | None:
            task_state = self._task_states.get(task_id)
            if not task_state:
                return None

            if not is_successful(result := await self._shutdown_task(task_state, cleanup=True)):
                logger.error(result.failure())
                return None

            del self._task_states[task_id]

            new_thread_info = self._generate_thread_info()
            new_task_state = self._new_task_state(
                task_id,
                new_thread_info,
                task_state.task,
                asyncio.new_event_loop()
            )
            self._task_states[task_id] = new_task_state
            self._update_task_status(task_id, "pending")
            return new_task_state

        while not self._requests_enqueued.empty():
            request_info = self._requests_enqueued.get_nowait()
            self._requests_unique.remove(request_info)

            task_id = request_info.data.task_id

            if task_id not in self._task_states:
                logger.warning("Queued request for task ID %s is not in the current task state list. request: %s", task_id, request_info)
                continue

            task_state = self._task_states[task_id]
            logger.info('Processing request for %s', task_state.thread_info.name)

            match request_info.data.kind:
                case SupervisorRequestKind.SHUTDOWN:
                    if new_task_state := await shutdown_task(task_id):
                        logger.info('Task %s on thread %s successfully shutdown', task_id, new_task_state.thread_info.name)
                case SupervisorRequestKind.RESTART:
                    if task_state.started and (new_task_state := await shutdown_task(task_id)):
                        logger.info('Reinitializing new task state for restarted task %s on thread %s', task_id, new_task_state.thread_info.name)
                        self._task_initialize(new_task_state)
                    elif not task_state.started and not task_state.initialized:
                        self._task_initialize(task_state)

        self._start_ready_tasks()


    def _task_initialize(self, task_state: TaskStateData) -> Result[None]:
        task_state.thread.start()

        runtime = TaskRuntime(task_state)

        init_callback = task_state.task.initialize
        if init_callback is not None:
            future = asyncio.run_coroutine_threadsafe(init_callback(runtime), task_state.event_loop)
            future.add_done_callback(lambda future, task_id=task_state.task_id: self._task_initialization_callback(future, task_id))
        else:
            task_state.initialized = True
            self._update_task_status(task_state.task_id, "initialized")

        return Success(None)


    def _task_run(self, task_state: TaskStateData) -> Result[None]:
        runtime = TaskRuntime(task_state)

        async def run(runtime: 'TaskRuntimeInterface') -> Result[None]:
            return await task_state.task.run(runtime)

        task_state.future = asyncio.run_coroutine_threadsafe(
            run(runtime),
            task_state.event_loop
        )

        return Success(None)


    def _new_thread_info_generator(self) -> Generator[ThreadInfoData, None, None]:
        while True:
            used_thread_ids: List[int] = [s.thread_info.id for s in self._task_states.values()]

            available_thread_ids = [
                n
                for a, b in zip(used_thread_ids, used_thread_ids[1:])
                for n in range(a + 1, b)
            ] if len(used_thread_ids) != 1 else [n + 1 for n in used_thread_ids]

            thread_id = available_thread_ids[0] if available_thread_ids else 1

            yield ThreadInfoData(
                id=thread_id,
                name=f"WorkerThread-{thread_id:02}"
            )


    def _new_task_id_generator(self) -> Generator[int, None, None]:
        task_id = 1
        while True:
            yield task_id
            task_id += 1


    async def _shutdown_task(self, task_state: TaskStateData, cleanup: bool = False) -> Result[None]:
        if task_state.initialized or task_state.started:
            shutdown_callback = task_state.task.shutdown
            if shutdown_callback is not None:
                runtime = TaskRuntime(task_state)
                await shutdown_callback(runtime)
            task_state.initialized = False
            task_state.started = False
            self._update_task_status(task_state.task_id, "stopped")

        for process_info in task_state.processes:
            if process_info.process.returncode is None:
                logger.info("Sending interrupt to sub-process PID %s, running on task worker thread %s", process_info.process.pid, task_state.thread_info.name)
                process_info.process.send_signal(signal.SIGINT)

        if not cleanup:
            return Success(None)

        if task_state.future:
            try:
                logger.info("Awaiting task future for thread %s to complete", task_state.thread_info.name)
                await asyncio.wait_for(asyncio.wrap_future(task_state.future), timeout=30.0)
            except asyncio.TimeoutError:
                logger.warning("Background task on thread ID %s timed out during exit phase.", task_state.thread_info.id)
            except Exception as exception:
                logger.error("Error during background task cleanup: %s", exception)

        logger.info("Joining thread %s", task_state.thread_info.name)
        task_state.event_loop.call_soon_threadsafe(task_state.event_loop.stop)
        task_state.thread.join(timeout=30.0)

        return Success(None)


    def _new_task_state(self, task_id: int, thread_info: ThreadInfoData, task: TaskInterface, event_loop: asyncio.AbstractEventLoop) -> TaskStateData:
        return TaskStateData(
            task_id=task_id,
            thread_info=thread_info,
            task=task,
            initialized=False,
            future=None,
            event_loop=event_loop,
            processes=[],
            thread=Thread(
                name=thread_info.name,
                target=Supervisor._start_worker_event_loop,
                args=(event_loop,),
                daemon=True
            )
        )


    async def _enqueue_request(self, request: SupervisorRequestData) -> Result[None]:
        match request.kind:
            case SupervisorRequestKind.SHUTDOWN:
                if request.task_id not in self._task_states:
                    message = f"Cannot shutdown task because task with ID {request.task_id} was not found."
                    logger.info(message)
                    return Failure(Error(SupervisorError.REQUEST_NOT_FULFILLED, details={
                        'message': message
                    }))
                elif not self._task_states[request.task_id].started:
                    message = f"Task with task ID {request.task_id} cannot be shutdown because it is not running."
                    logger.info(message)
                    return Failure(Error(SupervisorError.REQUEST_NOT_FULFILLED, details={
                        'message': message
                    }))

            case SupervisorRequestKind.RESTART:
                if request.task_id not in self._task_states:
                    message = f"Cannot restart task because task with ID {request.task_id} was not found."
                    logger.warning(message)
                    return Failure(Error(SupervisorError.REQUEST_NOT_FULFILLED, details={
                        'message': message
                    }))

        request_info = RequestInfoData(request)

        if not request_info in self._requests_unique:
            logger.info('Enqueuing request for task ID %s', request.task_id)
            self._requests_enqueued.put_nowait(request_info)
            self._requests_unique.add(request_info)
        else:
            logger.warning('An existing request has already been queued. Ignoring: %s', request)
            return Failure(Error(SupervisorError.REQUEST_IGNORED, details={ 'request': request }))

        return Success(None)


    def _update_task_status(self, task_id: int, status: str) -> None:
        if record := self._task_records.get(task_id):
            self._task_records[task_id] = TaskRecord(
                task_id=record.task_id,
                name=record.name,
                description=record.description,
                status=status,
            )


    # -- Threading ------------------------------------------------------------

    @classmethod
    def _start_worker_event_loop(cls, event_loop: asyncio.AbstractEventLoop) -> Result[None]:
        try:
            asyncio.set_event_loop(event_loop)
            event_loop.run_forever()
        finally:
            event_loop.close()

        return Success(None)

    def _task_initialization_callback(self, future: Future[Result[None]], task_id: int) -> Result[None]:
        try:
            if not is_successful(result := future.result()):
                logger.error(f"initialization of task {task_id} failed due to error: {result.failure()}")
                return result

            if task_state := self._task_states.get(task_id):
                task_state.initialized = True
                self._update_task_status(task_id, "initialized")
        except Exception as exception:
            logger.error(f"initialization of task {task_id} failed due to an exception: {exception}")

        return Success(None)


# -- Internal Types -----------------------------------------------------------

class TaskRuntime:
    def __init__(self, task_state: TaskStateData) -> None:
        self._task_state = task_state

    @property
    def name(self) -> str:
        return self._task_state.task.name

    async def dispatch_subprocess(
        self,
        argv: List[str],
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

        tasks: List[asyncio.Task[None]] = []
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
                            await callback(line)
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
        await asyncio.gather(*tasks)

        if return_code == 0:
            return Success("Subprocess executed successfully")
        else:
            return Failure(Error(SupervisorError.SUBPROCESS_ERROR, details={
                'details': 'Subprocess failed. Check console for errors.'
            }))


class SupervisorError(StrEnum):
    INITIALIZATION_FAILED = "an error occurred while initializing the supervisor"
    SUBPROCESS_ERROR = "a non-zero exit code occurred when running a subprocess"
    REQUEST_IGNORED = "the provided request has been ignored"
    BAD_REQUEST_DATA = "the provided supervisor request data is invalid"
    REQUEST_NOT_FULFILLED = "the specified request could not be fulfilled"

@dataclass
class TaskStateData:
    task_id: int
    thread_info: ThreadInfoData
    task: TaskInterface
    initialized: bool
    future: Future[Result[None]] | None
    event_loop: asyncio.AbstractEventLoop
    processes: List[ProcessInfoData]
    thread: Thread
    started: bool = False


@dataclass(frozen=True)
class TaskRecord:
    task_id: int
    name: str | None
    description: str | None
    status: str


@dataclass(frozen=True)
class ThreadInfoData:
    id: int
    name: str


@dataclass(frozen=True)
class ProcessInfoData:
    name: str
    process: Process


@dataclass(frozen=True)
class RequestInfoData:
    data: SupervisorRequestData
    time_received: datetime = field(default=datetime.now(), compare=False)
