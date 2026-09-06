from __future__ import annotations

import asyncio
import inspect
import logging
import os
import signal
import threading
from asyncio.queues import Queue
from collections.abc import Awaitable, Callable, Generator
from concurrent.futures import Future
from enum import Enum, StrEnum
from threading import Thread
from typing import Self, cast, override

from returns.pipeline import is_successful
from returns.result import Failure, Success

from armaden.framework.runtime.schedule.dto.schedule_execution_options_data import (
    ScheduleExecutionOptionsData,
)
from armaden.framework.facades.facade import Facade
from armaden.framework.runtime.error.error import Error
from armaden.framework.runtime.container.container import Container
from armaden.framework.runtime.supervisor.dto.active_coroutine_data import ActiveCoroutineData
from armaden.framework.runtime.supervisor.dto.process_info_data import ProcessInfoData
from armaden.framework.runtime.supervisor.dto.request_info_data import (
    SupervisorRequestData,
    SupervisorRequestInfoData,
)
from armaden.framework.runtime.supervisor.dto.task_state_data import TaskStateData
from armaden.framework.runtime.supervisor.dto.thread_info_data import ThreadInfoData
from armaden.framework.runtime.supervisor.enums.supervisor_request_kind import (
    SupervisorRequestKind,
)
from armaden.framework.runtime.supervisor.task.dto.task_record_data import TaskRecordData
from armaden.framework.runtime.supervisor.task.enums.task_graph_state import TaskGraphState
from armaden.framework.runtime.supervisor.task.dto.task_graph_data import TaskGraphData
from armaden.framework.runtime.supervisor.task.task_graph_compiler import TaskGraphCompiler
from armaden.framework.runtime.supervisor.task.graph_task_runtime import GraphTaskRuntime
from armaden.framework.runtime.supervisor.task.task_injector import TaskInjector
from armaden.framework.runtime.supervisor.task.policy_engine import PolicyEngine
from armaden.framework.runtime.supervisor.task.enums.task_threading_policy import TaskThreadingPolicy
from armaden.framework.protocols.scheduler_protocol import SchedulerProtocol
from armaden.framework.protocols.supervisor_protocol import SupervisorProtocol
from armaden.framework.protocols.task_protocol import TaskProtocol
from armaden.framework.protocols.task_runtime_protocol import (
    TaskRuntimeProtocol,
)
from armaden.framework.runtime.supervisor.task.task_runtime import TaskRuntime
from armaden.framework.runtime.schedule.scheduled_invocation_task import ScheduledInvocationTask
from armaden.framework.runtime.supervisor.worker.worker_pool import WorkerPool
from armaden.framework.types.result import Result
from armaden.framework.types.schedule import ScheduleCallback


logger = logging.getLogger(__name__)


