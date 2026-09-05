from dataclasses import dataclass, field


@dataclass(slots=True)
class DiscoverySettingsData:
    bind_interfaces: bool = True
    bind_self: bool = True
    enabled: bool = False
    excluded_interfaces: frozenset[type] = frozenset()
    paths: list[str] = field(default_factory=list)
    shared: bool = True
