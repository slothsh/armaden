from typing import Any

from pydantic.dataclasses import dataclass
from app.http.enums.api_status import ApiStatus


# -- Request Data -------------------------------------------------------------

@dataclass
class ApiResponseData:
    status: ApiStatus
    message: str | None
    data: Any | None
