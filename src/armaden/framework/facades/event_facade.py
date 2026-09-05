from collections.abc import Awaitable, Callable
from typing import cast, override

from armaden.framework.facades.facade import Facade
from armaden.framework.protocols.event_dispatcher_protocol import (
    EventDispatcherProtocol,
)
from armaden.framework.protocols.event_protocol import EventProtocol
from armaden.framework.runtime.events.queueable_event_listener import (
    QueueableEventListener,
)
from armaden.framework.types.result import Result


class EventFacade(Facade):
    @override
    @classmethod
    def get_facade_accessor(cls) -> object:
        return 'events.dispatcher'


    @classmethod
    async def defer(
        cls,
        callback: Callable[[], object | Awaitable[object]],
        events: list[type[EventProtocol]] | None = None,
    ) -> Result[object]:
        return await cls._dispatcher().defer(callback, events)


    @classmethod
    async def dispatch(cls, event: EventProtocol) -> Result[list[object]]:
        return await cls._dispatcher().dispatch(event)


    @classmethod
    def dispatch_sync(cls, event: EventProtocol) -> Result[list[object]]:
        return cls._dispatcher().dispatch_sync(event)


    @classmethod
    async def flush(cls, event_type: type[EventProtocol]) -> Result[list[object]]:
        return await cls._dispatcher().flush(event_type)


    @classmethod
    def forget(cls, event_type: type[EventProtocol]) -> None:
        cls._dispatcher().forget(event_type)


    @classmethod
    def forget_pushed(cls) -> None:
        cls._dispatcher().forget_pushed()


    @classmethod
    def has_listeners(cls, event_type: type[EventProtocol]) -> bool:
        return cls._dispatcher().has_listeners(event_type)


    @classmethod
    def listen(
        cls,
        event_type_or_listener: type[EventProtocol] | Callable[..., object],
        listener: object | None = None,
    ) -> Result[None]:
        return cls._dispatcher().listen(event_type_or_listener, listener)


    @classmethod
    def push(cls, event: EventProtocol) -> None:
        cls._dispatcher().push(event)


    @classmethod
    def queueable(
        cls,
        listener: Callable[..., object],
    ) -> QueueableEventListener:
        return QueueableEventListener(listener)


    @classmethod
    def subscribe(cls, subscriber: type[object] | object) -> Result[None]:
        return cls._dispatcher().subscribe(subscriber)


    @classmethod
    async def until(cls, event: EventProtocol) -> Result[object | None]:
        return await cls._dispatcher().until(event)


    @classmethod
    def until_sync(cls, event: EventProtocol) -> Result[object | None]:
        return cls._dispatcher().until_sync(event)


    @classmethod
    def _dispatcher(cls) -> EventDispatcherProtocol:
        return cast(EventDispatcherProtocol, cls.get_facade_root())
