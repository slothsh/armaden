import logging

from armaden.framework.runtime.http.controller import Controller
from ..actions.get_app_status import GetAppStatus
from ..actions.restart_app_service import RestartAppService
from ..actions.shutdown_app_service import ShutdownAppService
from ..classes.api import Api
from ..dto.api_data import ApiResponseData
from ..dto.lifecycle_data import RestartRequestData, ShutdownRequestData

logger = logging.getLogger(__name__)


class LifecycleController(Controller):
    def __init__(
        self,
        get_app_status: GetAppStatus | None = None,
        restart_app_service: RestartAppService | None = None,
        shutdown_app_service: ShutdownAppService | None = None,
    ) -> None:
        self._get_app_status = get_app_status or GetAppStatus()
        self._restart_app_service = restart_app_service or RestartAppService()
        self._shutdown_app_service = shutdown_app_service or ShutdownAppService()

    async def health(self) -> ApiResponseData:
        return Api.success(data=await self._get_app_status())

    async def restart(self, service: RestartRequestData) -> ApiResponseData:
        return Api.success(data=await self._restart_app_service(service))

    async def shutdown(self, service: ShutdownRequestData) -> ApiResponseData:
        return Api.success(data=await self._shutdown_app_service(service))