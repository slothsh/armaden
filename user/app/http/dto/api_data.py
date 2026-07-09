from typing import Any

from pydantic.dataclasses import dataclass
from ..enums.api_status import ApiStatus


# -- Request Data -------------------------------------------------------------

@dataclass
class ApiResponseData:
    status: ApiStatus
    message: str | None
    data: Any | None