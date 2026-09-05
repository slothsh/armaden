from __future__ import annotations

from starlette.responses import JSONResponse as StarletteJSONResponse


class HttpResponse(StarletteJSONResponse):
    pass
