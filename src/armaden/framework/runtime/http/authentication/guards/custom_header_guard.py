from __future__ import annotations

from collections.abc import Mapping
from typing import override

from armaden.framework.protocols.http_request_protocol import HttpRequestProtocol
from armaden.framework.runtime.http.authentication.config_user_provider import ConfigUserProvider
from armaden.framework.runtime.http.authentication.dto.api_user_data import ApiUserData
from armaden.framework.runtime.http.authentication.guards.authentication_guard import AuthenticationGuard


class CustomHeaderGuard(AuthenticationGuard):
    def __init__(self, provider: ConfigUserProvider, config: Mapping[str, object]) -> None:
        self._header: str = self._string(config.get('header'), 'X-API-Key')
        self._prefix: str | None = self._optional_string(config.get('prefix'))
        self._provider: ConfigUserProvider = provider


    @staticmethod
    def _optional_string(value: object) -> str | None:
        return value if isinstance(value, str) else None


    @staticmethod
    def _string(value: object, default: str) -> str:
        return value if isinstance(value, str) else default


    @override
    async def attempt(self, request: HttpRequestProtocol) -> ApiUserData | None:
        value = request.header(self._header, '')
        if not value:
            return None
        if self._prefix and value.startswith(f'{self._prefix} '):
            token = value[len(self._prefix) + 1:]
        elif self._prefix and value.startswith(self._prefix):
            token = value[len(self._prefix):]
        else:
            token = value
        return self._provider.retrieve_by_token(token) if token else None
