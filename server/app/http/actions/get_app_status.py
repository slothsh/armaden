import logging
from app.http.dto.lifecycle_data import HealthResponseData
from framework.enums.health_status import HealthStatus
from framework.facades.app import app

logger = logging.getLogger(__name__)

class GetAppStatus:
    async def __call__(self) -> HealthResponseData:
        try:
            result = await app().status()
            return HealthResponseData(status=result['status'], services=result['services'])
        except Exception as exception:
            logger.error(exception)
            return HealthResponseData(status=HealthStatus.UNKOWN, services={})
