from collections.abc import Awaitable, Callable, Mapping

from armaden.framework.protocols.event_protocol import EventProtocol


type EventType = type[EventProtocol]
type EventsConfiguration = Mapping[str, object]
type EventListenerCallback = Callable[[object], object]
type AsyncEventListenerCallback = Callable[[object], Awaitable[object]]
type DispatchCallback = Callable[[], object | Awaitable[object]]
type ListenerResult = object | Awaitable[object]