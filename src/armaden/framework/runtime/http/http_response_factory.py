from __future__ import annotations

from collections.abc import Mapping
from typing import override

from armaden.framework.protocols.response_factory_protocol import ResponseFactoryProtocol
from armaden.framework.runtime.http.http_response import HttpResponse


class HttpResponseFactory(ResponseFactoryProtocol):
    @override
    def json(
        self,
        data: object,
        status: int = 200,
        headers: Mapping[str, str] | None = None,
    ) -> HttpResponse:
        return HttpResponse(content=data, status_code=status, headers=headers)


    @override
    def make(
        self,
        data: object,
        status: int = 200,
        headers: Mapping[str, str] | None = None,
    ) -> HttpResponse:
        return HttpResponse(content=data, status_code=status, headers=headers)


    @override
    def no_content(self, headers: Mapping[str, str] | None = None) -> HttpResponse:
        return HttpResponse(content=None, status_code=204, headers=headers)
