from __future__ import annotations

from collections.abc import Callable, Mapping
from typing import Protocol

from armaden.framework.protocols.authentication_guard_protocol import AuthenticationGuardProtocol
from armaden.framework.protocols.http_request_protocol import HttpRequestProtocol


class AuthenticationManagerProtocol(Protocol):
    async def authenticate(
        self,
        request: HttpRequestProtocol,
        guard_name: str | None = None,
    ) -> object | None: ...

    def bootstrap(self, authentication_config: Mapping[str, object] | None = None) -> None: ...

    def extend(self, driver: str, creator: Callable[..., AuthenticationGuardProtocol]) -> None: ...

    def get_default_guard(self) -> str: ...

    def guard(self, name: str | None = None) -> AuthenticationGuardProtocol: ...