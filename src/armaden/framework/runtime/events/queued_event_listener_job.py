from __future__ import annotations

import inspect
from typing import cast, override

from armaden.framework.protocols.container_aware_queue_job_protocol import (
    ContainerAwareQueueJobProtocol,
)
from armaden.framework.protocols.container_protocol import ContainerProtocol
from armaden.framework.runtime.events.async_runtime import run_coroutine_sync
from armaden.framework.runtime.events.exceptions.event_dispatcher_error import (
    EventDispatcherError,
)


class QueuedEventListenerJob(ContainerAwareQueueJobProtocol):
    def __init__(
        self,
        listener: object,
        method: str,
        event: object,
    ) -> None:
        self._container: ContainerProtocol | None = None
        self._event: object = event
        self._listener: object = listener
        self._method: str = method


    @override
    def after(self) -> None:
        pass


    @override
    def before(self) -> None:
        pass


    @override
    def bind_container(self, container: ContainerProtocol) -> None:
        self._container = container


    @override
    def failed(self, exception: Exception) -> None:
        _ = exception


    @override
    def handle(self) -> None:
        if self._container is None:
            raise RuntimeError(EventDispatcherError.ASYNC_CONTEXT_REQUIRED.value)
        listener = self._resolve_listener()
        method = getattr(listener, self._method)
        response = method(self._event)
        if inspect.isawaitable(response):
            self._run_awaitable(response)


    @override
    def __getstate__(self) -> dict[str, object]:
        state = dict(self.__dict__)
        state['_container'] = None
        return state


    def __setstate__(self, state: dict[str, object]) -> None:
        self.__dict__.update(state)
        self._container = None


    def _resolve_listener(self) -> object:
        container = self._container
        container = cast(ContainerProtocol, container)
        if isinstance(self._listener, type):
            return container.make(self._listener)
        return self._listener


    def _run_awaitable(self, response: object) -> None:
        from collections.abc import Coroutine

        run_coroutine_sync(cast(Coroutine[object, object, object], response))