from __future__ import annotations

import shlex
from collections.abc import Sequence
from typing import cast, override

from armaden.framework.runtime.schedule.dto.scheduled_event_definition_data import (
    ScheduledEventDefinitionData,
)
from armaden.framework.protocols.queue_resolver_protocol import QueueResolverProtocol
from armaden.framework.protocols.schedule_dispatcher_protocol import ScheduleDispatcherProtocol
from armaden.framework.protocols.supervisor_protocol import SupervisorProtocol
from armaden.framework.runtime.schedule.enums import ScheduledEventKind
from armaden.framework.runtime.schedule.scheduled_queue_job import ScheduledQueueJob
from armaden.framework.runtime.supervisor.task.dto.task_policy_data import TaskPolicyData
from armaden.framework.runtime.supervisor.task.process_task import ProcessTask
from armaden.framework.types.result import Result
from armaden.framework.types.schedule import ScheduleCallback


class ScheduleDispatcher(ScheduleDispatcherProtocol[ScheduledEventDefinitionData]):
    def __init__(
        self,
        queue_resolver: QueueResolverProtocol,
        supervisor: SupervisorProtocol[object],
    ) -> None:
        self._queue_resolver: QueueResolverProtocol = queue_resolver
        self._supervisor: SupervisorProtocol[object] = supervisor


    @override
    async def dispatch(
        self,
        definition: ScheduledEventDefinitionData,
    ) -> Result[object]:
        match definition.kind:
            case ScheduledEventKind.CALL:
                return await self._dispatch_callback(definition)
            case ScheduledEventKind.EXEC:
                return await self._dispatch_process(definition)
            case ScheduledEventKind.JOB:
                return await self._dispatch_job(definition)


    async def _dispatch_callback(
        self,
        definition: ScheduledEventDefinitionData,
    ) -> Result[object]:
        callback = cast(ScheduleCallback, definition.target)
        return await self._supervisor.dispatch_scheduled(
            definition.name or 'scheduled-call',
            callback,
            definition.execution,
        )


    async def _dispatch_job(
        self,
        definition: ScheduledEventDefinitionData,
    ) -> Result[object]:
        target = definition.target
        queue = definition.execution.queue
        if queue is None:
            queue_name = getattr(target, 'queue', None) or 'default'
            connection = getattr(target, 'connection', None)
        else:
            queue_name = queue.name or getattr(target, 'queue', None) or 'default'
            connection = queue.connection or getattr(target, 'connection', None)

        driver = self._queue_resolver.connection(connection)
        job_priority = queue.priority if queue is not None else getattr(target, 'priority', 0)
        priority = job_priority if isinstance(job_priority, int) else 0
        queued_job = ScheduledQueueJob(
            target,
            str(queue_name),
            connection,
            priority,
        )

        def enqueue() -> Result[object]:
            result = driver.push(queued_job, str(queue_name))
            return cast(Result[object], result)

        return await self._supervisor.dispatch_scheduled(
            definition.name or (
                target.__name__ if isinstance(target, type) else type(target).__name__
            ),
            enqueue,
            definition.execution,
        )


    async def _dispatch_process(
        self,
        definition: ScheduledEventDefinitionData,
    ) -> Result[object]:
        argv = self._command(definition.target)
        queue = definition.execution.queue
        priority = queue.priority if queue is not None else 0
        task = ProcessTask(
            name=definition.name or 'scheduled-process',
            argv=argv,
            policy=TaskPolicyData(priority=priority),
        )
        return await self._supervisor.dispatch_task(
            task,
            definition.execution.run_in_background,
        )


    def _command(self, target: object) -> list[str]:
        if isinstance(target, str):
            return shlex.split(target)
        if isinstance(target, Sequence) and not isinstance(target, (str, bytes)):
            values = list(target)
            if all(isinstance(value, str) for value in values):
                return cast(list[str], values)
        raise TypeError('Scheduled exec targets must be a command string or sequence of strings')
