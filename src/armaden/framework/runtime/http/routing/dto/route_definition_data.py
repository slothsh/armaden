from __future__ import annotations

from dataclasses import dataclass, field
from typing import override


@dataclass(frozen=True)
class RouteDefinitionData:
    handler: object
    methods: list[str]
    middleware: list[str] = field(default_factory=list)
    name: str | None = None
    path: str = ''
    where: dict[str, str] = field(default_factory=dict)

    @override
    def __repr__(self) -> str:
        methods = '|'.join(self.methods)
        return f'RouteDefinition({methods} {self.path})'
