from __future__ import annotations

import asyncio
import logging
from typing import TYPE_CHECKING, Any

from returns.pipeline import is_successful
from returns.result import Success

from armaden.framework.protocols.task_runtime import TaskRuntimeInterface
from armaden.framework.runtime.task import Task
from armaden.framework.utils.types import Result

if TYPE_CHECKING:
    from armaden.framework.queue.driver import QueueDriver
    from armaden.framework.queue.job import Job

logger = logging.getLogger(__name__)


class QueueWorker(Task):
    """Supervisor-managed Task that polls a queue driver and processes jobs
    with retry/backoff/failed-job handling."""

    long_running = True

    def __init__(
        self,
        connection_name: str,
        driver: 'QueueDriver',
        config: dict,
        name: str | None = None,
    ) -> None:
        super().__init__(name=name or f'queue_worker_{connection_name}')
        self._connection_name = connection_name
        self._driver = driver

        worker_config = (config or {}).get('worker', {}) or {}
        self._num_workers: int = int(worker_config.get('num_workers', 4))
        self._sleep: int = int(worker_config.get('sleep', 3))
        self._timeout: int = int(worker_config.get('timeout', 60))
        self._tries: int = int(worker_config.get('tries', 3))
        self._backoff: int = int(worker_config.get('backoff', 2))
        self._max_exceptions: int = int(worker_config.get('max_exceptions', 3))

        queues_config = (config or {}).get('queues', {}) or {}
        self._queues: list[str] = sorted(
            queues_config.keys(),
            key=lambda q: queues_config[q].get('priority', 0),
            reverse=True,
        ) or ['default']

        self._running = False
        self._worker_tasks: list[asyncio.Task] = []
        self._inflight: set[asyncio.Task] = set()
        self._ready_signaled = False

    async def run(self, runtime: TaskRuntimeInterface) -> Result[None]:
        self._running = True
        self._worker_tasks = [
            asyncio.create_task(self._poll_loop(worker_id))
            for worker_id in range(self._num_workers)
        ]
        await self._signal_ready(runtime)
        try:
            await asyncio.gather(*self._worker_tasks, return_exceptions=True)
        except asyncio.CancelledError:
            pass
        return Success(None)

    async def shutdown(self, runtime: TaskRuntimeInterface) -> Result[None]:
        self._running = False

        for task in self._worker_tasks:
            if not task.done():
                task.cancel()
        if self._worker_tasks:
            await asyncio.gather(*self._worker_tasks, return_exceptions=True)

        if self._inflight:
            logger.info(
                "Queue worker '%s' draining %d inflight job(s) (timeout=%ss)",
                self.name, len(self._inflight), self._timeout,
            )
            try:
                await asyncio.wait_for(
                    asyncio.gather(*self._inflight, return_exceptions=True),
                    timeout=float(self._timeout),
                )
            except asyncio.TimeoutError:
                logger.warning(
                    "Queue worker '%s' drain timed out after %ss; cancelling %d job(s)",
                    self.name, self._timeout, len(self._inflight),
                )
                for task in self._inflight:
                    if not task.done():
                        task.cancel()
                if self._inflight:
                    await asyncio.gather(*self._inflight, return_exceptions=True)

        return Success(None)

    async def _signal_ready(self, runtime: TaskRuntimeInterface) -> None:
        if self._ready_signaled:
            return
        self._ready_signaled = True
        try:
            await runtime.signal_ready()
        except Exception:
            logger.exception(
                "Queue worker '%s' failed to signal ready", self.name,
            )

    async def _poll_loop(self, worker_id: int) -> None:
        logger.debug("Queue worker %s[%d] started for connection '%s'",
                     self.name, worker_id, self._connection_name)
        while self._running:
            popped = False
            try:
                for queue in self._queues:
                    pop_result = await asyncio.to_thread(self._driver.pop, queue)
                    if not is_successful(pop_result):
                        logger.warning(
                            "Queue worker %s[%d] pop failed on queue '%s': %s",
                            self.name, worker_id, queue, pop_result.failure(),
                        )
                        continue
                    job = pop_result.unwrap()
                    if job is None:
                        continue
                    job_id = getattr(job, '_job_id', '') or ''
                    task = asyncio.create_task(self._process_job(job, job_id, queue))
                    self._inflight.add(task)
                    task.add_done_callback(self._inflight.discard)
                    popped = True
                    break
            except asyncio.CancelledError:
                break

            if not popped and self._running:
                try:
                    await asyncio.sleep(self._sleep)
                except asyncio.CancelledError:
                    break

    async def _process_job(self, job: 'Job', job_id: str, queue: str) -> None:
        job_name = type(job).__name__
        try:
            job.before()
        except Exception:
            logger.exception("Job %s before() hook raised an exception", job_name)

        attempts = getattr(job, '_attempts', 1) or 1
        max_attempts = getattr(job, '__tries__', None) or self._tries
        timeout = getattr(job, '__timeout__', None) or self._timeout
        base_backoff = getattr(job, '__backoff__', None) or self._backoff

        success = False
        exception: Exception | None = None
        try:
            await asyncio.wait_for(asyncio.to_thread(job.handle), timeout=timeout)
            success = True
        except asyncio.CancelledError:
            await self._release_on_cancel(job_id, job_name, queue)
            raise
        except asyncio.TimeoutError:
            exception = TimeoutError(f"Job {job_id} timed out after {timeout}s")
            logger.error("Job %s (%s) timed out after %ss", job_id, job_name, timeout)
        except Exception as exc:
            exception = exc
            logger.warning(
                "Job %s (%s) raised on attempt %d/%d: %s: %s",
                job_id, job_name, attempts, max_attempts,
                type(exc).__name__, exc,
            )

        if success:
            try:
                job.after()
            except Exception:
                logger.exception("Job %s after() hook raised an exception", job_name)
            await self._safe_driver_call(
                'delete', self._driver.delete, job_id, queue,
                job_name=job_name,
            )
            return

        if exception is None:
            exception = RuntimeError("Job failed without a captured exception")

        if attempts < max_attempts:
            backoff_seconds = base_backoff ** attempts
            logger.warning(
                "Job %s (%s) retrying in %ss (attempt %d/%d)",
                job_id, job_name, backoff_seconds, attempts, max_attempts,
            )
            release_result = await self._safe_driver_call(
                'release', self._driver.release, job_id, backoff_seconds, queue,
                job_name=job_name, level='error',
            )
            if release_result is not None and not is_successful(release_result):
                logger.error(
                    "Job %s (%s) release for retry failed: %s",
                    job_id, job_name, release_result.failure(),
                )
            return

        logger.error(
            "Job %s (%s) exhausted retries (attempt %d/%d); marking failed",
            job_id, job_name, attempts, max_attempts,
        )
        fail_result = await self._safe_driver_call(
            'fail', self._driver.fail, job_id, job, exception, queue,
            job_name=job_name, level='error',
        )
        if fail_result is not None and not is_successful(fail_result):
            logger.error(
                "Job %s (%s) fail() to driver failed: %s",
                job_id, job_name, fail_result.failure(),
            )

    async def _release_on_cancel(self, job_id: str, job_name: str, queue: str) -> None:
        if not job_id:
            return
        logger.info(
            "Job %s (%s) cancelled during shutdown; releasing back to queue '%s'",
            job_id, job_name, queue,
        )
        await self._safe_driver_call(
            'release', self._driver.release, job_id, 0, queue,
            job_name=job_name, force=True,
        )

    async def _safe_driver_call(self, op: str, fn, *args, job_name: str = '',
                                level: str = 'warning', force: bool = False) -> Any:
        try:
            return await asyncio.to_thread(fn, *args)
        except RuntimeError as exc:
            if 'cannot schedule new futures' in str(exc):
                logger.debug(
                    "Executor shutting down; could not %s job %s (%s)",
                    op, job_name, exc,
                )
            else:
                getattr(logger, level)(
                    "RuntimeError during %s for job %s: %s", op, job_name, exc,
                )
            return None
        except Exception:
            logger.exception(
                "Unexpected error during %s for job %s", op, job_name,
            )
            return None
