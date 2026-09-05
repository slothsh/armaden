from enum import StrEnum


class EventListenerDiscoveryError(StrEnum):
    INVALID_EVENT_ANNOTATION = 'a listener event annotation is not an Event subclass'
    INVALID_LISTENER_METHOD = 'a listener method does not expose an event parameter'
    UNRESOLVED_ANNOTATION = 'a listener event annotation could not be resolved'
