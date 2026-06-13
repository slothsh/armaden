import asyncio
from enum import StrEnum
import logging
import signal
import sys
from typing import List, Self
from threading import Thread
from concurrent.futures import Future, wait

from dataclasses import dataclass
from returns.pipeline import is_successful
from returns.result import Success
from pathlib import Path

from server.lib import Result
from server.lib.interfaces import Server
from server.lib.types import Error

logger = logging.getLogger("server.supervisor")


class Supervisor:
    def __init__(self) -> None:
        self._shutdown_event = asyncio.Event()
        self._main_loop = asyncio.get_event_loop()

        self._server_states: List[ServerStateData] = []
        self._server_futures: List[Future] = []

        self._worker_event_loop = asyncio.new_event_loop()
        self._worker_thread = Thread(
            target=Supervisor._start_worker_event_loop,
            args=(self._worker_event_loop,),
            daemon=True
        )

        self._worker_thread.start()

        self._initialize_logging()
        self._initialize_signal_handlers()


    # -- Builder Methods ------------------------------------------------------
    
    def with_servers(self, servers: List[Server]) -> Self:
        self._server_states = [ServerStateData(server=server, initialized=False) for server in servers]
        return self


    # -- Lifecycle ------------------------------------------------------------

    async def initialize(self) -> Result[None]:
        for server_state in self._server_states:
            if not is_successful(result := await server_state.server.initialize()):
                return result
            server_state.initialized = True

        return Success(None)


    async def run(self) -> Result[None]:
        ready_servers = [server for server in self._server_states if server.initialized]

        for server_state in ready_servers:
            async def run(server_state: ServerStateData) -> Result[None]:
                return await server_state.server.run()

            self._server_futures.append(asyncio.run_coroutine_threadsafe(
                run(server_state),
                self._worker_event_loop
            ))
            server_state.initialized = True

        await self._shutdown_event.wait()
        
        return await self.shutdown()


    async def shutdown(self) -> Result[None]:
        for server_state in self._server_states:
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
                
        self._worker_event_loop.call_soon_threadsafe(self._worker_event_loop.stop)

        self._server_futures.clear()
        
        return Success(None)


    # -- SupervisorLike Protocol Interface-------------------------------------

    def queue_start(self) -> None:
        pass


    def queue_shutdown(self) -> None:
        pass


    def queue_restart(self) -> None:
        pass


    def queue_reload(self, config_path: str | Path) -> None:
        pass


    # -- Logging --------------------------------------------------------------

    def _initialize_logging(self) -> None:
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            stream=sys.stdout,
        )


    # -- Signal Handling ------------------------------------------------------

    def _initialize_signal_handlers(self) -> None:
        for sig in (signal.SIGINT, signal.SIGTERM, signal.SIGQUIT):
            signal.signal(sig, self._handle_os_signal)


    def _handle_os_signal(self, signum: int, frame: Any) -> None:
        logger.info("OS signal caught. Handling signal %s", signal.Signals(signum).name)
        self._main_loop.call_soon_threadsafe(self._shutdown_event.set)


    # -- Threading ------------------------------------------------------------

    @classmethod
    def _start_worker_event_loop(cls, event_loop: asyncio.AbstractEventLoop) -> Result[None]:
        asyncio.set_event_loop(event_loop)
        event_loop.run_forever()
        return Success(None)


# -- Internal Types -----------------------------------------------------------

class SupervisorError(StrEnum):
    INITIALIZATION_FAILED = "an error occurred while initializing the supervisor"


@dataclass
class ServerStateData:
    server: Server
    initialized: bool
