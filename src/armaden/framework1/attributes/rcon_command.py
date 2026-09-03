from __future__ import annotations


_RCON_REGISTRARS_ATTR = '__rcon_registrars__'


def register_rcon_command(*registrars: type) -> type:
    def decorator(cls: type) -> type:
        setattr(cls, _RCON_REGISTRARS_ATTR, list(registrars))
        return cls
    return decorator
