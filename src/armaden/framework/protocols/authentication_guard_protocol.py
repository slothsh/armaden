from __future__ import annotations

from typing import Protocol

from armaden.framework.protocols.http_request_protocol import HttpRequestProtocol


class AuthenticationGuardProtocol(Protocol):
    async def attempt(self, request: HttpRequestProtocol) -> object | None: ...