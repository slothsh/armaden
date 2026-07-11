import asyncio
from asyncio.subprocess import Process
from datetime import datetime
from enum import StrEnum
import logging
import os
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

from armaden.framework.classes.instance_container import InstanceContainer
from armaden.framework.enums.supervisor_request_kind import SupervisorRequestKind
from armaden.framework.enums.task_threading_policy import TaskThreadingPolicy
from armaden.framework.protocols.supervisor_request_interface import SupervisorRequestInterface

from armaden.framework.dto.supervisor_request_data import SupervisorRequestData
from armaden.framework.utils.types import Result, AsyncStreamArg, AsyncStreamCallback
from armaden.framework.errors import Error
from armaden.framework.protocols import TaskInterface, TaskRuntimeInterface
from armaden.framework.runtime.errors import TaskError
from armaden.framework.runtime.policy_engine import PolicyEngine
from armaden.framework.runtime.progress import ProgressChannel
from armaden.framework.runtime.task import Task as TaskABC
from armaden.framework.runtime.task_graph import TaskGraph, TaskGraphCompiler, TaskGraphState
from armaden.framework.runtime.task_injector import TaskInjector
from armaden.framework.runtime.task_runtime import TaskRuntime as GraphTaskRuntime

logger = logging.getLogger(__name__)


