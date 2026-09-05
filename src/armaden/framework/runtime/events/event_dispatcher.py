from __future__ import annotations

import asyncio
import inspect
import logging
import types
from collections.abc import Callable
from typing import cast, get_args, get_origin, get_type_hints, override
import typing

from returns.result import Failure, Success

from armaden.framework.protocols.container_protocol import ContainerProtocol
from armaden.framework.protocols.event_dispatcher_protocol import (
    EventDispatcherProtocol,
)
from armaden.framework.protocols.event_listener_registry_protocol import (
    EventListenerRegistryProtocol,
)
from armaden.framework.protocols.event_protocol import EventProtocol
from armaden.framework.protocols.event_subscriber_protocol import (
    EventSubscriberProtocol,
)
from armaden.framework.protocols.queue_resolver_protocol import QueueResolverProtocol
from armaden.framework.runtime.error.error import Error
from armaden.framework.runtime.events.dto.deferred_event_state_data import (
    DeferredEventStateData,
)
from armaden.framework.runtime.events.dto.event_listener_registration_data import (
    EventListenerRegistrationData,
)
from armaden.framework.runtime.events.exceptions.event_dispatcher_error import (
    EventDispatcherError,
)
from armaden.framework.runtime.events.exceptions.event_listener_registration_error import (
    EventListenerRegistrationError,
)
from armaden.framework.runtime.events.queueable_event_listener import (
    QueueableEventListener,
)
from armaden.framework.runtime.events.queued_event_listener_job import (
    QueuedEventListenerJob,
)
from armaden.framework.runtime.events.tags import ShouldQueueEventListenerTag
from armaden.framework.types.events import DispatchCallback
from armaden.framework.types.result import Result

logger = logging.getLogger(__name__)


