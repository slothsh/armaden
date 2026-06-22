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

from framework.enums.supervisor_request_kind import SupervisorRequestKind
from framework.protocols.supervisor_request_interface import SupervisorRequestInterface

from framework.dto.supervisor_request_data import SupervisorRequestData
from framework.utils.types import Result, AsyncStreamArg,  AsyncStreamCallback
from framework.errors import Error
from framework.protocols import ServerInterface

logger = logging.getLogger(__name__)


class Supervisor:
    def __init__(self, event_loop: asyncio.AbstractEventLoop) -> None:
        self._running = False
        self._shutdown_event = asyncio.Event()
        self._main_loop = event_loop

        self._requests_unique: Set[RequestInfoData] = set()
        self._requests_enqueued: Queue[RequestInfoData] = Queue()

        self._server_states: Dict[ThreadInfoData, ServerStateData] = {}
        self._processes: List[ProcessInfoData] = []

        self._initialize_signal_handlers()

        self._thread_info_generator = self._new_thread_info_generator()
        def generate_thread_info() -> ThreadInfoData:
            return next(self._thread_info_generator)
        self._generate_thread_info = generate_thread_info


    # -- Builder Methods ------------------------------------------------------

    def with_server(self, server: ServerInterface) -> Self:
        worker_event_loop = asyncio.new_event_loop()
        thread_info = self._generate_thread_info()
        self._server_states[thread_info] = self._new_server_state(thread_info.name, server, worker_event_loop)
        return self


    def with_servers(self, servers: List[ServerInterface]) -> Self:
        for server in servers:
            self.with_server(server)
        return self


    # -- Lifecycle ------------------------------------------------------------

    async def initialize(self) -> Result[None]:
        for thread_info, server_state in self._server_states.items():
            self._server_initialize(thread_info, server_state)

        return Success(None)


    async def run(self) -> Result[None]:
        self._running = True
        self._start_ready_servers()

        if self._server_states and not any(s.started for s in self._server_states.values()):
            logger.warning("No servers are running, waiting until shutdown signal is received")

        while not self._shutdown_event.is_set():
            try:
                await self._process_requests_queue()
                await asyncio.wait_for(self._shutdown_event.wait(), timeout=5.0)
            except asyncio.TimeoutError:
                self._start_ready_servers()
            except Exception as exception:
                logger.error(f"Error in in supervisor main event loop: {exception}")

        logger.info('Supervisor event loop finished. Shutting down now...')
        return await self.shutdown()


    async def shutdown(self) -> Result[None]:
        for thread_info, server_state in self._server_states.items():
            try:
                await self._shutdown_server(thread_info, server_state)
            except Exception as exception:
                logger.error("An error occurred trying to shutdown server on thread %s: %s", thread_info.name, exception)

        logger.info("Shutting down supervisor servers")
        futures = [asyncio.wrap_future(server_state.future) for server_state in self._server_states.values() if server_state.future]
        if futures:
            try:
                await asyncio.wait_for(asyncio.gather(*futures), timeout=30.0)
            except asyncio.TimeoutError:
                logger.warning("Background servers timed out during exit phase.")
            except Exception as e:
                logger.error(f"Error during background server cleanup: {e}")

        for process_info in self._processes:
            logger.info("Sending interrupt to sub-process PID %s, running on thread %s", process_info.process.pid, threading.current_thread().name)
            process_info.process.send_signal(signal.SIGINT)

        try:
            join_threads = []
            for server_state in self._server_states.values():
                server_state.event_loop.call_soon_threadsafe(server_state.event_loop.stop)
                join_threads.append(server_state.thread)
            for thread in join_threads:
                thread.join(timeout=30.0)
        except Exception as e:
            logger.error(f"Error while waiting for servers threads to join: {e}")

        self._running = False

        return Success(None)


    # -- SupervisorLike Protocol Interface-------------------------------------

    async def enqueue_request(self, request: SupervisorRequestInterface) -> Result[None]:
        if not isinstance(request, SupervisorRequestData):
            return Failure(Error(SupervisorError.BAD_REQUEST_DATA, details={
                'request': request
            }))

        # NOTE: should we do something with the future?
        asyncio.run_coroutine_threadsafe(self._enqueue_request(cast(SupervisorRequestData, request)), self._main_loop)

        return Success(None)


    async def dispatch_subprocess(
        self,
        argv: List[str],
        cwd: Path | str | None = None,
        handle_std_stream: AsyncStreamCallback | None = None,
    ) -> Result[str]:
        logger.info('Executing command in subprocess: %s', ' '.join(argv))

        current_thread_name = threading.current_thread().name
        current_server = [server_state for server_state in self._server_states.values() if server_state.thread.name == current_thread_name]

        process = await asyncio.create_subprocess_exec(
            argv[0], *argv[1:],
            cwd=cwd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        tasks: List[asyncio.Task[None]]  = []
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

        process_info = ProcessInfoData(name=current_thread_name, process=process)
        if len(current_server) == 1:
            current_server[0].processes.append(process_info)
        else:
            self._processes.append(process_info)

        return_code = await process.wait()
        await asyncio.gather(*tasks)

        if return_code == 0:
            return Success("Subprocess executed successfully")
        else:
            return Failure(Error(SupervisorError.SUBPROCESS_ERROR, details={
                'details': 'Subprocess failed. Check console for errors.'
            }))


    # -- Signal Handling ------------------------------------------------------

    def _initialize_signal_handlers(self) -> None:
        for sig in (signal.SIGINT, signal.SIGTERM, signal.SIGQUIT):
            signal.signal(sig, self._handle_os_signal)


    def _handle_os_signal(self, signum: int, frame: Any) -> None:
        logger.info("OS signal caught. Handling signal %s", signal.Signals(signum).name)
        self._shutdown_event.set()


    # -- Helpers --------------------------------------------------------------

    def _start_ready_servers(self) -> None:
        for server_state in self._server_states.values():
            if server_state.initialized and not server_state.started:
                if not is_successful(result := self._server_run(server_state)):
                    logger.error("Failed to run server on worker thread %s: %s", server_state.thread.name, result.failure())
                    continue
                server_state.started = True


    async def _process_requests_queue(self) -> None:
        if self._requests_enqueued.empty():
            return

        async def shutdown_thread(thread_id: int) -> ThreadInfoData | None:
            if not is_successful(result := await self._shutdown_server(*server_states[thread_id], cleanup=True)):
                logger.error(result.failure())
                return None

            (old_thread_info, old_server_state) = server_states[thread_id]
            del self._server_states[old_thread_info]

            new_thread_info = self._generate_thread_info()

            self._server_states[new_thread_info] = self._new_server_state(
                new_thread_info.name,
                old_server_state.server,
                asyncio.new_event_loop()
            )

            return new_thread_info

        server_states = { thread_info.id: (thread_info, server_state) for thread_info, server_state in self._server_states.items() }

        while not self._requests_enqueued.empty():
            request_info = self._requests_enqueued.get_nowait()
            self._requests_unique.remove(request_info)

            thread_id = request_info.data.thread_id

            if thread_id not in server_states:
                logger.warning("Queued request for thread ID %s is not in the current server state list. request: %s", thread_id, request_info)
                continue

            logger.info('Processing request for %s', server_states[thread_id][0].name)

            match request_info.data.kind:
                case SupervisorRequestKind.SHUTDOWN:
                    if new_thread_info := await shutdown_thread(thread_id):
                        logger.info('Server on thread %s (%s) successfully shutdown', new_thread_info.name, new_thread_info.id)
                case SupervisorRequestKind.RESTART:
                    (current_thread_info, current_server_state) = server_states[thread_id]

                    if current_server_state.started and (new_thread_info := await shutdown_thread(thread_id)):
                        logger.info('Reinitializing new server state for restarted server on thread %s (%s)', new_thread_info.name, new_thread_info.id)
                        self._server_initialize(new_thread_info, self._server_states[new_thread_info])
                    elif not current_server_state.started and not current_server_state.initialized:
                        self._server_initialize(current_thread_info, self._server_states[current_thread_info])

        self._start_ready_servers()


    def _server_initialize(self, thread_info: ThreadInfoData, server_state: ServerStateData) -> Result[None]:
        server_state.thread.start()
        future = asyncio.run_coroutine_threadsafe(server_state.server.initialize(), server_state.event_loop)
        future.add_done_callback(lambda future, thread_info=thread_info: self._server_initialization_callback(future, thread_info))
        return Success(None)


    def _server_run(self, server_state: ServerStateData) -> Result[None]:
        async def run(server_state: ServerStateData) -> Result[None]:
            return await server_state.server.run()

        server_state.future = asyncio.run_coroutine_threadsafe(
            run(server_state),
            server_state.event_loop
        )

        return Success(None)


    def _new_thread_info_generator(self) -> Generator[ThreadInfoData]:
        while True:
            used_thread_ids: List[int] = [thread_info.id for thread_info in self._server_states.keys()]

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


    async def _shutdown_server(self, thread_info: ThreadInfoData, server_state: ServerStateData, cleanup: bool = False) -> Result[None]:
        if server_state.initialized or server_state.started:
            await server_state.server.shutdown()
            server_state.initialized = False
            server_state.started = False

        for process_info in server_state.processes:
            if process_info.process.returncode is None:
                logger.info("Sending interrupt to sub-process PID %s, running on server worker thread %s", process_info.process.pid, thread_info.name)
                process_info.process.send_signal(signal.SIGINT)

        if not cleanup:
            return Success(None)

        if server_state.future:
            try:
                logger.info("Awaiting server future for thread %s to complete", thread_info.name)
                await asyncio.wait_for(asyncio.wrap_future(server_state.future), timeout=30.0)
            except asyncio.TimeoutError:
                logger.warning("Background server on thread ID %s timed out during exit phase.", thread_info.id)
            except Exception as exception:
                logger.error("Error during background server cleanup: %s", exception)

        logger.info("Joining thread %s", thread_info.name)
        server_state.event_loop.call_soon_threadsafe(server_state.event_loop.stop)
        server_state.thread.join(timeout=30.0)

        return Success(None)


    def _new_server_state(self, name: str, server: ServerInterface, event_loop: asyncio.AbstractEventLoop) -> ServerStateData:
        return ServerStateData(
            server=server,
            initialized=False,
            future=None,
            event_loop=event_loop,
            processes=[],
            thread=Thread(
                name=name,
                target=Supervisor._start_worker_event_loop,
                args=(event_loop,),
                daemon=True
            )
        )

    async def _enqueue_request(self, request: SupervisorRequestData) ->  Result[None]:
        match request.kind:
            case SupervisorRequestKind.SHUTDOWN:
                started_server_states = {
                    thread_info.id: server_state
                    for (thread_info, server_state) in self._server_states.items()
                    if server_state.started
                }

                if request.thread_id not in self._server_states and request.thread_id not in started_server_states:
                    message = f"Cannot shutdown server because thread with ID {request.thread_id} was not found."
                    logger.info(message)
                    return Failure(Error(SupervisorError.REQUEST_NOT_FULFILLED, details={
                        'message': message
                    }))
                elif request.thread_id in self._server_states and request.thread_id not in started_server_states:
                    message = f"Server with thread ID {request.thread_id} cannot be shutdown because it is not running."
                    logger.info(message)
                    return Failure(Error(SupervisorError.REQUEST_NOT_FULFILLED, details={
                        'message': message
                    }))

            case SupervisorRequestKind.RESTART:
                server_states = {
                    thread_info.id: server_state
                    for (thread_info, server_state) in self._server_states.items()
                }

                if request.thread_id not in server_states:
                    message = f"Cannot restart server because thread with ID {request.thread_id} was not found."
                    logger.warning(message)
                    return Failure(Error(SupervisorError.REQUEST_NOT_FULFILLED, details={
                        'message': message
                    }))

        request_info = RequestInfoData(request)

        if not request_info in self._requests_unique:
            logger.info('Enqueuing request for thread ID %s', request)
            self._requests_enqueued.put_nowait(request_info)
            self._requests_unique.add(request_info)
        else:
            logger.warning('An existing request has already been queued. Ignoring: %s', request)
            return Failure(Error(SupervisorError.REQUEST_IGNORED, details={ 'request': request }))

        return Success(None)


    # -- Threading ------------------------------------------------------------

    @classmethod
    def _start_worker_event_loop(cls, event_loop: asyncio.AbstractEventLoop) -> Result[None]:
        try:
            asyncio.set_event_loop(event_loop)
            event_loop.run_forever()
        finally:
            event_loop.close()

        return Success(None)

    def _server_initialization_callback(self, future: Future[Result[None]], thread_info: ThreadInfoData) -> Result[None]:
        try:
            if not is_successful(result := future.result()):
                logger.error(f"initialization of worker thread {thread_info.name} failed due to error: {result.failure()}")
                return result

            self._server_states[thread_info].initialized = True
        except Exception as exception:
            logger.error(f"initialization of worker thread {thread_info.name} failed due to an exception: {exception}")

        return Success(None)


# -- Internal Types -----------------------------------------------------------

class SupervisorError(StrEnum):
    INITIALIZATION_FAILED = "an error occurred while initializing the supervisor"
    SUBPROCESS_ERROR = "a non-zero exit code occurred when running a subprocess"
    REQUEST_IGNORED = "the provided request has been ignored"
    BAD_REQUEST_DATA = "the provided supervisor request data is invalid"
    REQUEST_NOT_FULFILLED = "the specified request could not be fulfilled"

@dataclass
class ServerStateData:
    server: ServerInterface
    initialized: bool
    future: Future[Result[None]] | None
    event_loop: asyncio.AbstractEventLoop
    processes: List[ProcessInfoData]
    thread: Thread
    started: bool = False


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
