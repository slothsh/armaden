from __future__ import annotations

import inspect
from collections.abc import Awaitable, Callable
from typing import cast, override

from armaden.framework.protocols.container_aware_queue_job_protocol import (
    ContainerAwareQueueJobProtocol,
)
from armaden.framework.protocols.container_protocol import ContainerProtocol


class ScheduledQueueJob(ContainerAwareQueueJobProtocol):
    def __init__(
        self,
        target: object,
        queue: str,
        connection: str | None,
        priority: int,
    ) -> None:
        self.connection: str | None = connection
        self.priority: int = priority
        self.queue: str = queue
        self._container: ContainerProtocol | None = None
        self._target: object = target


    @override
    def __getstate__(self) -> dict[str, object]:
        state = dict(self.__dict__)
        state['_container'] = None
        return state


    @override
    def after(self) -> None:
        pass


    @override
    async def handle(self) -> None:
        target = self._resolve_target()
        handle = getattr(target, 'handle', None)
        callback = cast(Callable[[], object], handle) if callable(handle) else cast(Callable[[], object], target)
        result = callback()
        if inspect.isawaitable(result):
            _ = await cast(Awaitable[object], result)


    @override
    def before(self) -> None:
        pass


    @override
    def bind_container(self, container: ContainerProtocol) -> None:
        self._container = container


    @override
    def failed(self, exception: Exception) -> None:
        _ = exception


    def _resolve_target(self) -> object:
        if isinstance(self._target, type):
            if self._container is None:
                raise RuntimeError('Scheduled queue job requires a container to resolve its target')
            return self._container.make(self._target)
        return self._target