class Supervisor:
    def __init__(
        self,
        event_loop: asyncio.AbstractEventLoop,
        container: InstanceContainer | None = None,
        pool_size: int | None = None,
        max_exclusive_threads: int = 8,
    ) -> None:
        self._container = container
        self._max_exclusive_threads = max_exclusive_threads
        self._pool_size = pool_size or (os.cpu_count() or 4)
        self._running = False
        self._shutdown_event = asyncio.Event()
        self._main_loop = event_loop

        self._requests_unique: Set[RequestInfoData] = set()
        self._requests_enqueued: Queue[RequestInfoData] = Queue()

        self._task_states: Dict[int, TaskStateData] = {}
        self._task_records: Dict[int, TaskRecord] = {}
        self._processes: List[ProcessInfoData] = []

        self._graphs: List[TaskGraph] = []
        self._compiler = TaskGraphCompiler()
        self._policy_engine = PolicyEngine()
        self._injector = TaskInjector(container) if container is not None else None
        self._worker_pool: WorkerPool | None = None
        self._scheduler = None

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
        if isinstance(task, TaskABC):
            self.submit([task])
            return self
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
        abc_tasks = [t for t in tasks if isinstance(t, TaskABC)]
        legacy_tasks = [t for t in tasks if not isinstance(t, TaskABC)]
        if abc_tasks:
            self.submit(abc_tasks)
        for task in legacy_tasks:
            self.add_task(task)
        return self


    def submit(self, tasks: list) -> TaskGraph:
        graph = self._compiler.compile(list(tasks))
        graph.state = TaskGraphState.PENDING
        self._graphs.append(graph)
        return graph

    # -- Facade accessors (stubs — implementation in later tasks) --------------

    def process(self):
        from armaden.framework.runtime.facades.process import ProcessFacade
        return ProcessFacade(self)

    def schedule(self):
        from armaden.framework.runtime.facades.schedule import ScheduleFacade
        return ScheduleFacade(self)

    def concurrency(self):
        from armaden.framework.runtime.facades.concurrency import ConcurrencyFacade
        return ConcurrencyFacade(self)

    def list_schedules(self) -> list:
        if self._scheduler is None:
            return []
        return [
            {'name': job.id, 'trigger': str(job.trigger), 'next_run_time': job.next_run_time}
            for job in self._scheduler.get_jobs()
        ]

    def remove_schedule(self, name: str) -> None:
        if self._scheduler is not None:
            try:
                self._scheduler.remove_job(name)
            except Exception:
                pass

    def _ensure_scheduler(self):
        if self._scheduler is not None:
            return self._scheduler
        try:
            from apscheduler.schedulers.asyncio import AsyncIOScheduler
        except ImportError:
            raise RuntimeError(
                'APScheduler is required for scheduled tasks. Install with: pip install apscheduler'
            )
        self._scheduler = AsyncIOScheduler()
        self._scheduler.start()
        return self._scheduler


    # -- Lifecycle ------------------------------------------------------------

    async def initialize(self) -> Result[None]:
        for task_state in self._task_states.values():
            self._task_initialize(task_state)

        return Success(None)


    async def run(self) -> Result[None]:
        self._running = True
        self._start_ready_tasks()

        try:
            await self._execute_graphs()
        except Exception as exception:
            logger.error('Graph execution raised: %s', exception)

        if self._task_states and not any(s.started for s in self._task_states.values()):
            if not self._graphs:
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


    # -- Graph Execution ------------------------------------------------------

    async def _execute_graphs(self) -> None:
        pending = [g for g in self._graphs if g.state in (TaskGraphState.PENDING, TaskGraphState.RUNNING)]
        for graph in pending:
            try:
                await self._execute_graph(graph)
            except Exception as exception:
                logger.exception('Graph %s execution failed: %s', graph.graph_id, exception)
                graph.state = TaskGraphState.FAILED

    async def _execute_graph(self, graph: TaskGraph) -> None:
        graph.state = TaskGraphState.RUNNING
        injector = self._injector or TaskInjector(self._container) if self._container is not None else None
        if injector is None:
            injector = TaskInjector(None)

        for layer in graph.layers:
            await self._execute_layer(graph, layer, injector)
            if graph.state == TaskGraphState.FAILED:
                break

        if graph.state != TaskGraphState.FAILED:
            graph.state = TaskGraphState.COMPLETED

    async def _execute_layer(self, graph: TaskGraph, layer: list[str], injector: TaskInjector) -> None:
        tasks = [graph.tasks[name] for name in layer]
        long_running = any(getattr(t, 'long_running', False) for t in tasks)

        coros: dict[str, asyncio.Task] = {}
        ready_events: dict[str, asyncio.Event] = {}
        for task in tasks:
            event = asyncio.Event()
            ready_events[task.name] = event
            runtime = GraphTaskRuntime(
                task_name=task.name,
                graph_id=graph.graph_id,
                graph=graph,
                ready_event=event,
            )
            coros[task.name] = asyncio.create_task(self._run_one_task(task, runtime, graph, injector))

        if long_running:
            done, pending = await asyncio.wait(
                coros.values(), return_when=asyncio.ALL_COMPLETED
            )
        else:
            await asyncio.gather(*coros.values())

        for name, task in zip(layer, tasks):
            name = task.name
            coro = coros.get(name)
            result = coro.result() if coro is not None else None
            if result is not None:
                graph.outputs[name] = result
            if result is not None and not is_successful(result):
                task_obj = graph.tasks[name]
                if not (task_obj.policy.continue_on_failure if hasattr(task_obj, 'policy') else False):
                    graph.state = TaskGraphState.FAILED
                    graph.errors.append(_result_error(result))
                    return

    async def _run_one_task(self, task, runtime, graph: TaskGraph, injector: TaskInjector):
        try:
            if hasattr(task, 'initialize') and callable(getattr(task, 'initialize', None)):
                init_kwargs = await injector.resolve(task, task.initialize, graph, runtime) if hasattr(task.initialize, '__call__') else {}
                init_result = task.initialize(**init_kwargs)
                if hasattr(init_result, '__await__'):
                    await init_result
            result = await self._policy_engine.execute(task, runtime, injector, graph)
            return result
        except Exception as exception:
            logger.exception('Task %s failed: %s', task.name, exception)
            return Failure(Error(TaskError.SUBPROCESS_ERROR, details={'task': task.name, 'error': str(exception)}))
        finally:
            try:
                if hasattr(task, 'shutdown') and callable(getattr(task, 'shutdown', None)):
                    shutdown_kwargs = await injector.resolve(task, task.shutdown, graph, runtime) if hasattr(task.shutdown, '__call__') else {}
                    shutdown_result = task.shutdown(**shutdown_kwargs)
                    if hasattr(shutdown_result, '__await__'):
                        await shutdown_result
            except Exception:
                logger.exception('Task %s shutdown failed', task.name)


    # -- Signal Handling ------------------------------------------------------

    def _initialize_signal_handlers(self) -> None:
        for sig in (signal.SIGINT, signal.SIGTERM, signal.SIGQUIT):
            signal.signal(sig, self._handle_os_signal)


    def _handle_os_signal(self, signum: int, frame: Any) -> None:
        _ = frame
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

        async def run(runtime: TaskRuntimeInterface) -> Result[None]:
            return await task_state.task.run(runtime)

        task_state.future = asyncio.run_coroutine_threadsafe(
            run(runtime),
            task_state.event_loop
        )

        return Success(None)


    def _new_thread_info_generator(self) -> Generator[ThreadInfoData, None, None]:
        while True:
            used_thread_ids: List[int] = sorted([s.thread_info.id for s in self._task_states.values()])

            available_thread_ids = [
                n
                for s, e in zip(used_thread_ids, used_thread_ids[1:])
                for n in range(s + 1, e)
            ]

            thread_id = available_thread_ids[0] if available_thread_ids else used_thread_ids[-1] + 1 if used_thread_ids and used_thread_ids[0] == 1 else 1

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


