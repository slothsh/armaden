from __future__ import annotations

from typing import Protocol


class RconCommandProtocol(Protocol):
    category: str
    command_name: str
    description: str

    async def execute(self, **kwargs: object) -> object: ...

    async def on_response(self, response: object) -> object: ...

    def validate(self, **kwargs: object) -> tuple[dict[str, object], list[str]]: ...