class EventDispatcher(EventDispatcherProtocol):
    def __init__(
        self,
        container: ContainerProtocol,
        registry: EventListenerRegistryProtocol,
        queue_resolver: QueueResolverProtocol | None = None,
    ) -> None:
        self._container: ContainerProtocol = container
        self._deferred: list[DeferredEventStateData] = []
        self._pushed: list[EventProtocol] = []
        self._queue_resolver: QueueResolverProtocol | None = queue_resolver
        self._registry: EventListenerRegistryProtocol = registry


    @override
    async def defer(
        self,
        callback: DispatchCallback,
        events: list[type[EventProtocol]] | None = None,
    ) -> Result[object]:
        event_types = frozenset(events) if events is not None else None
        state = DeferredEventStateData([], event_types)
        self._deferred.append(state)
        try:
            callback_result = callback()
            if inspect.isawaitable(callback_result):
                callback_result = await callback_result
        except Exception as exception:
            _ = self._deferred.pop()
            return Failure(Error(EventDispatcherError.DEFERRED_CALLBACK_FAILED, details={
                'exception': exception,
            }))

        _ = self._deferred.pop()
        if self._deferred:
            self._deferred[-1].events.extend(state.events)
            return Success(callback_result)
        for event in state.events:
            result = await self._dispatch_now(event)
            if isinstance(result, Failure):
                return result.map(lambda _: callback_result)
        return Success(callback_result)


    @override
    async def dispatch(self, event: EventProtocol) -> Result[list[object]]:
        validation = self._validate_event(event)
        if isinstance(validation, Failure):
            return validation
        if self._deferred and self._should_defer(event):
            self._deferred[-1].events.append(event)
            return Success([])
        return await self._dispatch_now(event)


    @override
    def dispatch_sync(self, event: EventProtocol) -> Result[list[object]]:
        if self._running_loop():
            return Failure(Error(
                EventDispatcherError.ASYNC_CONTEXT_REQUIRED,
                details={'event': type(event).__name__},
            ))
        return asyncio.run(self.dispatch(event))


    @override
    async def flush(self, event_type: type[EventProtocol]) -> Result[list[object]]:
        matching = [
            event
            for event in self._pushed
            if isinstance(event, event_type)
        ]
        self._pushed = [
            event
            for event in self._pushed
            if not isinstance(event, event_type)
        ]
        responses: list[object] = []
        for event in matching:
            result = await self._dispatch_now(event)
            if isinstance(result, Failure):
                return result
            responses.extend(result.unwrap())
        return Success(responses)


    @override
    def forget(self, event_type: type[object]) -> None:
        self._registry.forget(event_type)


    @override
    def forget_pushed(self) -> None:
        self._pushed.clear()


    @override
    def has_listeners(self, event_type: type[object]) -> bool:
        return self._registry.has_listeners(event_type)


    @override
    def listen(
        self,
        event_type_or_listener: type[EventProtocol] | Callable[..., object],
        listener: object | None = None,
    ) -> Result[None]:
        if listener is None:
            event_types = self._event_types_from_callable(
                cast(Callable[..., object], event_type_or_listener),
            )
            if not event_types:
                return self._invalid_listener()
            method = '__call__'
            target = event_type_or_listener
        else:
            if not self._is_event_type(event_type_or_listener):
                return self._invalid_listener()
            event_types = [cast(type[object], event_type_or_listener)]
            method_result = self._listener_method(listener)
            if method_result is None:
                return self._invalid_listener()
            method = method_result
            target = listener
        for event_type in event_types:
            registration = self._registry.register(event_type, target, method)
            if isinstance(registration, Failure):
                return registration
        return Success(None)


    @override
    def push(self, event: EventProtocol) -> None:
        self._pushed.append(event)


    @override
    def subscribe(self, subscriber: type[object] | object) -> Result[None]:
        instance = self._resolve_subscriber(subscriber)
        method = getattr(instance, 'subscribe', None)
        if not callable(method):
            return Failure(Error(
                EventListenerRegistrationError.INVALID_LISTENER,
                details={'subscriber': type(instance).__name__},
            ))
        try:
            result = method(self)
            if inspect.isawaitable(result):
                return Failure(Error(
                    EventListenerRegistrationError.SUBSCRIBER_FAILED,
                    details={'subscriber': type(instance).__name__, 'message': 'subscribe must be synchronous'},
                ))
        except Exception as exception:
            return Failure(Error(
                EventListenerRegistrationError.SUBSCRIBER_FAILED,
                details={'subscriber': type(instance).__name__, 'exception': exception},
            ))
        return Success(None)


    @override
    async def until(self, event: EventProtocol) -> Result[object | None]:
        validation = self._validate_event(event)
        if isinstance(validation, Failure):
            return validation.map(lambda _: None)
        if self._deferred and self._should_defer(event):
            self._deferred[-1].events.append(event)
            return Success(None)
        registrations = self._registrations(event)
        for registration in registrations:
            if self._is_queued_listener(cast(EventListenerRegistrationData, registration).listener):
                return Failure(Error(
                    EventDispatcherError.QUEUED_LISTENER_UNSUPPORTED,
                    details={'event': type(event).__name__},
                ))
            response = await self._invoke_registration(registration, event)
            if isinstance(response, Failure):
                return response
            value = response.unwrap()
            if value is not None:
                return Success(value)
        return Success(None)


    @override
    def until_sync(self, event: EventProtocol) -> Result[object | None]:
        if self._running_loop():
            return Failure(Error(
                EventDispatcherError.ASYNC_CONTEXT_REQUIRED,
                details={'event': type(event).__name__},
            ))
        return asyncio.run(self.until(event))


    async def _dispatch_now(self, event: EventProtocol) -> Result[list[object]]:
        registrations = self._registrations(event)
        responses: list[object] = []
        for registration in registrations:
            result = await self._invoke_registration(registration, event)
            if isinstance(result, Failure):
                return result
            responses.append(result.unwrap())
        return Success(responses)


    def _event_types_from_callable(
        self,
        listener: Callable[..., object],
    ) -> list[type[EventProtocol]]:
        try:
            target: object = listener
            if isinstance(listener, QueueableEventListener):
                target = listener.callback
            elif not inspect.isfunction(listener) and not inspect.ismethod(listener):
                target = listener.__call__
            signature = inspect.signature(target)
            parameter = next(
                parameter
                for parameter in signature.parameters.values()
                if parameter.kind in {
                    inspect.Parameter.POSITIONAL_ONLY,
                    inspect.Parameter.POSITIONAL_OR_KEYWORD,
                    inspect.Parameter.KEYWORD_ONLY,
                }
            )
            hints = get_type_hints(target)
            annotation = hints.get(parameter.name, parameter.annotation)
        except (AttributeError, StopIteration, TypeError, ValueError):
            return []
        return self._event_types_from_annotation(annotation)


    def _event_types_from_annotation(self, annotation: object) -> list[type[EventProtocol]]:
        annotations = get_args(annotation)
        origin = get_origin(annotation)
        values = (
            annotations
            if origin in {types.UnionType, getattr(typing, 'Union')}
            else (annotation,)
        )
        return [
            cast(type[EventProtocol], value)
            for value in values
            if self._is_event_type(value)
        ]


    def _invalid_listener(self) -> Failure[Error]:
        return Failure(Error(EventListenerRegistrationError.INVALID_LISTENER))


    async def _invoke_registration(
        self,
        registration_object: object,
        event: EventProtocol,
    ) -> Result[object]:
        registration = cast(EventListenerRegistrationData, registration_object)
        try:
            if self._is_queued_listener(registration.listener):
                return self._queue_listener(registration, event)
            listener = self._resolve_listener(registration.listener)
            method = getattr(listener, registration.method)
            response = method(event)
            if inspect.isawaitable(response):
                response = await response
            return Success(response)
        except Exception as exception:
            return Failure(Error(EventDispatcherError.LISTENER_FAILED, details={
                'event': type(event).__name__,
                'exception': exception,
                'listener': type(registration.listener).__name__,
            }))


    def _is_event_type(self, value: object) -> bool:
        return isinstance(value, type) and getattr(value, 'event_marker', False) is True


    def _is_queued_listener(self, listener: object) -> bool:
        if isinstance(listener, type):
            return issubclass(listener, ShouldQueueEventListenerTag)
        return isinstance(listener, ShouldQueueEventListenerTag) or isinstance(
            listener,
            QueueableEventListener,
        )


    def _listener_method(self, listener: object) -> str | None:
        handle = getattr(listener, 'handle', None)
        if callable(handle):
            return 'handle'
        if callable(listener):
            return '__call__'
        return None


    def _queue_listener(
        self,
        registration: EventListenerRegistrationData,
        event: EventProtocol,
    ) -> Result[object]:
        listener = registration.listener
        connection: str | None = None
        delay: int | None = None
        queue = 'default'
        if isinstance(listener, QueueableEventListener):
            connection = listener.connection
            delay = listener.delay
            queue = listener.queue
        else:
            connection_value = getattr(listener, 'connection', None)
            delay_value = getattr(listener, 'delay', None)
            queue_value = getattr(listener, 'queue', 'default')
            connection = connection_value if isinstance(connection_value, str) else None
            delay = delay_value if isinstance(delay_value, int) else None
            queue = queue_value if isinstance(queue_value, str) else 'default'
        job = QueuedEventListenerJob(listener, registration.method, event)
        resolver = self._queue_resolver
        if resolver is None:
            resolver = cast(
                QueueResolverProtocol,
                self._container.make(QueueResolverProtocol),
            )
        driver = resolver.connection(connection)
        result = (
            driver.later(delay, job, queue)
            if delay is not None and delay > 0
            else driver.push(job, queue)
        )
        return result.map(lambda job_id: job_id)


    def _registrations(self, event: EventProtocol) -> list[object]:
        return self._registry.listeners(type(event))


    def _resolve_listener(self, listener: object) -> object:
        if isinstance(listener, type):
            return self._container.make(listener)
        return listener


    def _resolve_subscriber(self, subscriber: type[object] | object) -> EventSubscriberProtocol:
        instance = (
            self._container.make(subscriber)
            if isinstance(subscriber, type)
            else subscriber
        )
        return cast(EventSubscriberProtocol, instance)


    def _running_loop(self) -> bool:
        try:
            _ = asyncio.get_running_loop()
        except RuntimeError:
            return False
        return True


    def _should_defer(self, event: EventProtocol) -> bool:
        event_types = self._deferred[-1].event_types
        return event_types is None or type(event) in event_types


    def _validate_event(self, event: EventProtocol) -> Result[None]:
        if not self._is_event_type(type(event)):
            return Failure(Error(EventDispatcherError.INVALID_EVENT, details={
                'event': type(event).__name__,
            }))
        return Success(None)
