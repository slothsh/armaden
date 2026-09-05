from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class ApiUserData:
    id: str
    metadata: dict[str, object] = field(default_factory=dict)
    roles: list[str] = field(default_factory=list)
    username: str | None = None

    def has_role(self, role: str) -> bool:
        return role in self.roles