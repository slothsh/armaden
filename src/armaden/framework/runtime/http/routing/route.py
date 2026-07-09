from dataclasses import dataclass, field
from typing import Callable


@dataclass(frozen=True)
class RouteDefinition:
    methods: list[str]
    path: str
    handler: tuple[type, str] | Callable
    name: str | None = None
    middleware: list[str] = field(default_factory=list)
    where: dict[str, str] = field(default_factory=dict)

    def __repr__(self) -> str:
        methods_str = '|'.join(self.methods)
        return f'RouteDefinition({methods_str} {self.path})'
