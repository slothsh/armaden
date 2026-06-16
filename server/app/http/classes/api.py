from typing import Any

from app.http.dto.api_data import ApiResponseData
from app.http.enums.api_status import ApiStatus


class Api:
    @classmethod
    def success(cls, message: str | None = None, data: Any | None = None) -> ApiResponseData:
        return ApiResponseData(
            status=ApiStatus.OK,
            message=message,
            data=data,
        )


    @classmethod
    def error(cls, message: str | None = None, data: Any | None = None) -> ApiResponseData:
        return ApiResponseData(
            status=ApiStatus.ERROR,
            message=message,
            data=data,
        )
