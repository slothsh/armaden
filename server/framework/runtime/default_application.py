import logging
from typing import Any, Dict, Mapping
from returns.pipeline import is_successful

from framework.enums.health_status import HealthStatus
from framework.utils.dictionary import Dictionary

from .kernel import Kernel
from ..utils.types import Result

logger = logging.getLogger(__name__)


class DefaultApplication(Kernel):
    def __init__(self, handle: DefaultApplication | None = None):
        super().__init__(handle if handle else self, package_name='app')


    async def status(self) -> Mapping[str, Any]:
        def handle_result(results: Dict[str, Result[Dict[str, Any]]]) -> Dict[str, Any]:
            status: Dict[str, Any] = {}

            for name, result in results.items():
                if not is_successful(result):
                    logger.warning(result.failure())
                    status[name] = { 'status': HealthStatus.UNAVAILABLE }
                    continue

                status[name] = result.unwrap()

            return status


        service_statuses = { service.name: handle_result(result) for service in self.service_manager.services for result in await service.status() }
        app_degraded = Dictionary.has('status', lambda value: value != HealthStatus.OK, [
            *service_statuses.values()
        ])

        return {
            'status': HealthStatus.DEGRADED if app_degraded else HealthStatus.OK,
            'services': service_statuses,
        }
