import asyncio
from threading import Thread
from typing import Protocol


class WorkerProtocol(Protocol):
    busy: bool
    loop: asyncio.AbstractEventLoop
    name: str
    thread: Thread

    def shutdown(self) -> None: ...
