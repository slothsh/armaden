from __future__ import annotations

import inspect
import logging
import types
from typing import cast, get_args, get_origin, get_type_hints, override
import typing

from returns.pipeline import is_successful
from returns.result import Success

from armaden.framework.runtime.events.event import Event
from armaden.framework.protocols.class_discovery_protocol import (
    ClassDiscoveryProtocol,
)
from armaden.framework.protocols.event_listener_discovery_protocol import (
    EventListenerDiscoveryProtocol,
)
from armaden.framework.runtime.events.dto.event_listener_registration_data import (
    EventListenerRegistrationData,
)
from armaden.framework.runtime.events.dto.event_subscriber_registration_data import (
    EventSubscriberRegistrationData,
)
from armaden.framework.types.result import Result

logger = logging.getLogger(__name__)


class EventListenerDiscovery(EventListenerDiscoveryProtocol):
    def __init__(self, class_discovery: ClassDiscoveryProtocol) -> None:
        self._class_discovery: ClassDiscoveryProtocol = class_discovery


    @override
    def discover(self, paths: list[str]) -> Result[list[object]]:
        result = self._class_discovery.discover(paths)
        if not is_successful(result):
            return result.map(lambda _: [])
        registrations: list[object] = []
        for listener_type in result.unwrap():
            if callable(getattr(listener_type, 'subscribe', None)):
                registrations.append(EventSubscriberRegistrationData(listener_type))
            registrations.extend(self._discover_listener(listener_type))
        return Success(registrations)


    def _discover_listener(
        self,
        listener_type: type[object],
    ) -> list[EventListenerRegistrationData]:
        method_name = self._listener_method(listener_type)
        if method_name is None:
            return []
        method = getattr(listener_type, method_name)
        try:
            signature = inspect.signature(method)
            parameter = next(
                parameter
                for parameter in signature.parameters.values()
                if parameter.name not in {'self', 'cls'}
                and parameter.kind in {
                    inspect.Parameter.POSITIONAL_ONLY,
                    inspect.Parameter.POSITIONAL_OR_KEYWORD,
                    inspect.Parameter.KEYWORD_ONLY,
                }
            )
            hints = get_type_hints(method)
            annotation = hints.get(parameter.name, parameter.annotation)
        except (AttributeError, StopIteration, TypeError, ValueError) as exception:
            logger.warning(
                'Unable to inspect event listener [%s]: %s',
                listener_type.__name__,
                exception,
            )
            return []
        event_types = self._event_types(annotation)
        if not event_types:
            logger.warning(
                'Event listener [%s.%s] has no valid Event annotation',
                listener_type.__name__,
                method_name,
            )
        return [
            EventListenerRegistrationData(
                event_type=event_type,
                listener=listener_type,
                method=method_name,
            )
            for event_type in event_types
        ]


    def _event_types(self, annotation: object) -> list[type[object]]:
        origin = get_origin(annotation)
        values = (
            get_args(annotation)
            if origin in {types.UnionType, getattr(typing, 'Union')}
            else (annotation,)
        )
        return [
            cast(type[object], value)
            for value in values
            if self._is_event_type(value)
        ]


    def _is_event_type(self, value: object) -> bool:
        return isinstance(value, type) and issubclass(value, Event)


    def _listener_method(self, listener_type: type[object]) -> str | None:
        handle = getattr(listener_type, 'handle', None)
        if callable(handle):
            return 'handle'
        invoke = any(
            '__call__' in base.__dict__
            for base in listener_type.__mro__
            if base is not object
        )
        return '__call__' if invoke else None
