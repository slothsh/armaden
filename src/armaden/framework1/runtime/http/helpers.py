from .request_context import RequestContext
from .response import response, json_response


def request():
    return RequestContext.get_request()


def auth():
    req = RequestContext.get_request()
    if req is not None:
        return req.user()
    return None


__all__ = [
    'auth',
    'request',
    'response',
    'json_response',
]
