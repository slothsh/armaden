import logging
from typing import List, Tuple

from returns.pipeline import is_successful
from returns.result import Success, Failure
from enum import StrEnum

from framework.protocols.error import ErrorInterface

from ..errors.error import Error
from ..protocols.service import ServiceInterface
from ..utils.types import Result

logger = logging.getLogger(__name__)


class ServiceManager:
    def __init__(self) -> None:
        self._declared_services: List[ServiceInterface] = []
        self._failed_services: List[Tuple[ErrorInterface, ServiceInterface]] = []
        self._successul_services: List[ServiceInterface] = []


    async def initialize(self) -> Result[None]:
        for service in self._declared_services:
            if not is_successful(result := service()):
                self._successul_services.append(service)
            else:
                self._failed_services.append((result.failure(), service))

        if self._failed_services:
            logger.error('%s services failed to initialize', len(self._failed_services))
            logger.error('Failed services:')
            errors = [error for error in self._failed_services]
            for error in errors:
                logger.error('%4s', error)
            return Failure(Error(ServiceManagerError.INITIALIZATION_FAILED, details={
                'failed': errors
            }))

        return Success(None)


    def add_service(self, service: ServiceInterface) -> Result[None]:
        self._declared_services.append(service)
        return Success(None)


    def add_services(self, services: List[ServiceInterface]) -> Result[None]:
        self._declared_services.extend(services)
        return Success(None)


    @property
    def services(self) -> List[ServiceInterface]:
        return self._declared_services


# -- Intneral Types -------------------------------------------------------

class ServiceManagerError(StrEnum):
    INITIALIZATION_FAILED = 'the service manager failed to successfully initialize'
