import logging
from returns.pipeline import is_successful

from ..dto.lifecycle_data import ShutdownRequestData, ShutdownResponseData
from ...facades.app import app
from ....dto.supervisor_request_data import SupervisorRequestData
from ....enums.supervisor_request_kind import SupervisorRequestKind

logger = logging.getLogger(__name__)

class ShutdownAppService:
    async def __call__(self, service: ShutdownRequestData) -> ShutdownResponseData:
        try:
            request = SupervisorRequestData(
                kind=SupervisorRequestKind.SHUTDOWN,
                thread_id=service.id
            )

            if not is_successful(await app().supervisor.enqueue_request(request)):
                raise Exception(f"could queue restart for service ID: {service.id}")

            return ShutdownResponseData(success=True)
        except Exception as exception:
            logger.error(exception)
            return ShutdownResponseData(success=False)

