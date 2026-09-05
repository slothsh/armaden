from enum import StrEnum


class DiscoveryBinderError(StrEnum):
    EXCLUDED_INTERFACE_BINDING = 'a discovered type attempted to bind an excluded interface'
