from __future__ import annotations

from collections.abc import Awaitable
from typing import Protocol


class RconSendCommandProtocol(Protocol):
    def send_command(self, command: str, *args: str) -> Awaitable[object]: ...
