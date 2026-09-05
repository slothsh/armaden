from enum import StrEnum


class EventListenerRegistrationError(StrEnum):
    INVALID_LISTENER = 'the event listener is not a supported class or callable'
    SUBSCRIBER_FAILED = 'an event subscriber failed during registration'
