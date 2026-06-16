from returns.pipeline import is_successful

from app.http.dto.lifecycle_data import RestartRequestData, RestartResponseData
from framework.facades.app import app


class RestartAppService:
    async def __call__(self, service: RestartRequestData) -> RestartResponseData:
        try:
            if not is_successful(await app().supervisor.queue_restart(service.id)):
                raise Exception(f"could queue restart for service ID: {service.id}")
            return RestartResponseData(success=True)
        except:
            return RestartResponseData(success=False)

