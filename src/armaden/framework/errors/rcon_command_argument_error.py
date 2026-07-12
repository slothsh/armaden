from __future__ import annotations

from typing import Any


class RconCommandArgumentError(Exception):
    def __init__(self, command_name: str, args: dict[str, Any], errors: list[str]) -> None:
        self.command_name = command_name
        self.args = args
        self.errors = errors
        detail = '; '.join(errors) if errors else 'argument validation failed'
        super().__init__(
            f"RCON command '{command_name}' failed argument validation: {detail}"
        )
