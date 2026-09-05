from __future__ import annotations

import json
import re
from collections.abc import Callable
from typing import override

from starlette.requests import Request as StarletteRequest

from armaden.framework.protocols.http_request_protocol import HttpRequestProtocol


class HttpRequest(HttpRequestProtocol):
    def __init__(self, request: StarletteRequest) -> None:
        self._form_data: dict[str, object] | None = None
        self._json_body: dict[str, object] | None = None
        self._request: StarletteRequest = request
        self._query_params: dict[str, object] | None = None


    def _get_form_data(self) -> dict[str, object]:
        if self._form_data is None:
            self._form_data = {}
        return self._form_data


    def _get_json_body(self) -> dict[str, object]:
        if self._json_body is None:
            return {}
        return self._json_body


    def _get_query_params(self) -> dict[str, object]:
        if self._query_params is None:
            self._query_params = {}
            items = self._request.query_params.multi_items()
            for key, value in items:
                if key in self._query_params:
                    existing = self._query_params[key]
                    if isinstance(existing, list):
                        existing.append(value)
                    else:
                        self._query_params[key] = [existing, value]
                else:
                    self._query_params[key] = value
        return self._query_params


    async def load_body(self) -> None:
        content_type = self._request.headers.get('content-type', '')
        if 'application/json' in content_type:
            try:
                raw = await self._request.body()
                value: object = json.loads(raw) if raw else {}
                self._json_body = value if isinstance(value, dict) else {}
            except Exception:
                self._json_body = {}
            return
        if (
            'application/x-www-form-urlencoded' in content_type
            or 'multipart/form-data' in content_type
        ):
            try:
                form = await self._request.form()
                self._form_data = {key: value for key, value in form.items()}
            except Exception:
                self._form_data = {}


    @override
    def accepts(self, *content_types: str) -> bool:
        accept = self._request.headers.get('Accept', '')
        return any(content_type in accept for content_type in content_types)


    @override
    def accepts_html(self) -> bool:
        return self.accepts('text/html')


    @override
    def accepts_json(self) -> bool:
        return self.accepts('application/json')


    @override
    def all(self) -> dict[str, object]:
        return {
            **self._get_query_params(),
            **self._get_form_data(),
            **self._get_json_body(),
        }


    @override
    def bearer_token(self) -> str | None:
        authorization = self.header('Authorization', '')
        if authorization and authorization.startswith('Bearer '):
            return authorization[7:]
        return None


    @override
    async def body(self) -> bytes:
        return await self.content()


    @override
    async def content(self) -> bytes:
        return await self._request.body()


    @override
    def except_(self, *keys: str) -> dict[str, object]:
        values = self.all()
        return {key: value for key, value in values.items() if key not in keys}


    @override
    def expects_json(self) -> bool:
        accept = self.header('Accept', '')
        return 'application/json' in accept if accept else False


    @override
    def file(self, key: str) -> object | None:
        _ = key
        raise NotImplementedError('File support is not implemented')


    @override
    def filled(self, key: str | list[str]) -> bool:
        keys = [key] if isinstance(key, str) else key
        values = self.all()
        return all(name in values and values[name] != '' for name in keys)


    @override
    def full_url(self) -> str:
        return str(self._request.url)


    @override
    def full_url_is(self, *patterns: str) -> bool:
        url = self.full_url()
        return any(re.match(pattern, url) for pattern in patterns)


    @override
    def has(self, key: str | list[str]) -> bool:
        keys = [key] if isinstance(key, str) else key
        values = self.all()
        return all(name in values for name in keys)


    @override
    def has_file(self, key: str) -> bool:
        _ = key
        raise NotImplementedError('File support is not implemented')


    @override
    def has_header(self, key: str) -> bool:
        return key in self._request.headers


    @override
    def has_session(self) -> bool:
        return False


    @override
    def header(self, key: str, default: object | None = None) -> str | None:
        value = self._request.headers.get(key)
        if value is None:
            return default if isinstance(default, str) else None
        return value


    @override
    def input(self, key: str | None = None, default: object | None = None) -> object:
        values = self.all()
        if key is None:
            return values
        return values.get(key, default)


    @override
    def ip(self) -> str:
        forwarded = self.header('X-Forwarded-For')
        if forwarded:
            return forwarded.split(',')[0].strip()
        real_ip = self.header('X-Real-IP')
        if real_ip:
            return real_ip.strip()
        if self._request.client is not None:
            return self._request.client.host
        return '127.0.0.1'


    @override
    def is_(self, pattern: str) -> bool:
        return bool(re.match(pattern, self.path()))


    @override
    def is_authenticated(self) -> bool:
        return self.user() is not None


    @override
    def is_method(self, method: str) -> bool:
        return self.method() == method.upper()


    @override
    async def json(
        self,
        key: str | None = None,
        default: object | None = None,
    ) -> object:
        values = self._get_json_body()
        if key is None:
            return values
        return values.get(key, default)


    @override
    def method(self) -> str:
        return self._request.method.upper()


    @override
    def missing(self, key: str | list[str]) -> bool:
        return not self.has(key)


    @override
    def only(self, *keys: str) -> dict[str, object]:
        values = self.all()
        return {key: values[key] for key in keys if key in values}


    @override
    def path(self) -> str:
        return self._request.url.path


    @override
    def post(self, key: str | None = None, default: object | None = None) -> object:
        values = {**self._get_form_data(), **self._get_json_body()}
        if key is None:
            return values
        return values.get(key, default)


    @override
    def query(self, key: str | None = None, default: object | None = None) -> object:
        values = self._get_query_params()
        if key is None:
            return values
        return values.get(key, default)


    @override
    def route_is(self, *names: str) -> bool:
        route_name = getattr(self._request.state, 'route_name', None)
        return isinstance(route_name, str) and route_name in names


    @override
    def session(self) -> object:
        raise NotImplementedError('Session support is not yet implemented')


    @override
    def set_user(self, user: object) -> None:
        self._request.state._armaden_user = user


    @override
    def url(self) -> str:
        return str(self._request.url)


    @override
    def user(self) -> object | None:
        return getattr(self._request.state, '_armaden_user', None)


    @override
    def user_agent(self) -> str:
        return self.header('User-Agent', '') or ''


    @override
    def wants_json(self) -> bool:
        accept = self.header('Accept', '')
        return bool(
            accept
            and (
                'application/json' in accept
                or 'application/*' in accept
                or '*/*' in accept
            )
        )


    @override
    def when_filled(self, key: str, callback: Callable[..., object]) -> None:
        if self.filled(key):
            _ = callback(self.input(key))


    @override
    def when_has(self, key: str, callback: Callable[..., object]) -> None:
        if self.has(key):
            _ = callback(self.input(key))
