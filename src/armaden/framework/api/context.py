from collections.abc import Mapping

from armaden.framework.api.http import (
    HttpRequestContext,
    HttpResponse,
    HttpResponseFactory,
)
from armaden.framework.facades.cache_facade import CacheFacade
from armaden.framework.facades.database_facade import DatabaseFacade
from armaden.framework.facades.queue_facade import QueueFacade
from armaden.framework.facades.storage_facade import StorageFacade
from armaden.framework.facades.url_facade import UrlFacade
from armaden.framework.protocols.cache_protocol import CacheProtocol
from armaden.framework.protocols.database_resolver_protocol import DatabaseResolverProtocol
from armaden.framework.protocols.database_schema_builder_protocol import DatabaseSchemaBuilderProtocol
from armaden.framework.protocols.filesystem_protocol import FilesystemProtocol
from armaden.framework.protocols.http_request_protocol import HttpRequestProtocol
from armaden.framework.protocols.queue_driver_protocol import QueueDriverProtocol

_response_factory = HttpResponseFactory()


def auth() -> object | None:
    return HttpRequestContext.get_request().user()


def cache() -> CacheProtocol:
    return CacheFacade.store()


def database() -> DatabaseResolverProtocol:
    return DatabaseFacade.connection()


def json_response(data: object, status: int = 200) -> HttpResponse:
    return _response_factory.json(data, status)


def queue() -> QueueDriverProtocol:
    return QueueFacade.connection()


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


def schema(connection: str | None = None) -> DatabaseSchemaBuilderProtocol:
    return DatabaseFacade.schema(connection)


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
    'database',
    'json_response',
    'queue',
    'request',
    'response',
    'route',
    'schema',
    'storage',
    'url',
]
