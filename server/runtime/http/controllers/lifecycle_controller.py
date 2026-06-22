import logging
from fastapi import Depends
from ..actions.get_app_status import GetAppStatus
from ..actions.restart_app_service import RestartAppService
from ..actions.shutdown_app_service import ShutdownAppService
from ..classes.api import Api
from ..dto.api_data import ApiResponseData
from ..dto.lifecycle_data import RestartRequestData, ShutdownRequestData

logger = logging.getLogger(__name__)


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


    async def shutdown(
        self,
        service: ShutdownRequestData,
        shutdown_service: ShutdownAppService = Depends(ShutdownAppService)
    ) -> ApiResponseData:
        return Api.success(data=await shutdown_service(service))

