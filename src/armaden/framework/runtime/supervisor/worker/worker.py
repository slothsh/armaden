from __future__ import annotations

import asyncio
from abc import ABC
from threading import Thread
from typing import override

from armaden.framework.protocols.worker_protocol import WorkerProtocol


class Worker(WorkerProtocol, ABC):
    def __init__(self, name: str) -> None:
        self.busy: bool = False
        self.loop: asyncio.AbstractEventLoop = asyncio.new_event_loop()
        self.name: str = name
        self.thread: Thread = Thread(target=self._run_loop, name=name, daemon=True)
        self.thread.start()


    def _run_loop(self) -> None:
        asyncio.set_event_loop(self.loop)
        self.loop.run_forever()


    @override
    def shutdown(self) -> None:
        try:
            _ = self.loop.call_soon_threadsafe(self.loop.stop)
        except RuntimeError:
            pass
        self.thread.join(timeout=5.0)


class SharedWorker(Worker):
    pass


class ExclusiveWorker(Worker):
    pass