class Supervisor(SupervisorProtocol[TaskGraphData]):
    def __init__(
        self,
        event_loop: asyncio.AbstractEventLoop,
        container: Container | None = None,
        pool_size: int | None = None,
        max_exclusive_threads: int = 8,
    ) -> None:
        def generate_thread_info() -> ThreadInfoData:
            return next(self._thread_info_generator)

        def generate_task_id() -> int:
            return next(self._task_id_generator)

        self._initialize_signal_handlers()

        self._active_coros: dict[int, ActiveCoroutineData] = {}
        self._compiler: TaskGraphCompiler = TaskGraphCompiler()
        self._container: Container | None = container
        self._generate_task_id: Callable[[], int] = generate_task_id
        self._generate_thread_info: Callable[[], ThreadInfoData] = generate_thread_info
        self._graphs: list[TaskGraphData] = []
        self._initialized: bool = False
        self._injector: TaskInjector = TaskInjector(container)
        self._main_loop: asyncio.AbstractEventLoop = event_loop
        self._max_exclusive_threads: int = max_exclusive_threads
        self._policy_engine: PolicyEngine = PolicyEngine()
        self._pool_size: int = pool_size or (os.cpu_count() or 4)
        self._processes: list[ProcessInfoData] = []
        self._requests_enqueued: Queue[SupervisorRequestInfoData] = Queue()
        self._requests_unique: set[SupervisorRequestInfoData] = set()
        self._running: bool = False
        self._scheduler: SchedulerProtocol | None = None
        self._shutdown_completed: bool = False
        self._shutdown_event: asyncio.Event = asyncio.Event()
        self._shutdown_task_ids: set[int] = set()
        self._task_id_generator: Generator[int, None, None] = self._new_task_id_generator()
        self._task_records: dict[int, TaskRecordData] = {}
        self._task_states: dict[int, TaskStateData] = {}
        self._thread_info_generator: Generator[ThreadInfoData, None, None] = self._new_thread_info_generator()
        self._worker_pool: WorkerPool | None = None

        if container is not None:
            Facade.set_facade_application(container)
            _ = container.instance(SupervisorProtocol, self)


    async def _await_long_running_ready(
        self,
        task: TaskProtocol[Enum],
        coro: asyncio.Task[object],
        runtime: GraphTaskRuntime,
        graph: TaskGraphData,
        ready_timeout: float | None,
    ) -> None:
        ready_wait = asyncio.create_task(runtime.ready_event.wait())
        try:
            _ = await asyncio.wait(
                {coro, ready_wait},
                timeout=ready_timeout,
                return_when=asyncio.FIRST_COMPLETED,
            )
        finally:
            if not ready_wait.done():
                _ = ready_wait.cancel()

        if runtime.ready_event.is_set():
            return
        if coro.done():
            return
        if ready_timeout is not None:
            logger.warning(
                "Long-running task '%s' failed to signal ready within %.2fs",
                task.name, ready_timeout,
            )
            graph.lifecycle_signals[task.name] = Failure(
                Error(SupervisorError.READY_TIMEOUT, details={'task': task.name})
            )


    async def _dispatch_to_worker(
        self,
        task: TaskProtocol[Enum],
        runtime: GraphTaskRuntime,
        graph: TaskGraphData,
        injector: TaskInjector,
        semaphore: asyncio.Semaphore | None = None,
    ) -> Result[object]:
        if self._worker_pool is None:
            self._worker_pool = WorkerPool(self._pool_size, self._max_exclusive_threads)

        policy = getattr(task, 'threading_policy', TaskThreadingPolicy.SHARED)

        try:
            if policy == TaskThreadingPolicy.EXCLUSIVE:
                worker = await self._worker_pool.acquire_exclusive(task.name)
                if getattr(task, 'long_running', False) and id(task) in self._active_coros:
                    self._active_coros[id(task)].loop = worker.loop
                task_ref: dict[str, asyncio.Task[object]] = {}
                future = asyncio.run_coroutine_threadsafe(
                    self._run_wrapped_task(task, runtime, graph, injector, task_ref),
                    worker.loop,
                )
                try:
                    return await asyncio.wrap_future(future)
                finally:
                    self._drain_worker_future(future, worker.loop, task_ref)
                    await self._worker_pool.release_exclusive(task.name)

            if semaphore is not None:
                _ = await semaphore.acquire()
            try:
                worker = await self._worker_pool.acquire_shared()
                if getattr(task, 'long_running', False) and id(task) in self._active_coros:
                    self._active_coros[id(task)].loop = worker.loop
                task_ref = {}
                future = asyncio.run_coroutine_threadsafe(
                    self._run_wrapped_task(task, runtime, graph, injector, task_ref),
                    worker.loop,
                )
                try:
                    return await asyncio.wrap_future(future)
                finally:
                    self._drain_worker_future(future, worker.loop, task_ref)
                    await self._worker_pool.release_shared(worker)
            finally:
                if semaphore is not None:
                    _ = semaphore.release()
        except RuntimeError as exception:
            logger.error('Worker dispatch failed for task %s: %s', task.name, exception)
            return Failure(Error(SupervisorError.SUBPROCESS_ERROR, details={
                'task': task.name, 'error': str(exception),
            }))


    def _drain_worker_future(
        self,
        future: Future[Result[object]],
        worker_loop: asyncio.AbstractEventLoop,
        task_ref: dict[str, asyncio.Task[object]],
    ) -> None:
        worker_task = task_ref.get('task')
        if worker_task is not None and not worker_task.done():
            _ = worker_loop.call_soon_threadsafe(worker_task.cancel)
            try:
                _ = future.result(timeout=30.0)
            except Exception:
                pass
            try:
                sync_fut = asyncio.run_coroutine_threadsafe(asyncio.sleep(0), worker_loop)
                _ = sync_fut.result(timeout=5.0)
            except Exception:
                pass


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

        request_info = SupervisorRequestInfoData(request)

        if not request_info in self._requests_unique:
            logger.info('Enqueuing request for task ID %s', request.task_id)
            self._requests_enqueued.put_nowait(request_info)
            self._requests_unique.add(request_info)
        else:
            logger.warning('An existing request has already been queued. Ignoring: %s', request)
            return Failure(Error(SupervisorError.REQUEST_IGNORED, details={ 'request': request }))

        return Success(None)


    @override
    def ensure_scheduler(self) -> SchedulerProtocol:
        if self._scheduler is not None:
            return self._scheduler
        try:
            module = __import__('apscheduler.schedulers.asyncio', fromlist=['AsyncIOScheduler'])
            scheduler_type = cast(type[SchedulerProtocol], getattr(module, 'AsyncIOScheduler'))
        except ImportError as exception:
            raise RuntimeError(
                'APScheduler is required for scheduled tasks. Install with: pip install apscheduler'
            ) from exception
        scheduler_factory = cast(Callable[..., SchedulerProtocol], scheduler_type)
        scheduler = scheduler_factory(event_loop=self._main_loop)
        _ = scheduler.start()
        self._scheduler = scheduler
        container = self._container
        if container is not None:
            _ = container.instance(SchedulerProtocol, scheduler)
        return self._scheduler


    @override
    async def execute_graph(self, graph: TaskGraphData) -> None:
        graph.state = TaskGraphState.RUNNING
        injector = self._injector

        for layer in graph.layers:
            await self._execute_layer(graph, layer, injector)
            if str(graph.state) == TaskGraphState.FAILED.value:
                break

        if str(graph.state) != TaskGraphState.FAILED.value:
            graph.state = TaskGraphState.COMPLETED


    async def _execute_graphs(self) -> None:
        pending = [g for g in self._graphs if g.state in (TaskGraphState.PENDING, TaskGraphState.RUNNING)]
        for graph in pending:
            try:
                await self.execute_graph(graph)
                if graph.state == TaskGraphState.FAILED:
                    logger.error(
                        'Task graph %s failed with %d error(s)',
                        graph.graph_id,
                        len(graph.errors),
                    )
                    for error in graph.errors:
                        logger.error('Task graph %s failure: %s', graph.graph_id, error)
            except Exception as exception:
                logger.exception('Graph %s execution failed: %s', graph.graph_id, exception)
                graph.state = TaskGraphState.FAILED


    async def _execute_layer(self, graph: TaskGraphData, layer: list[str], injector: TaskInjector) -> None:
        tasks = sorted(
            (graph.tasks[name] for name in layer),
            key=lambda task: -task.policy.priority,
        )

        semaphore = None
        if graph.max_concurrency is not None and graph.max_concurrency > 0:
            semaphore = asyncio.Semaphore(graph.max_concurrency)

        coros: dict[str, asyncio.Task[object]] = {}
        runtimes: dict[str, GraphTaskRuntime] = {}
        for task in tasks:
            event = asyncio.Event()
            runtime = GraphTaskRuntime(
                task_name=task.name,
                graph_id=graph.graph_id,
                graph=graph,
                ready_event=event,
                main_loop=self._main_loop,
            )
            runtimes[task.name] = runtime
            coro = asyncio.create_task(
                self._dispatch_to_worker(task, runtime, graph, injector, semaphore)
            )
            coros[task.name] = coro
            if getattr(task, 'long_running', False):
                self._active_coros[id(task)] = ActiveCoroutineData(
                    coro=coro,
                    loop=None,
                    runtime=runtime,
                )
                task_id = id(task)

                def remove_completed_task(_future: asyncio.Task[Result[object]]) -> None:
                    _ = self._active_coros.pop(task_id, None)

                coro.add_done_callback(remove_completed_task)

        signals: list[asyncio.Task[object]] = []
        for task in tasks:
            coro = coros[task.name]
            if getattr(task, 'long_running', False):
                ready_timeout = task.policy.ready_timeout
                signals.append(asyncio.create_task(
                    self._await_long_running_ready(task, coro, runtimes[task.name], graph, ready_timeout)
                ))
            else:
                signals.append(coro)

        if signals:
            _ = await asyncio.gather(*signals, return_exceptions=True)

        for task in tasks:
            name = task.name
            coro = coros.get(name)
            if getattr(task, 'long_running', False):
                if name not in graph.lifecycle_signals and coro is not None and coro.done():
                    result = cast(Result[object] | None, coro.result() if not coro.cancelled() else None)
                    if result is not None:
                        graph.outputs[name] = result
                    if result is not None and not is_successful(result):
                        if not task.policy.continue_on_failure:
                            graph.state = TaskGraphState.FAILED
                            graph.errors.append(self._result_error(result))
                            return
                continue

            result = cast(Result[object] | None, coro.result() if coro is not None and coro.done() and not coro.cancelled() else None)
            if result is not None:
                graph.outputs[name] = result
            if result is not None and not is_successful(result):
                if not task.policy.continue_on_failure:
                    graph.state = TaskGraphState.FAILED
                    graph.errors.append(self._result_error(result))
                    return


    def _handle_os_signal(self, signum: int, frame: object) -> None:
        _ = frame
        logger.info("OS signal caught. Handling signal %s", signal.Signals(signum).name)
        self._shutdown_event.set()


    def _initialize_signal_handlers(self) -> None:
        for sig in (signal.SIGINT, signal.SIGTERM, signal.SIGQUIT):
            _ = signal.signal(sig, self._handle_os_signal)


    def _new_task_id_generator(self) -> Generator[int, None, None]:
        task_id = 1
        while True:
            yield task_id
            task_id += 1


    def _new_task_state(self, task_id: int, thread_info: ThreadInfoData, task: TaskProtocol[Enum], event_loop: asyncio.AbstractEventLoop) -> TaskStateData:
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


    def _new_thread_info_generator(self) -> Generator[ThreadInfoData, None, None]:
        while True:
            used_thread_ids: list[int] = sorted([s.thread_info.id for s in self._task_states.values()])

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
                        _ = self._task_initialize(new_task_state)
                    elif not task_state.started and not task_state.initialized:
                        _ = self._task_initialize(task_state)

        self._start_ready_tasks()


    @staticmethod
    def _result_error(result: Result[object]) -> Error:
        failure = result.failure()
        if isinstance(failure, Error):
            return failure
        return Error(SupervisorError.SUBPROCESS_ERROR, details={'error': str(failure)})


    async def _run_one_task(
        self,
        task: TaskProtocol[Enum],
        runtime: GraphTaskRuntime,
        graph: TaskGraphData,
        injector: TaskInjector,
    ) -> Result[object]:
        setattr(task, '_runtime_ref', runtime)
        setattr(task, '_injector_ref', injector)
        setattr(task, '_graph_ref', graph)
        try:
            init_callback = task.initialize
            if init_callback is not None:
                init_kwargs = await injector.resolve(task, init_callback, graph, runtime)
                initialize_callback = cast(
                    Callable[..., Awaitable[Result[None]]],
                    init_callback,
                )
                init_result: object = initialize_callback(**init_kwargs)
                if inspect.isawaitable(init_result):
                    init_result = await cast(Awaitable[object], init_result)
                typed_init_result = cast(Result[None], init_result)
                if not is_successful(typed_init_result):
                    return typed_init_result
            result = await self._policy_engine.execute(task, runtime, injector, graph)
            return result
        except Exception as exception:
            logger.exception('Task %s failed: %s', task.name, exception)
            return Failure(Error(SupervisorError.SUBPROCESS_ERROR, details={'task': task.name, 'error': str(exception)}))
        finally:
            setattr(task, '_runtime_ref', None)
            setattr(task, '_injector_ref', None)
            setattr(task, '_graph_ref', None)


    async def _run_shutdown(
        self,
        task: TaskProtocol[Enum],
        injector: TaskInjector,
        graph: TaskGraphData,
        runtime: TaskRuntimeProtocol,
    ) -> Result[object] | None:
        shutdown_callback = task.shutdown
        if shutdown_callback is None:
            return None
        setattr(task, '_runtime_ref', runtime)
        setattr(task, '_injector_ref', injector)
        setattr(task, '_graph_ref', graph)
        try:
            shutdown_kwargs = await injector.resolve(
                task,
                shutdown_callback,
                graph,
                runtime,
            )
            shutdown_function = cast(
                Callable[..., Awaitable[Result[object]]],
                shutdown_callback,
            )
            result = shutdown_function(**shutdown_kwargs)
            if inspect.isawaitable(result):
                return await result
            return result
        finally:
            setattr(task, '_runtime_ref', None)
            setattr(task, '_injector_ref', None)
            setattr(task, '_graph_ref', None)


    async def _run_wrapped_task(
        self,
        task: TaskProtocol[Enum],
        runtime: GraphTaskRuntime,
        graph: TaskGraphData,
        injector: TaskInjector,
        task_ref: dict[str, asyncio.Task[object]],
    ) -> Result[object]:
        worker_task = asyncio.current_task()
        if worker_task is not None:
            task_ref['task'] = cast(asyncio.Task[object], worker_task)
        return await self._run_one_task(task, runtime, graph, injector)


    async def _shutdown_task(self, task_state: TaskStateData, cleanup: bool = False) -> Result[None]:
        if task_state.initialized or task_state.started:
            shutdown_callback = task_state.task.shutdown
            if shutdown_callback is not None:
                runtime = TaskRuntime(task_state)
                _ = await shutdown_callback(runtime)
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
                _ = await asyncio.wait_for(asyncio.wrap_future(task_state.future), timeout=30.0)
            except asyncio.TimeoutError:
                logger.warning("Background task on thread ID %s timed out during exit phase.", task_state.thread_info.id)
            except Exception as exception:
                logger.error("Error during background task cleanup: %s", exception)

        logger.info("Joining thread %s", task_state.thread_info.name)
        _ = task_state.event_loop.call_soon_threadsafe(task_state.event_loop.stop)
        task_state.thread.join(timeout=30.0)

        return Success(None)


    def _start_ready_tasks(self) -> None:
        for task_state in self._task_states.values():
            if task_state.initialized and not task_state.started:
                if not is_successful(result := self._task_run(task_state)):
                    logger.error("Failed to run task on worker thread %s: %s", task_state.thread_info.name, result.failure())
                    continue
                task_state.started = True
                self._update_task_status(task_state.task_id, "running")


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

        async def run(runtime: TaskRuntimeProtocol) -> Result[object]:
            return await task_state.task.run(runtime)

        task_state.future = asyncio.run_coroutine_threadsafe(
            run(runtime),
            task_state.event_loop
        )

        return Success(None)


    def _update_task_status(self, task_id: int, status: str) -> None:
        if record := self._task_records.get(task_id):
            self._task_records[task_id] = TaskRecordData(
                task_id=record.task_id,
                name=record.name,
                description=record.description,
                status=status,
            )


    def add_task(self, task: TaskProtocol[Enum]) -> Self:
        task_id = self._generate_task_id()
        thread_info = self._generate_thread_info()
        self._task_states[task_id] = self._new_task_state(task_id, thread_info, task, asyncio.new_event_loop())
        self._task_records[task_id] = TaskRecordData(
            task_id=task_id,
            name=task.name,
            description=task.description,
            status="pending",
        )
        return self


    def add_tasks(self, tasks: list[TaskProtocol[Enum]]) -> Self:
        for task in tasks:
            _ = self.add_task(task)
        return self


    @override
    async def dispatch_scheduled(
        self,
        name: str,
        callback: ScheduleCallback,
        options: object,
    ) -> Result[object]:
        schedule_options = cast(ScheduleExecutionOptionsData, options)
        task = ScheduledInvocationTask(name, callback, schedule_options)
        return await self.dispatch_task(task, schedule_options.run_in_background)


    @override
    async def dispatch_task(
        self,
        task: TaskProtocol[Enum],
        run_in_background: bool = False,
    ) -> Result[object]:
        graph = self.submit([task])
        if run_in_background:
            _ = asyncio.create_task(self.execute_graph(graph))
            return Success(graph)
        await self.execute_graph(graph)
        return Success(graph)


    @override
    async def enqueue_request(self, request: object) -> Result[None]:
        request_data = cast(SupervisorRequestData, request)
        _ = asyncio.run_coroutine_threadsafe(self._enqueue_request(request_data), self._main_loop)

        return Success(None)


    @override
    async def initialize(self) -> Result[None]:
        if self._initialized:
            return Success(None)
        if self._worker_pool is None:
            self._worker_pool = WorkerPool(self._pool_size, self._max_exclusive_threads)

        for task_state in self._task_states.values():
            _ = self._task_initialize(task_state)
        self._initialized = True

        return Success(None)


    def list_schedules(self) -> list[dict[str, object]]:
        if self._scheduler is None:
            return []
        schedules: list[dict[str, object]] = []
        for job in self._scheduler.get_jobs():
            job_id = getattr(job, 'id', None)
            trigger = getattr(job, 'trigger', None)
            next_run_time = getattr(job, 'next_run_time', None)
            schedules.append({
                'name': job_id,
                'trigger': str(trigger),
                'next_run_time': next_run_time,
            })
        return schedules


    async def list_tasks(self) -> Result[list[TaskRecordData]]:
        return Success(list(self._task_records.values()))


    def remove_schedule(self, name: str) -> None:
        if self._scheduler is not None:
            try:
                _ = self._scheduler.remove_job(name)
            except Exception:
                pass


    @override
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
                _ = await asyncio.wait_for(self._shutdown_event.wait(), timeout=5.0)
            except asyncio.TimeoutError:
                self._start_ready_tasks()
            except Exception as exception:
                logger.error(f"Error in supervisor main event loop: {exception}")

        logger.info('Supervisor event loop finished. Shutting down now...')
        return await self.shutdown()


    async def shutdown(self) -> Result[None]:
        if getattr(self, '_shutdown_completed', False):
            return Success(None)
        self._shutdown_completed = True

        Facade.clear_resolved_instances()

        self._shutdown_event.set()

        injector = self._injector

        for graph in list(self._graphs):
            for task_name in graph.shutdown_order:
                task = graph.tasks.get(task_name)
                if task is None:
                    continue
                task_id = id(task)
                if task_id in self._shutdown_task_ids:
                    continue

                entry = self._active_coros.get(task_id)
                if entry is not None and not entry.coro.done():
                    worker_loop = entry.loop
                    runtime = entry.runtime
                    if worker_loop is not None:
                        try:
                            if worker_loop is asyncio.get_running_loop():
                                _ = await self._run_shutdown(task, injector, graph, runtime)
                            else:
                                fut = asyncio.run_coroutine_threadsafe(
                                    self._run_shutdown(task, injector, graph, runtime),
                                    worker_loop,
                                )
                                _ = await asyncio.wrap_future(fut)
                        except Exception as exception:
                            logger.error('Task %s shutdown failed: %s', task_name, exception)

                    if not entry.coro.done():
                        _ = entry.coro.cancel()
                        try:
                            await entry.coro
                        except (asyncio.CancelledError, Exception):
                            pass
                    self._shutdown_task_ids.add(task_id)
                    continue

                self._shutdown_task_ids.add(task_id)
                try:
                    runtime = GraphTaskRuntime(
                        task_name=task.name,
                        graph_id=graph.graph_id,
                        graph=graph,
                        main_loop=self._main_loop,
                    )
                    _ = await self._run_shutdown(task, injector, graph, runtime)
                except Exception as exception:
                    logger.error('Task %s shutdown failed: %s', task_name, exception)
                finally:
                    setattr(task, '_runtime_ref', None)
                    setattr(task, '_injector_ref', None)
                    setattr(task, '_graph_ref', None)

        remaining_coros = [
            entry.coro
            for entry in self._active_coros.values()
            if not entry.coro.done()
        ]
        for coro in remaining_coros:
            _ = coro.cancel()
        if remaining_coros:
            try:
                _ = await asyncio.wait_for(
                    asyncio.gather(*remaining_coros, return_exceptions=True),
                    timeout=30.0,
                )
            except asyncio.TimeoutError:
                logger.warning('Long-running graph tasks timed out during shutdown.')
            except Exception as exception:
                logger.error('Error during graph task cleanup: %s', exception)
            self._active_coros.clear()

        for task_state in self._task_states.values():
            try:
                _ = await self._shutdown_task(task_state)
            except Exception as exception:
                logger.error("An error occurred trying to shutdown task on thread %s: %s", task_state.thread_info.name, exception)

        logger.info("Shutting down supervisor tasks")
        futures = [asyncio.wrap_future(task_state.future) for task_state in self._task_states.values() if task_state.future]
        if futures:
            try:
                _ = await asyncio.wait_for(asyncio.gather(*futures), timeout=30.0)
            except asyncio.TimeoutError:
                logger.warning("Background tasks timed out during exit phase.")
            except Exception as e:
                logger.error(f"Error during background task cleanup: {e}")

        for process_info in self._processes:
            logger.info("Sending interrupt to sub-process PID %s, running on thread %s", process_info.process.pid, threading.current_thread().name)
            process_info.process.send_signal(signal.SIGINT)

        try:
            join_threads: list[Thread] = []
            for task_state in self._task_states.values():
                _ = task_state.event_loop.call_soon_threadsafe(task_state.event_loop.stop)
                join_threads.append(task_state.thread)
            for thread in join_threads:
                thread.join(timeout=30.0)
        except Exception as e:
            logger.error(f"Error while waiting for task threads to join: {e}")

        if self._scheduler is not None:
            try:
                _ = self._scheduler.shutdown(wait=False)
            except Exception as exception:
                logger.error('APScheduler shutdown failed: %s', exception)
            finally:
                self._scheduler = None

        if self._worker_pool is not None:
            try:
                self._worker_pool.shutdown()
            except Exception as exception:
                logger.error('WorkerPool shutdown failed: %s', exception)

        self._running = False

        return Success(None)


    @override
    def submit(self, tasks: list[TaskProtocol[Enum]]) -> TaskGraphData:
        graph = self._compiler.compile(list(tasks))
        graph.state = TaskGraphState.PENDING
        self._graphs.append(graph)
        return graph


class SupervisorError(StrEnum):
    INITIALIZATION_FAILED = "an error occurred while initializing the supervisor"
    SUBPROCESS_ERROR = "a non-zero exit code occurred when running a subprocess"
    READY_TIMEOUT = "task did not signal readiness before the timeout"
    REQUEST_IGNORED = "the provided request has been ignored"
    BAD_REQUEST_DATA = "the provided supervisor request data is invalid"
    REQUEST_NOT_FULFILLED = "the specified request could not be fulfilled"
