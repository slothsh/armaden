from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


class _Missing:
    __slots__ = ()

    _instance: '_Missing | None' = None

    def __new__(cls) -> '_Missing':
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __bool__(self) -> bool:
        return False

    def __repr__(self) -> str:
        return '<MISSING>'

    def __copy__(self) -> '_Missing':
        return self

    def __deepcopy__(self, memo) -> '_Missing':
        return self


_MISSING: Any = _Missing()


@dataclass
class RconCommandArgSpec:
    name: str
    type: type
    required: bool = True
    default: Any = field(default_factory=lambda: _MISSING)
    description: str | None = None
