import json as _json
import re
from typing import Any, Callable

from starlette.requests import Request as StarletteRequest


class Request:
    def __init__(self, starlette_request: StarletteRequest) -> None:
        self._request = starlette_request
        self._json_body: dict[str, Any] | None = None
        self._form_data: dict[str, Any] | None = None
        self._query_params: dict[str, Any] | None = None

    # -- Input access ---------------------------------------------------------

    def input(self, key: str | None = None, default: Any = None) -> Any:
        merged = {**self._get_query_params(), **self._get_post_data(), **self._get_json_body()}
        if key is None:
            return merged
        return merged.get(key, default)

    def query(self, key: str | None = None, default: Any = None) -> Any:
        params = self._get_query_params()
        if key is None:
            return params
        return params.get(key, default)

    def post(self, key: str | None = None, default: Any = None) -> Any:
        body = {**self._get_form_data(), **self._get_json_body()}
        if key is None:
            return body
        return body.get(key, default)

    def all(self) -> dict[str, Any]:
        return {**self._get_query_params(), **self._get_form_data(), **self._get_json_body()}

    def only(self, *keys: str) -> dict[str, Any]:
        all_data = self.all()
        return {k: all_data[k] for k in keys if k in all_data}

    def except_(self, *keys: str) -> dict[str, Any]:
        all_data = self.all()
        return {k: v for k, v in all_data.items() if k not in keys}

    def has(self, key: str | list[str]) -> bool:
        keys = [key] if isinstance(key, str) else key
        return all(k in self.all() for k in keys)

    def filled(self, key: str | list[str]) -> bool:
        keys = [key] if isinstance(key, str) else key
        data = self.all()
        return all(k in data and data[k] != '' for k in keys)

    def missing(self, key: str | list[str]) -> bool:
        return not self.has(key)

    def when_has(self, key: str, callback: Callable) -> None:
        if self.has(key):
            callback(self.input(key))

    def when_filled(self, key: str, callback: Callable) -> None:
        if self.filled(key):
            callback(self.input(key))

    # -- Header access --------------------------------------------------------

    def header(self, key: str, default: Any = None) -> str | None:
        return self._request.headers.get(key, default)

    def bearer_token(self) -> str | None:
        auth = self.header('Authorization', '')
        if auth and auth.startswith('Bearer '):
            return auth[7:]
        return None

    def has_header(self, key: str) -> bool:
        return key in self._request.headers

    # -- Request metadata -----------------------------------------------------

    def method(self) -> str:
        return self._request.method.upper()

    def is_method(self, method: str) -> bool:
        return self.method().upper() == method.upper()

    def path(self) -> str:
        return self._request.url.path

    def url(self) -> str:
        return str(self._request.url)

    def full_url(self) -> str:
        url = self._request.url
        return str(url)

    def full_url_is(self, *patterns: str) -> bool:
        url = self.full_url()
        return any(re.match(pattern, url) for pattern in patterns)

    def is_(self, pattern: str) -> bool:
        return bool(re.match(pattern, self.path()))

    def route_is(self, *names: str) -> bool:
        route_name = getattr(self._request.state, 'route_name', None)
        if route_name is None:
            return False
        return route_name in names

    def ip(self) -> str:
        forwarded = self.header('X-Forwarded-For')
        if forwarded:
            return forwarded.split(',')[0].strip()
        real_ip = self.header('X-Real-IP')
        if real_ip:
            return real_ip.strip()
        client = self._request.client
        if client:
            host, _ = client
            return host
        return '127.0.0.1'

    def user_agent(self) -> str:
        return self.header('User-Agent', '') or ''

    def expects_json(self) -> bool:
        accept = self.header('Accept', '')
        return 'application/json' in accept if accept else False

    def wants_json(self) -> bool:
        accept = self.header('Accept', '')
        return ('application/json' in accept or 'application/*' in accept or '*/*' in accept) if accept else False

    def accepts(self, *content_types: str) -> bool:
        accept = self.header('Accept', '')
        return any(ct in accept for ct in content_types) if accept else False

    def accepts_json(self) -> bool:
        return self.accepts('application/json')

    def accepts_html(self) -> bool:
        return self.accepts('text/html')

    # -- Auth -----------------------------------------------------------------

    def _get_user(self) -> Any:
        return getattr(self._request.state, '_armaden_user', None)

    def set_user(self, user: Any) -> None:
        self._request.state._armaden_user = user

    def user(self) -> Any:
        return self._get_user()

    def is_authenticated(self) -> bool:
        return self._get_user() is not None

    # -- Session (placeholder) ------------------------------------------------

    def session(self) -> Any:
        raise NotImplementedError('Session support is not yet implemented')

    def has_session(self) -> bool:
        return False

    # -- Body / Content -------------------------------------------------------

    async def content(self) -> bytes:
        return await self._request.body()

    async def body(self) -> bytes:
        return await self.content()

    async def json(self, key: str | None = None, default: Any = None) -> Any:
        body = self._get_json_body()
        if key is None:
            return body
        return body.get(key, default)

    # -- Files (placeholder) --------------------------------------------------

    def file(self, key: str) -> Any | None:
        _ = key
        raise NotImplementedError("File support is not implemented")

    def has_file(self, key: str) -> bool:
        _ = key
        raise NotImplementedError("File support is not implemented")

    # -- Internal helpers -----------------------------------------------------

    def _get_query_params(self) -> dict[str, Any]:
        if self._query_params is None:
            self._query_params = {}
            for k, v in self._request.query_params.multi_items():
                if k in self._query_params:
                    existing = self._query_params[k]
                    if isinstance(existing, list):
                        existing.append(v)
                    else:
                        self._query_params[k] = [existing, v]
                else:
                    self._query_params[k] = v
        return self._query_params

    def _get_form_data(self) -> dict[str, Any]:
        if self._form_data is None:
            self._form_data = {}
        return self._form_data

    def _get_json_body(self) -> dict[str, Any]:
        if self._json_body is not None:
            return self._json_body
        content_type = self._request.headers.get('content-type', '')
        if 'application/json' not in content_type:
            return {}
        try:
            async def _():
                raw = await self._request.body()
                return raw
            # TODO: handle this
            # We can't async here - json body should be loaded via async path
            return {}
        except Exception:
            return {}

    def _get_post_data(self) -> dict[str, Any]:
        return {**self._get_form_data(), **self._get_json_body()}

    def _cache_json_body(self, data: dict[str, Any]) -> None:
        self._json_body = data

    async def _load_body(self) -> None:
        content_type = self._request.headers.get('content-type', '')
        if 'application/json' in content_type:
            try:
                raw = await self._request.body()
                if raw:
                    self._json_body = _json.loads(raw)
            except (_json.JSONDecodeError, Exception):
                self._json_body = {}
        elif 'application/x-www-form-urlencoded' in content_type or 'multipart/form-data' in content_type:
            try:
                form = await self._request.form()
                self._form_data = {k: v for k, v in form.items()}
            except Exception:
                self._form_data = {}
