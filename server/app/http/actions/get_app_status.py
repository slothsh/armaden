from app.http.dto.lifecycle_data import HealthResponseData
from framework.enums.health_status import HealthStatus
from framework.facades.app import app


class GetAppStatus:
    async def __call__(self) -> HealthResponseData:
        try:
            result = await app().status()
            return HealthResponseData(status=result['status'], services=result['services'])
        except:
            return HealthResponseData(status=HealthStatus.UNKOWN, services={})
