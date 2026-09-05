from __future__ import annotations

from collections.abc import Mapping
from typing import override

from armaden.framework.protocols.http_request_protocol import HttpRequestProtocol
from armaden.framework.runtime.http.authentication.config_user_provider import ConfigUserProvider
from armaden.framework.runtime.http.authentication.dto.api_user_data import ApiUserData
from armaden.framework.runtime.http.authentication.guards.authentication_guard import AuthenticationGuard


class TokenGuard(AuthenticationGuard):
    def __init__(self, provider: ConfigUserProvider, config: Mapping[str, object]) -> None:
        self._field: str | None = self._optional_string(config.get('field'))
        self._header: str = self._string(config.get('header'), 'Authorization')
        self._prefix: str = self._string(config.get('prefix'), 'Bearer')
        self._provider: ConfigUserProvider = provider


    @staticmethod
    def _optional_string(value: object) -> str | None:
        return value if isinstance(value, str) else None


    @staticmethod
    def _string(value: object, default: str) -> str:
        return value if isinstance(value, str) else default


    def _extract_token(self, request: HttpRequestProtocol) -> str | None:
        if self._field:
            value = request.input(self._field)
            return value if isinstance(value, str) else None
        value = request.header(self._header, '')
        if not value:
            return None
        if self._prefix and value.startswith(f'{self._prefix} '):
            return value[len(self._prefix) + 1:]
        if self._prefix and value.startswith(self._prefix):
            return value[len(self._prefix):]
        return value if not self._prefix else None


    @override
    async def attempt(self, request: HttpRequestProtocol) -> ApiUserData | None:
        token = self._extract_token(request)
        return None if token is None else self._provider.retrieve_by_token(token)
