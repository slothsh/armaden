from armaden.framework.api.http import (
    HttpRequestContext,
    HttpResponse,
    HttpResponseFactory,
)
from armaden.framework.protocols.http_request_protocol import HttpRequestProtocol


_response_factory = HttpResponseFactory()


def auth() -> object | None:
    return HttpRequestContext.get_request().user()


def json_response(data: object, status: int = 200) -> HttpResponse:
    return _response_factory.json(data, status)


def request() -> HttpRequestProtocol:
    return HttpRequestContext.get_request()


def response() -> HttpResponseFactory:
    return _response_factory


__all__ = [
    'auth',
    'json_response',
    'request',
    'response',
]