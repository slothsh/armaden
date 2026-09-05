import logging

from armaden.framework.api.http import HttpController
from app.http.actions.get_app_status import GetAppStatus
from app.http.actions.restart_app_service import RestartAppService
from app.http.actions.shutdown_app_service import ShutdownAppService
from app.http.classes.api import Api
from app.http.dto.api_data import ApiResponseData
from app.http.dto.lifecycle_data import RestartRequestData, ShutdownRequestData

logger = logging.getLogger(__name__)


class LifecycleController(HttpController):
    def __init__(
        self,
        get_app_status: GetAppStatus,
        restart_app_service: RestartAppService,
        shutdown_app_service: ShutdownAppService,
    ) -> None:
        self._get_app_status: GetAppStatus = get_app_status
        self._restart_app_service: RestartAppService = restart_app_service
        self._shutdown_app_service: ShutdownAppService = shutdown_app_service

    async def health(self) -> ApiResponseData:
        return Api.success(data=await self._get_app_status())

    async def restart(self, service: RestartRequestData) -> ApiResponseData:
        return Api.success(data=await self._restart_app_service(service))

    async def shutdown(self, service: ShutdownRequestData) -> ApiResponseData:
        return Api.success(data=await self._shutdown_app_service(service))