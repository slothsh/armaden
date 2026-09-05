from __future__ import annotations

from abc import ABC
from typing import ClassVar

from returns.result import Success

from armaden.framework.facades.event_facade import EventFacade
from armaden.framework.protocols.event_dispatcher_protocol import (
    EventDispatcherProtocol,
)
from armaden.framework.protocols.event_listener_discovery_protocol import (
    EventListenerDiscoveryProtocol,
)
from armaden.framework.protocols.event_listener_protocol import EventListenerProtocol
from armaden.framework.protocols.event_protocol import EventProtocol
from armaden.framework.protocols.event_queueable_listener_protocol import (
    QueueableEventListenerProtocol,
)
from armaden.framework.protocols.event_subscriber_protocol import (
    EventSubscriberProtocol,
)
from armaden.framework.runtime.events.dto.event_listener_registration_data import (
    EventListenerRegistrationData,
)
from armaden.framework.runtime.events.dto.event_subscriber_registration_data import (
    EventSubscriberRegistrationData,
)
from armaden.framework.runtime.events.event import Event as RuntimeEvent
from armaden.framework.runtime.events.event_listener_discovery import (
    EventListenerDiscovery,
)
from armaden.framework.runtime.events.queueable_event_listener import (
    QueueableEventListener,
)
from armaden.framework.runtime.events.tags import ShouldQueueEventListenerTag
from armaden.framework.types.result import Result


class Event(RuntimeEvent):
    event_marker: ClassVar[bool] = True


    @classmethod
    async def dispatch(cls, *args: object, **kwargs: object) -> Result[list[object]]:
        return await EventFacade.dispatch(cls(*args, **kwargs))


    @classmethod
    async def dispatch_if(
        cls,
        condition: bool,
        *args: object,
        **kwargs: object,
    ) -> Result[list[object]]:
        if not condition:
            return Success([])
        return await cls.dispatch(*args, **kwargs)


    @classmethod
    async def dispatch_unless(
        cls,
        condition: bool,
        *args: object,
        **kwargs: object,
    ) -> Result[list[object]]:
        if condition:
            return Success([])
        return await cls.dispatch(*args, **kwargs)


    @classmethod
    def dispatch_sync(
        cls,
        *args: object,
        **kwargs: object,
    ) -> Result[list[object]]:
        return EventFacade.dispatch_sync(cls(*args, **kwargs))


    @classmethod
    def dispatch_if_sync(
        cls,
        condition: bool,
        *args: object,
        **kwargs: object,
    ) -> Result[list[object]]:
        if not condition:
            return Success([])
        return cls.dispatch_sync(*args, **kwargs)


    @classmethod
    def dispatch_unless_sync(
        cls,
        condition: bool,
        *args: object,
        **kwargs: object,
    ) -> Result[list[object]]:
        if condition:
            return Success([])
        return cls.dispatch_sync(*args, **kwargs)


class EventListener(EventListenerProtocol, ABC):
    def __init__(self) -> None:
        pass


__all__ = [
    'Event',
    'EventDispatcherProtocol',
    'EventFacade',
    'EventListener',
    'EventListenerDiscovery',
    'EventListenerDiscoveryProtocol',
    'EventListenerProtocol',
    'EventListenerRegistrationData',
    'EventProtocol',
    'EventSubscriberProtocol',
    'QueueableEventListenerProtocol',
    'EventSubscriberRegistrationData',
    'QueueableEventListener',
    'ShouldQueueEventListenerTag',
]
