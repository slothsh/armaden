import logging
from typing import cast

from returns.pipeline import is_successful

from armaden.framework.protocols.container_protocol import ContainerProtocol
from armaden.framework.api.supervisor import (
    Supervisor,
    SupervisorRequestData,
    SupervisorRequestKind,
)
from armaden.framework.protocols.supervisor_protocol import SupervisorProtocol
from app.http.dto.lifecycle_data import RestartRequestData, RestartResponseData

logger = logging.getLogger(__name__)


class RestartAppService:
    def __init__(self, container: ContainerProtocol) -> None:
        self._supervisor: Supervisor = cast(
            Supervisor,
            container.make(SupervisorProtocol),
        )


    async def __call__(self, service: RestartRequestData) -> RestartResponseData:
        try:
            request = SupervisorRequestData(
                kind=SupervisorRequestKind.RESTART,
                task_id=service.id,
            )

            if not is_successful(await self._supervisor.enqueue_request(request)):
                raise RuntimeError(f'Could not queue restart for service ID: {service.id}')

            return RestartResponseData(success=True)
        except Exception as exception:
            logger.error(exception)
            return RestartResponseData(success=False)
