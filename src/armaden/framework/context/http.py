from armaden.framework.protocols.http_request_protocol import HttpRequestProtocol
from armaden.framework.runtime.http.http_request_context import HttpRequestContext
from armaden.framework.runtime.http.http_response import HttpResponse
from armaden.framework.runtime.http.http_response_factory import HttpResponseFactory


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