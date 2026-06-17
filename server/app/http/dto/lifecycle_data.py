from typing import Dict
from pydantic.dataclasses import dataclass

from framework.enums.health_status import HealthStatus
# -- Request Data -------------------------------------------------------------

@dataclass
class RestartRequestData:
    id: int


@dataclass
class ShutdownRequestData:
    id: int


# -- Response Data ------------------------------------------------------------

@dataclass(config={'extra': 'allow'})
class HealthResponseData:
    status: HealthStatus
    services: Dict[str, Dict[str, ServiceHealthData]]


@dataclass(config={'extra': 'allow'})
class RestartResponseData:
    success: bool


@dataclass(config={'extra': 'allow'})
class ShutdownResponseData:
    success: bool


# -- Internal Data ------------------------------------------------------------

@dataclass(config={'extra': 'allow'})
class ServiceHealthData:
    status: HealthStatus
