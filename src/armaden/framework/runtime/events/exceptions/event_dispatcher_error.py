from enum import StrEnum


class EventDispatcherError(StrEnum):
    ASYNC_CONTEXT_REQUIRED = 'the async event dispatch bridge requires a non-running event loop'
    DEFERRED_CALLBACK_FAILED = 'a deferred event callback failed'
    INVALID_EVENT = 'the dispatched value is not an Event instance'
    LISTENER_FAILED = 'an event listener failed during dispatch'
    QUEUED_LISTENER_UNSUPPORTED = 'a queued listener cannot be used with halt-on-response dispatch'
