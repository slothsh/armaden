import asyncio
import logging
from typing import Any

from returns.pipeline import is_successful
from returns.result import Failure, Success

from armaden.framework.errors import Error
from armaden.framework.runtime.errors import TaskError
from armaden.framework.runtime.task import Task, TaskPolicy, RestartPolicy
from armaden.framework.runtime.task_injector import TaskInjector

logger = logging.getLogger(__name__)


class PolicyEngine:
    async def execute(
        self,
        task: Task,
        runtime,
        injector: TaskInjector,
        graph,
    ) -> Any:
        policy = task.policy if isinstance(task.policy, TaskPolicy) else TaskPolicy()

        resolved = await injector.resolve(task, task.run, graph, runtime)

        attempts = max(int(policy.retries), 0) + 1
        delay = float(policy.retry_delay) if policy.retry_delay is not None else 1.0
        backoff = float(policy.retry_backoff) if policy.retry_backoff is not None else 2.0

        last_result = None
        for attempt in range(attempts):
            try:
                if policy.timeout is not None:
                    result = await asyncio.wait_for(task.run(**resolved), timeout=float(policy.timeout))
                else:
                    result = await task.run(**resolved)
            except asyncio.TimeoutError:
                last_result = Failure(Error(TaskError.TIMEOUT, details={'task': task.name}))
                if attempt < attempts - 1:
                    wait = delay * (backoff ** attempt)
                    logger.warning("Task '%s' timed out on attempt %d/%d; retrying in %.2fs", task.name, attempt + 1, attempts, wait)
                    await asyncio.sleep(wait)
                    continue
                return last_result
            except Exception as exception:
                last_result = Failure(Error(TaskError.MAX_RETRIES_EXCEEDED, details={
                    'task': task.name,
                    'error': str(exception),
                }))
                if attempt < attempts - 1:
                    wait = delay * (backoff ** attempt)
                    logger.warning("Task '%s' raised on attempt %d/%d: %s; retrying in %.2fs", task.name, attempt + 1, attempts, exception, wait)
                    await asyncio.sleep(wait)
                    continue
                return last_result

            last_result = result
            if is_successful(result):
                return result

            if attempt < attempts - 1:
                wait = delay * (backoff ** attempt)
                logger.warning("Task '%s' failed on attempt %d/%d; retrying in %.2fs", task.name, attempt + 1, attempts, wait)
                await asyncio.sleep(wait)
                continue

        return last_result

    def should_restart(self, task: Task, result) -> bool:
        policy = task.policy if isinstance(task.policy, TaskPolicy) else TaskPolicy()
        match policy.restart:
            case RestartPolicy.NEVER:
                return False
            case RestartPolicy.ALWAYS:
                return True
            case RestartPolicy.ON_FAILURE:
                return not is_successful(result)
        return False
