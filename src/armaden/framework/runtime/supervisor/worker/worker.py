from threading import Thread
import asyncio

class Worker:
    def __init__(self, name: str) -> None:
        self.name: str = name
        self.loop: asyncio.AbstractEventLoop = asyncio.new_event_loop()
        self.thread: Thread = Thread(target=self._run_loop, name=name, daemon=True)
        self.busy: bool = False
        self.thread.start()


    def shutdown(self) -> None:
        try:
            _ = self.loop.call_soon_threadsafe(self.loop.stop)
        except RuntimeError:
            pass
        self.thread.join(timeout=5.0)


    def _run_loop(self) -> None:
        asyncio.set_event_loop(self.loop)
        self.loop.run_forever()


class SharedWorker(Worker):
    pass


class ExclusiveWorker(Worker):
    pass
