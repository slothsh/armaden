from .request_context import RequestContext
from .response import response as _response, json_response


def request():
    return RequestContext.get_request()


__all__ = [
    'request',
    'response',
    'json_response',
]