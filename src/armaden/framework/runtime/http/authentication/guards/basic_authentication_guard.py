from __future__ import annotations

import base64
from collections.abc import Mapping
from typing import override

from armaden.framework.protocols.http_request_protocol import HttpRequestProtocol
from armaden.framework.runtime.http.authentication.config_user_provider import ConfigUserProvider
from armaden.framework.runtime.http.authentication.dto.api_user_data import ApiUserData
from armaden.framework.runtime.http.authentication.guards.authentication_guard import AuthenticationGuard


class BasicAuthenticationGuard(AuthenticationGuard):
    def __init__(self, provider: ConfigUserProvider, config: Mapping[str, object]) -> None:
        self._header: str = self._string(config.get('header'), 'Authorization')
        self._prefix: str = self._string(config.get('prefix'), 'Basic')
        self._provider: ConfigUserProvider = provider


    def _extract_credentials(self, request: HttpRequestProtocol) -> tuple[str, str] | None:
        value = request.header(self._header, '')
        if not value:
            return None
        if self._prefix and value.startswith(f'{self._prefix} '):
            encoded = value[len(self._prefix) + 1:]
        elif self._prefix and value.startswith(self._prefix):
            encoded = value[len(self._prefix):]
        else:
            return None
        try:
            decoded = base64.b64decode(encoded).decode('utf-8')
        except Exception:
            return None
        if ':' not in decoded:
            return None
        username, password = decoded.split(':', 1)
        return username, password


    @staticmethod
    def _string(value: object, default: str) -> str:
        return value if isinstance(value, str) else default


    @override
    async def attempt(self, request: HttpRequestProtocol) -> ApiUserData | None:
        credentials = self._extract_credentials(request)
        if credentials is None:
            return None
        return self._provider.retrieve_by_credentials(*credentials)
