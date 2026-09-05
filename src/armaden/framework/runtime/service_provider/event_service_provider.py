from __future__ import annotations

import logging
from collections.abc import Mapping
from typing import cast, override

from returns.result import Failure, Success

from armaden.framework.protocols.class_discovery_protocol import (
    ClassDiscoveryProtocol,
)
from armaden.framework.protocols.container_protocol import ContainerProtocol
from armaden.framework.protocols.core_application_protocol import (
    CoreApplicationProtocol,
)
from armaden.framework.protocols.event_dispatcher_protocol import (
    EventDispatcherProtocol,
)
from armaden.framework.protocols.event_listener_registry_protocol import (
    EventListenerRegistryProtocol,
)
from armaden.framework.runtime.events.dto.event_listener_registration_data import (
    EventListenerRegistrationData,
)
from armaden.framework.runtime.events.dto.event_subscriber_registration_data import (
    EventSubscriberRegistrationData,
)
from armaden.framework.runtime.events.event_dispatcher import EventDispatcher
from armaden.framework.runtime.events.event_listener_discovery import (
    EventListenerDiscovery,
)
from armaden.framework.runtime.events.event_listener_registry import (
    EventListenerRegistry,
)
from armaden.framework.runtime.service_provider.service_provider import ServiceProvider
from armaden.framework.runtime.supervisor.task.dto.task_graph_data import TaskGraphData
from armaden.framework.types.result import Result

logger = logging.getLogger(__name__)


class EventServiceProvider(ServiceProvider):
    name: str = 'events'

    def __init__(self, container: ContainerProtocol) -> None:
        super().__init__(container)
        self._dispatcher: EventDispatcher | None = None


    @override
    def boot(self) -> Result[None]:
        dispatcher = self._dispatcher
        if dispatcher is None:
            return Success(None)
        configuration = cast(
            CoreApplicationProtocol[TaskGraphData],
            self._container.make('app'),
        )
        raw_events = configuration.config('events', {})
        events_configuration: Mapping[str, object] = (
            cast(Mapping[str, object], raw_events)
            if isinstance(raw_events, Mapping)
            else {}
        )
        discovery_configuration = self._discovery_configuration(events_configuration)
        if discovery_configuration.get('enabled') is not True:
            logger.debug('Event listener discovery is disabled')
            return Success(None)
        paths = self._paths(discovery_configuration.get('paths'))
        discovery = EventListenerDiscovery(
            cast(ClassDiscoveryProtocol, self._container.make(ClassDiscoveryProtocol)),
        )
        result = discovery.discover(paths)
        if isinstance(result, Failure):
            return result.map(lambda _: None)
        registrations = result.unwrap()
        registered = 0
        for registration in registrations:
            if isinstance(registration, EventListenerRegistrationData):
                event_type = cast(type, registration.event_type)
                listener_result = dispatcher.listen(
                    event_type,
                    registration.listener,
                )
                if isinstance(listener_result, Failure):
                    return listener_result
                registered += 1
            elif isinstance(registration, EventSubscriberRegistrationData):
                subscriber_result = dispatcher.subscribe(registration.subscriber)
                if isinstance(subscriber_result, Failure):
                    return subscriber_result
                registered += 1
        logger.info(
            'Registered %d discovered event listener/subscriber entries from %d path(s)',
            registered,
            len(paths),
        )
        return Success(None)


    @override
    def register(self) -> Result[None]:
        registry = EventListenerRegistry()
        dispatcher = EventDispatcher(self._container, registry)
        self._dispatcher = dispatcher
        _ = self._container.instance(EventListenerRegistryProtocol, registry)
        _ = self._container.instance(EventDispatcherProtocol, dispatcher)
        _ = self._container.instance('events.dispatcher', dispatcher)
        return Success(None)


    def _discovery_configuration(
        self,
        configuration: Mapping[str, object],
    ) -> Mapping[str, object]:
        listeners = configuration.get('listeners', {})
        listeners_mapping: Mapping[str, object] = (
            cast(Mapping[str, object], listeners)
            if isinstance(listeners, Mapping)
            else {}
        )
        discovery = listeners_mapping.get('discovery', {})
        return (
            cast(Mapping[str, object], discovery)
            if isinstance(discovery, Mapping)
            else {}
        )


    def _paths(self, value: object) -> list[str]:
        if not isinstance(value, list):
            return ['app/listeners']
        values = cast(list[object], value)
        return [item for item in values if isinstance(item, str)]
