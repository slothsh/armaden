from typing import Any

from starlette.responses import JSONResponse as StarletteJSONResponse


class JSONResponse(StarletteJSONResponse):
    pass


class ResponseFactory:
    def json(
        self,
        data: Any,
        status: int = 200,
        headers: dict[str, str] | None = None,
    ) -> JSONResponse:
        return JSONResponse(content=data, status_code=status, headers=headers)

    def no_content(self, headers: dict[str, str] | None = None) -> JSONResponse:
        return JSONResponse(content=None, status_code=204, headers=headers)

    def make(
        self,
        data: Any,
        status: int = 200,
        headers: dict[str, str] | None = None,
    ) -> JSONResponse:
        return JSONResponse(content=data, status_code=status, headers=headers)


_response_factory = ResponseFactory()


def response() -> ResponseFactory:
    return _response_factory


def json_response(data: Any, status: int = 200) -> JSONResponse:
    return JSONResponse(content=data, status_code=status)