from dataclasses import dataclass, field
from typing import Any


@dataclass
class ApiUser:
    id: str
    roles: list[str] = field(default_factory=list)
    username: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def has_role(self, role: str) -> bool:
        return role in self.roles
