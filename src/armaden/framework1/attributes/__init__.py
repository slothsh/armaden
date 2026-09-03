from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from armaden.framework.classes.instance_container import InstanceContainer

_BIND_ATTR = '_armaden_bindings'
_SINGLETON_ATTR = '_armaden_singleton'
_SCOPED_ATTR = '_armaden_scoped'


class Bind:
    def __init__(self, concrete: type, environments: list[str] | None = None) -> None:
        self.concrete = concrete
        self.environments = environments or []

    def __call__(self, cls: type) -> type:
        existing: list[Bind] = getattr(cls, _BIND_ATTR, None)
        if existing is None:
            setattr(cls, _BIND_ATTR, [self])
        else:
            existing.append(self)
        return cls


class Singleton:
    def __call__(self, cls: type) -> type:
        setattr(cls, _SINGLETON_ATTR, True)
        return cls


class Scoped:
    def __call__(self, cls: type) -> type:
        setattr(cls, _SCOPED_ATTR, True)
        return cls


from armaden.framework.attributes.rcon_command import register_rcon_command

__all__ = [
    'Bind',
    'Singleton',
    'Scoped',
    'register_rcon_command',
]