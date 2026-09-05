from __future__ import annotations

from dataclasses import dataclass, field

from armaden.framework.api.rcon.tags.rcon_missing_argument_tag import (
    RCON_MISSING_ARGUMENT,
)


@dataclass
class RconCommandArgumentData:
    name: str
    type: type[object] | None = None
    required: bool = True
    default: object = field(default_factory=lambda: RCON_MISSING_ARGUMENT)
    description: str | None = None


__all__ = [
    'RconCommandArgumentData',
]
