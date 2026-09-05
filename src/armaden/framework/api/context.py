from collections.abc import Mapping

from armaden.framework.api.http import (    HttpRequestContext,
    HttpResponse,
    HttpResponseFactory,
)
from armaden.framework.facades.cache_facade import CacheFacade
from armaden.framework.facades.storage_facade import StorageFacade
from armaden.framework.facades.url_facade import UrlFacade
from armaden.framework.protocols.cache_protocol import CacheProtocol
from armaden.framework.protocols.filesystem_protocol import FilesystemProtocol
from armaden.framework.protocols.http_request_protocol import HttpRequestProtocol


_response_factory = HttpResponseFactory()


def auth() -> object | None:
    return HttpRequestContext.get_request().user()


def cache() -> CacheProtocol:
    return CacheFacade.store()


def json_response(data: object, status: int = 200) -> HttpResponse:
    return _response_factory.json(data, status)


def request() -> HttpRequestProtocol:
    return HttpRequestContext.get_request()


def response() -> HttpResponseFactory:
    return _response_factory


def route(
    name: str,
    parameters: Mapping[str, object] | None = None,
    absolute: bool = True,
) -> str:
    return UrlFacade.route(name, parameters, absolute)


def storage() -> FilesystemProtocol:
    return StorageFacade.disk()


def url(
    path: str = '/',
    parameters: Mapping[str, object] | None = None,
) -> str:
    return UrlFacade.to(path, parameters)


__all__ = [
    'auth',
    'cache',
    'json_response',
    'request',
    'response',
    'route',
    'storage',
    'url',
]