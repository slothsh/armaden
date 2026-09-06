from __future__ import annotations

import asyncio
import logging
from collections.abc import Mapping
from typing import cast, override

from returns.pipeline import is_successful
from returns.result import Success

from armaden.framework.protocols.container_aware_queue_job_protocol import (
    ContainerAwareQueueJobProtocol,
)
from armaden.framework.protocols.container_protocol import ContainerProtocol
from armaden.framework.protocols.queue_driver_protocol import QueueDriverProtocol
from armaden.framework.protocols.queue_job_protocol import QueueJobProtocol
from armaden.framework.protocols.queue_worker_protocol import QueueWorkerProtocol
from armaden.framework.protocols.task_runtime_protocol import TaskRuntimeProtocol
from armaden.framework.types.result import Result
from armaden.framework.runtime.queue.job_invoker import invoke_job_handle

logger = logging.getLogger(__name__)


class QueueWorker(QueueWorkerProtocol):
    def __init__(
        self,
        driver: QueueDriverProtocol,
        config: Mapping[str, object],
        container: ContainerProtocol | None = None,
    ) -> None:
        worker_config_object = config.get('worker', {})
        worker_config: Mapping[str, object] = (
            cast(Mapping[str, object], worker_config_object)
            if isinstance(worker_config_object, Mapping)
            else {}
        )
        self._backoff: int = self._integer(worker_config.get('backoff'), 2)
        self._num_workers: int = self._integer(worker_config.get('num_workers'), 1)
        self._running: bool = False
        self._sleep: float = float(self._integer(worker_config.get('sleep'), 3))
        self._timeout: float = float(self._integer(worker_config.get('timeout'), 60))
        self._tries: int = self._integer(worker_config.get('tries'), 3)
        self._driver: QueueDriverProtocol = driver
        self._container: ContainerProtocol | None = container
        self._inflight: set[asyncio.Task[None]] = set()
        self._worker_tasks: list[asyncio.Task[None]] = []
        queues_object = config.get('queues', {})
        queues = (
            cast(Mapping[str, object], queues_object)
            if isinstance(queues_object, Mapping)
            else cast(Mapping[str, object], {})
        )
        self._queues: list[str] = list(queues) or ['default']


    @override
    async def run(self, runtime: TaskRuntimeProtocol) -> Result[None]:
        self._running = True
        self._worker_tasks = [
            asyncio.create_task(self._poll_loop())
            for _ in range(max(1, self._num_workers))
        ]
        _ = await runtime.signal_ready()
        try:
            _ = await asyncio.gather(*self._worker_tasks, return_exceptions=True)
        except asyncio.CancelledError:
            pass
        return Success(None)


    @override
    async def shutdown(self, runtime: TaskRuntimeProtocol) -> Result[None]:
        _ = runtime
        self._running = False
        for task in self._worker_tasks:
            _ = task.cancel()
        if self._worker_tasks:
            _ = await asyncio.gather(*self._worker_tasks, return_exceptions=True)
        if self._inflight:
            _ = await asyncio.gather(*self._inflight, return_exceptions=True)
        return Success(None)


    def _prepare_job(self, job: QueueJobProtocol) -> None:
        if self._container is None:
            return
        if isinstance(job, ContainerAwareQueueJobProtocol):
            job.bind_container(self._container)


    async def _poll_loop(self) -> None:
        while self._running:
            found_job = False
            for queue in self._queues:
                result = await asyncio.to_thread(self._driver.pop, queue)
                if not is_successful(result):
                    logger.warning('Queue pop failed for %s: %s', queue, result.failure())
                    continue
                job = result.unwrap()
                if job is None:
                    continue
                task = asyncio.create_task(self._process_job(job, queue))
                self._inflight.add(task)
                task.add_done_callback(self._inflight.discard)
                found_job = True
                break
            if not found_job and self._running:
                try:
                    await asyncio.sleep(self._sleep)
                except asyncio.CancelledError:
                    return


    async def _process_job(self, job: QueueJobProtocol, queue: str) -> None:
        job_id_object = getattr(job, '_queue_job_id', '')
        job_id = job_id_object if isinstance(job_id_object, str) else ''
        try:
            self._prepare_job(job)
            job.before()
            _ = await invoke_job_handle(job, self._timeout)
            job.after()
            if job_id:
                _ = await asyncio.to_thread(self._driver.delete, job_id, queue)
        except asyncio.CancelledError:
            if job_id:
                _ = await asyncio.to_thread(self._driver.release, job_id, 0, queue)
            raise
        except Exception as exception:
            attempts_object = getattr(job, '_queue_attempts', 1)
            attempts = attempts_object if isinstance(attempts_object, int) else 1
            if job_id and attempts < self._tries:
                _ = await asyncio.to_thread(
                    self._driver.release,
                    job_id,
                    self._backoff ** attempts,
                    queue,
                )
            elif job_id:
                _ = await asyncio.to_thread(
                    self._driver.fail,
                    job_id,
                    job,
                    exception,
                    queue,
                )
            else:
                job.failed(exception)


    @staticmethod
    def _integer(value: object, default: int) -> int:
        return value if isinstance(value, int) else default
