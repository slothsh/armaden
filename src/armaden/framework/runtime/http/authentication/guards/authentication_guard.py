from __future__ import annotations

from abc import ABC, abstractmethod
from typing import override

from armaden.framework.protocols.authentication_guard_protocol import AuthenticationGuardProtocol
from armaden.framework.protocols.http_request_protocol import HttpRequestProtocol
from armaden.framework.runtime.http.authentication.dto.api_user_data import ApiUserData


class AuthenticationGuard(AuthenticationGuardProtocol, ABC):
    @abstractmethod
    @override
    async def attempt(self, request: HttpRequestProtocol) -> ApiUserData | None:
        raise NotImplementedError
