import logging
from typing import cast

from returns.pipeline import is_successful

from armaden.framework.protocols.container_protocol import ContainerProtocol
from armaden.framework.protocols.supervisor_protocol import SupervisorProtocol
from armaden.framework.api.supervisor import (
    Supervisor,
    SupervisorRequestData,
    SupervisorRequestKind,
)
from app.http.dto.lifecycle_data import ShutdownRequestData, ShutdownResponseData

logger = logging.getLogger(__name__)


class ShutdownAppService:
    def __init__(self, container: ContainerProtocol) -> None:
        self._supervisor: Supervisor = cast(
            Supervisor,
            container.make(SupervisorProtocol),
        )


    async def __call__(self, service: ShutdownRequestData) -> ShutdownResponseData:
        try:
            request = SupervisorRequestData(
                kind=SupervisorRequestKind.SHUTDOWN,
                task_id=service.id,
            )

            if not is_successful(await self._supervisor.enqueue_request(request)):
                raise RuntimeError(f'Could not queue shutdown for service ID: {service.id}')

            return ShutdownResponseData(success=True)
        except Exception as exception:
            logger.error(exception)
            return ShutdownResponseData(success=False)
