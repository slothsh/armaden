from armaden.framework.runtime.supervisor.worker.worker import SharedWorker, ExclusiveWorker
from armaden.framework.support.string import String
import asyncio


class WorkerPool:
    def __init__(self, pool_size: int, max_exclusive_threads: int) -> None:
        self._pool_size: int = pool_size
        self._max_exclusive_threads: int = max_exclusive_threads
        self._shared: list[SharedWorker] = [
            SharedWorker(f'worker-shared-{i:02d}') for i in range(pool_size)
        ]

        self._free: asyncio.Queue[SharedWorker] = asyncio.Queue()

        for worker in self._shared:
            self._free.put_nowait(worker)

        self._exclusive: dict[str, ExclusiveWorker] = {}

        self._lock: asyncio.Lock = asyncio.Lock()


    async def acquire_shared(self) -> SharedWorker:
        return await self._free.get()


    async def release_shared(self, worker: SharedWorker) -> None:
        worker.busy = False
        await self._free.put(worker)


    async def acquire_exclusive(self, task_name: str) -> ExclusiveWorker:
        async with self._lock:
            if len(self._exclusive) >= self._max_exclusive_threads:
                raise RuntimeError(
                    f'Exclusive thread capacity reached ({self._max_exclusive_threads}); cannot start task \"{task_name}\"'
                )
            worker = ExclusiveWorker(f'worker-{String.toKebabCase(task_name)}')
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
