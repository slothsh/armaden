import logging
from typing import cast

from returns.pipeline import is_successful

from app.http.enums.api_health_status import ApiHealthStatus
from armaden.framework.protocols.application_protocol import ApplicationProtocol
from armaden.framework.protocols.container_protocol import ContainerProtocol
from armaden.framework.api.supervisor import TaskGraphData
from app.http.dto.lifecycle_data import HealthResponseData

logger = logging.getLogger(__name__)


class GetAppStatus:
    def __init__(self, container: ContainerProtocol) -> None:
        self._application: ApplicationProtocol[TaskGraphData] = cast(
            ApplicationProtocol[TaskGraphData],
            container.make(ApplicationProtocol),
        )


    async def __call__(self) -> HealthResponseData:
        try:
            result = await self._application.status()
            if not is_successful(result):
                raise RuntimeError('Application status was not available')
            values = result.unwrap()
            status_value = values.get('status', ApiHealthStatus.UNKNOWN)
            try:
                status = ApiHealthStatus(str(status_value))
            except ValueError:
                status = ApiHealthStatus.UNKNOWN
            services = values.get('services', {})
            return HealthResponseData(
                status=status,
                services=cast(dict[str, dict[str, object]], services),
            )
        except Exception as exception:
            logger.error(exception)
            return HealthResponseData(status=ApiHealthStatus.UNKNOWN, services={})
