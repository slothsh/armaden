from __future__ import annotations

import asyncio
import logging
from enum import Enum, StrEnum
from typing import override

from returns.pipeline import is_successful
from returns.result import Failure

from armaden.framework.error.error import Error
from armaden.framework.protocols.policy_engine_protocol import PolicyEngineProtocol
from armaden.framework.protocols.task_injector_protocol import TaskInjectorProtocol
from armaden.framework.protocols.task_protocol import TaskProtocol
from armaden.framework.protocols.task_runtime_protocol import TaskRuntimeProtocol
from armaden.framework.runtime.supervisor.task.dto.task_graph_data import TaskGraphData
from armaden.framework.runtime.supervisor.task.enums.task_restart_policy import TaskRestartPolicy
from armaden.framework.types.result import Result

logger = logging.getLogger(__name__)


class PolicyEngineError(StrEnum):
    MAX_RETRIES_EXCEEDED = 'maximum task retries exceeded'
    TIMEOUT = 'task execution timed out'


class PolicyEngine(PolicyEngineProtocol[TaskGraphData]):
    async def _wait_before_retry(
        self,
        task: TaskProtocol[Enum],
        attempt: int,
        attempts: int,
        delay: float,
        backoff: float,
        reason: str,
    ) -> None:
        wait = delay * (backoff ** attempt)
        logger.warning(
            "Task '%s' %s on attempt %d/%d; retrying in %.2fs",
            task.name,
            reason,
            attempt + 1,
            attempts,
            wait,
        )
        await asyncio.sleep(wait)


    @override
    async def execute(
        self,
        task: TaskProtocol[Enum],
        runtime: TaskRuntimeProtocol,
        injector: TaskInjectorProtocol[TaskGraphData],
        graph: TaskGraphData,
    ) -> Result[object]:
        resolved = await injector.resolve(task, task.run, graph, runtime)
        _ = resolved.pop('runtime', None)

        attempts = max(task.policy.retries, 0) + 1
        delay = max(task.policy.retry_delay, 0.0)
        backoff = max(task.policy.retry_backoff, 0.0)
        last_result: Result[object] = Failure(
            Error(PolicyEngineError.MAX_RETRIES_EXCEEDED, details={'task': task.name})
        )

        for attempt in range(attempts):
            try:
                invocation = task.run(runtime, **resolved)
                if task.policy.timeout is None:
                    result = await invocation
                else:
                    result = await asyncio.wait_for(invocation, task.policy.timeout)
            except asyncio.TimeoutError:
                last_result = Failure(Error(PolicyEngineError.TIMEOUT, details={'task': task.name}))
                if attempt >= attempts - 1:
                    return last_result
                await self._wait_before_retry(
                    task,
                    attempt,
                    attempts,
                    delay,
                    backoff,
                    'timed out',
                )
                continue
            except Exception as exception:
                last_result = Failure(Error(
                    PolicyEngineError.MAX_RETRIES_EXCEEDED,
                    details={'task': task.name, 'error': str(exception)},
                ))
                if attempt >= attempts - 1:
                    return last_result
                await self._wait_before_retry(
                    task,
                    attempt,
                    attempts,
                    delay,
                    backoff,
                    str(exception),
                )
                continue

            last_result = result
            if is_successful(result) or attempt >= attempts - 1:
                return result
            await self._wait_before_retry(
                task,
                attempt,
                attempts,
                delay,
                backoff,
                'failed',
            )

        return last_result


    @override
    def should_restart(
        self,
        task: TaskProtocol[Enum],
        result: Result[object],
    ) -> bool:
        policy = TaskRestartPolicy(task.policy.restart)
        if policy is TaskRestartPolicy.ALWAYS:
            return True
        if policy is TaskRestartPolicy.ON_FAILURE:
            return not is_successful(result)
        return False
