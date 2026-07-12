from __future__ import annotations

from typing import TYPE_CHECKING, Protocol, runtime_checkable

if TYPE_CHECKING:
    from armaden.framework.classes.instance_container import InstanceContainer


@runtime_checkable
class DiscoveryHook(Protocol):
    def on_discovery_complete(self, classes: list[type], container: 'InstanceContainer') -> None:
        ...
