import asyncio
from enum import StrEnum
import logging
import signal
from typing import Any, Dict, List, Self
from threading import Thread
from concurrent.futures import Future

from dataclasses import dataclass
from returns.pipeline import is_successful
from returns.result import Failure, Success
from pathlib import Path

from server.lib import Result
from server.lib.interfaces import Server
from server.lib.types import Error

logger = logging.getLogger("server.supervisor")


class Supervisor:
    def __init__(self) -> None:
        self._running = False
        self._shutdown_event = asyncio.Event()
        self._main_loop = asyncio.get_event_loop()

        self._server_states: Dict[str, ServerStateData] = {}
        self._server_futures: List[Future] = []

        self._initialize_signal_handlers()


    # -- Builder Methods ------------------------------------------------------
    
    def with_servers(self, servers: List[Server]) -> Self:
        for i, server in enumerate(servers):
            thread_name = f"WorkerThread-{i + 1:02}"
            worker_event_loop = asyncio.new_event_loop()

            self._server_states[thread_name] = ServerStateData(
                server=server,
                initialized=False,
                event_loop=worker_event_loop,
                thread=Thread(
                    name=thread_name,
                    target=Supervisor._start_worker_event_loop,
                    args=(worker_event_loop,),
                    daemon=True
                )
            )

        return self


    # -- Lifecycle ------------------------------------------------------------

    async def initialize(self) -> Result[None]:
        for thread_name, server_state in self._server_states.items():
            server_state.thread.start()
            future = asyncio.run_coroutine_threadsafe(server_state.server.initialize(), server_state.event_loop)
            future.add_done_callback(lambda future, name=thread_name: self._server_initialization_callback(future, name))

        return Success(None)


    async def run(self) -> Result[None]:
        ready_servers = [server for server in self._server_states.values() if server.initialized]

        running = False
        for server_state in ready_servers:
            if not is_successful(result := self._server_run(server_state)):
                logger.error("Failed to run server on worker thread %s: %s", server_state.thread.name, result.failure())
                continue
            running = True

        if not running:
            logger.warning("No servers are running, waiting until shutdown signal is received")

        self._running = running
        await self._shutdown_event.wait()
        
        return await self.shutdown()


    async def shutdown(self) -> Result[None]:
        for server_state in self._server_states.values():
            if server_state.initialized:
                await server_state.server.shutdown()
                server_state.initialized = False

        if self._server_futures:
            logger.warning("Shutting down supervisor servers")
            asyncio_tasks = [asyncio.wrap_future(future) for future in self._server_futures]
            
            try:
                await asyncio.wait_for(asyncio.gather(*asyncio_tasks), timeout=10.0)
            except asyncio.TimeoutError:
                logger.warning("Background servers timed out during exit phase.")
            except Exception as e:
                logger.error(f"Error during background server cleanup: {e}")
                
        join_threads = []
        for server_state in self._server_states.values():
            server_state.event_loop.call_soon_threadsafe(server_state.event_loop.stop)
            join_threads.append(server_state.thread)

        for thread in join_threads:
            thread.join(timeout=10.0)

        self._server_futures.clear()
        
        self._running = False

        return Success(None)


    # -- SupervisorLike Protocol Interface-------------------------------------

    async def queue_start(self) -> None:
        pass


    async def queue_shutdown(self) -> None:
        pass


    async def queue_restart(self) -> None:
        pass


    async def queue_reload(self, config_path: str | Path) -> None:
        pass


    async def dispatch_subprocess(self, argv: List[str]) -> Result[str]:
        logger.info('Executing command in subprocess: %s', ' '.join(argv))

        process = await asyncio.create_subprocess_exec(
            argv[0], *argv[1:],
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        stdout, stderr = await process.communicate()

        if process.returncode == 0:
            return Success(stdout.decode().strip())
        else:
            return Failure(Error(SupervisorError.SUBPROCESS_ERROR, details={
                'stderr': stderr.decode().strip()
            }))


    # -- Signal Handling ------------------------------------------------------

    def _initialize_signal_handlers(self) -> None:
        for sig in (signal.SIGINT, signal.SIGTERM, signal.SIGQUIT):
            signal.signal(sig, self._handle_os_signal)


    def _handle_os_signal(self, signum: int, frame: Any) -> None:
        logger.info("OS signal caught. Handling signal %s", signal.Signals(signum).name)
        self._main_loop.call_soon_threadsafe(self._shutdown_event.set)


    # -- Helpers --------------------------------------------------------------

    # def _pre_run_checks(self) -> Result[None]:
    #     errors: Dict[str, Error] = {}
    #     for thread_name, future in futures.items():
    #         if not is_successful(result := await asyncio.wrap_future(future)):
    #             errors[thread_name] = result.failure()
    #             continue
    #
    #         self._server_states[thread_name].initialized = True
    #
    #     if errors:
    #         return Failure(Error(SupervisorError.INITIALIZATION_FAILED, details={
    #             'errors': errors
    #         }))
    #
    #     return Success(None)


    def _server_run(self, server_state: ServerStateData) -> Result[None]:
        async def run(server_state: ServerStateData) -> Result[None]:
            return await server_state.server.run()

        self._server_futures.append(asyncio.run_coroutine_threadsafe(
            run(server_state),
            server_state.event_loop
        ))

        return Success(None)


    # -- Threading ------------------------------------------------------------

    @classmethod
    def _start_worker_event_loop(cls, event_loop: asyncio.AbstractEventLoop) -> Result[None]:
        asyncio.set_event_loop(event_loop)
        event_loop.run_forever()
        return Success(None)


    def _server_initialization_callback(self, future: Future[Result[None]], thread_name: str) -> Result[None]:
        try:
            if not is_successful(result := future.result()):
                logger.error(f"initialization of worker thread {thread_name} failed due to error: {result.failure()}")
                return result

            self._server_states[thread_name].initialized = True

            if self._running:
                self._server_run(self._server_states[thread_name])
        except Exception as exception:
            logger.error(f"initialization of worker thread {thread_name} failed due to an exception: {exception}")

        return Success(None)


    # -- steamcmd Flags -------------------------------------------------------

class SupervisorError(StrEnum):
    INITIALIZATION_FAILED = "an error occurred while initializing the supervisor"
    SUBPROCESS_ERROR = "a non-zero exit code occurred when running a subprocess"


@dataclass
class ServerStateData:
    server: Server
    initialized: bool
    event_loop: asyncio.AbstractEventLoop
    thread: Thread


# import asyncio
#
# async def pump_stream(stream, prefix):
#     while True:
#         line = await stream.readline()
#         if not line:
#             break
#
#         print(f"[{prefix}] {line.decode().rstrip()}")
#
# async def run_process():
#     proc = await asyncio.create_subprocess_exec(
#         "python",
#         "-u",  # unbuffered output
#         "long_running_script.py",
#         stdout=asyncio.subprocess.PIPE,
#         stderr=asyncio.subprocess.PIPE,
#     )
#
#     stdout_task = asyncio.create_task(
#         pump_stream(proc.stdout, "stdout")
#     )
#     stderr_task = asyncio.create_task(
#         pump_stream(proc.stderr, "stderr")
#     )
#
#     returncode = await proc.wait()
#
#     await stdout_task
#     await stderr_task
#
#     print(f"Process exited with {returncode}")
