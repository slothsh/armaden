import logging

from ..dto.lifecycle_data import HealthResponseData
from armaden.framework.facades import App
from armaden.framework.enums.health_status import HealthStatus

logger = logging.getLogger(__name__)

class GetAppStatus:
    async def __call__(self) -> HealthResponseData:
        try:
            result = await App.status()
            return HealthResponseData(status=result['status'], services=result['services'])
        except Exception as exception:
            logger.error(exception)
            return HealthResponseData(status=HealthStatus.UNKOWN, services={})