def _result_error(result):
    failure = result.failure() if hasattr(result, 'failure') else result
    if isinstance(failure, Error):
        return failure
    return Error(TaskError.SUBPROCESS_ERROR, details={'error': str(failure)})


# -- Internal Types -----------------------------------------------------------

class TaskRuntime:
    def __init__(self, task_state: TaskStateData) -> None:
        self._task_state = task_state

    @property
    def name(self) -> str | None:
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


# -- WorkerPool --------------------------------------------------------------

class _WorkerBase:
    def __init__(self, name: str) -> None:
        self.name = name
        self.loop: asyncio.AbstractEventLoop = asyncio.new_event_loop()
        self.thread = Thread(target=self._run_loop, name=name, daemon=True)
        self.busy = False
        self.thread.start()

    def _run_loop(self) -> None:
        asyncio.set_event_loop(self.loop)
        self.loop.run_forever()

    def shutdown(self) -> None:
        try:
            self.loop.call_soon_threadsafe(self.loop.stop)
        except RuntimeError:
            pass
        self.thread.join(timeout=5.0)


class _SharedWorker(_WorkerBase):
    pass


class _ExclusiveWorker(_WorkerBase):
    pass


class WorkerPool:
    def __init__(self, pool_size: int, max_exclusive_threads: int) -> None:
        self._pool_size = pool_size
        self._max_exclusive_threads = max_exclusive_threads
        self._shared: list[_SharedWorker] = [
            _SharedWorker(f'shared-worker-{i}') for i in range(pool_size)
        ]
        self._free: asyncio.Queue[_SharedWorker] = asyncio.Queue()
        for worker in self._shared:
            self._free.put_nowait(worker)
        self._exclusive: dict[str, _ExclusiveWorker] = {}
        self._lock = asyncio.Lock()

    async def acquire_shared(self) -> _SharedWorker:
        return await self._free.get()

    async def release_shared(self, worker: _SharedWorker) -> None:
        worker.busy = False
        await self._free.put(worker)

    async def acquire_exclusive(self, task_name: str) -> _ExclusiveWorker:
        async with self._lock:
            if len(self._exclusive) >= self._max_exclusive_threads:
                raise RuntimeError(
                    f'Exclusive thread capacity reached ({self._max_exclusive_threads}); '
                    f'cannot start task \"{task_name}\"'
                )
            worker = _ExclusiveWorker(f'exclusive-worker-{task_name}')
            self._exclusive[task_name] = worker
            return worker

    async def release_exclusive(self, task_name: str) -> None:
        async with self._lock:
            worker = self._exclusive.pop(task_name, None)
        if worker is not None:
            worker.shutdown()

    def shutdown(self) -> None:
        for worker in self._shared:
            worker.shutdown()
        for worker in list(self._exclusive.values()):
            worker.shutdown()
        self._exclusive.clear()
