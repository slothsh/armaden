import base64
from abc import ABC, abstractmethod
from typing import Any

from ..request import Request
from .api_user import ApiUser
from .config_user_provider import ConfigUserProvider


class AuthGuard(ABC):
    @abstractmethod
    async def attempt(self, request: Request) -> ApiUser | None:
        raise NotImplementedError


class TokenGuard(AuthGuard):
    def __init__(self, provider: ConfigUserProvider, config: dict[str, Any]) -> None:
        self._provider = provider
        self._header = config.get('header', 'Authorization')
        self._prefix = config.get('prefix', 'Bearer')
        self._field = config.get('field')

    async def attempt(self, request: Request) -> ApiUser | None:
        token = self._extract_token(request)
        if token is None:
            return None
        return self._provider.retrieve_by_token(token)

    def _extract_token(self, request: Request) -> str | None:
        if self._field:
            return request.input(self._field)

        header_value = request.header(self._header, '')
        if not header_value:
            return None

        prefix = self._prefix or ''
        if prefix and header_value.startswith(prefix + ' '):
            return header_value[len(prefix) + 1:]
        if prefix and header_value.startswith(prefix):
            return header_value[len(prefix):]
        return header_value if not prefix else None


class BasicAuthGuard(AuthGuard):
    def __init__(self, provider: ConfigUserProvider, config: dict[str, Any]) -> None:
        self._provider = provider
        self._header = config.get('header', 'Authorization')
        self._prefix = config.get('prefix', 'Basic')

    async def attempt(self, request: Request) -> ApiUser | None:
        credentials = self._extract_credentials(request)
        if credentials is None:
            return None
        username, password = credentials
        return self._provider.retrieve_by_credentials(username, password)

    def _extract_credentials(self, request: Request) -> tuple[str, str] | None:
        header_value = request.header(self._header, '')
        if not header_value:
            return None
        prefix = self._prefix or ''
        if prefix and header_value.startswith(prefix + ' '):
            encoded = header_value[len(prefix) + 1:]
        elif prefix and header_value.startswith(prefix):
            encoded = header_value[len(prefix):]
        else:
            return None
        try:
            decoded = base64.b64decode(encoded).decode('utf-8')
            if ':' not in decoded:
                return None
            username, password = decoded.split(':', 1)
            return username, password
        except Exception:
            return None


class CustomHeaderGuard(AuthGuard):
    def __init__(self, provider: ConfigUserProvider, config: dict[str, Any]) -> None:
        self._provider = provider
        self._header = config.get('header', 'X-API-Key')
        self._prefix = config.get('prefix')

    async def attempt(self, request: Request) -> ApiUser | None:
        header_value = request.header(self._header, '')
        if not header_value:
            return None
        prefix = self._prefix
        if prefix and header_value.startswith(prefix + ' '):
            token = header_value[len(prefix) + 1:]
        elif prefix and header_value.startswith(prefix):
            token = header_value[len(prefix):]
        else:
            token = header_value
        if not token:
            return None
        return self._provider.retrieve_by_token(token)