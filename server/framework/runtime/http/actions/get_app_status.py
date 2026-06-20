import logging

from ..dto.lifecycle_data import HealthResponseData
from ...facades.app import app
from ....enums.health_status import HealthStatus

logger = logging.getLogger(__name__)

class GetAppStatus:
    async def __call__(self) -> HealthResponseData:
        try:
            result = await app().status()
            return HealthResponseData(status=result['status'], services=result['services'])
        except Exception as exception:
            logger.error(exception)
            return HealthResponseData(status=HealthStatus.UNKOWN, services={})
