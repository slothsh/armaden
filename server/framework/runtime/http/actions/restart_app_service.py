import logging
from returns.pipeline import is_successful

from ..dto.lifecycle_data import RestartRequestData, RestartResponseData
from ...facades.app import app
from ....dto.supervisor_request_data import SupervisorRequestData
from ....enums.supervisor_request_kind import SupervisorRequestKind

logger = logging.getLogger(__name__)

class RestartAppService:
    async def __call__(self, service: RestartRequestData) -> RestartResponseData:
        try:
            request = SupervisorRequestData(
                kind=SupervisorRequestKind.RESTART,
                thread_id=service.id
            )

            if not is_successful(await app().supervisor.enqueue_request(request)):
                raise Exception(f"could queue restart for service ID: {service.id}")

            return RestartResponseData(success=True)
        except Exception as exception:
            logger.error(exception)
            return RestartResponseData(success=False)

