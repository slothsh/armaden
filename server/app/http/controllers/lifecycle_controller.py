import logging
from fastapi import Depends
from app.http.actions.get_app_status import GetAppStatus
from app.http.actions.restart_app_service import RestartAppService
from app.http.classes.api import Api
from app.http.dto.api_data import ApiResponseData
from app.http.dto.lifecycle_data import RestartRequestData

logger = logging.getLogger('app.http.controllers.lifecycle')


class LifecycleController:
    async def health(
        self,
        status: GetAppStatus = Depends(GetAppStatus)
    ) -> ApiResponseData:
        return Api.success(data=await status())


    async def restart(
        self,
        service: RestartRequestData,
        restart_service: RestartAppService = Depends(RestartAppService)
    ) -> ApiResponseData:
        return Api.success(data=await restart_service(service))

