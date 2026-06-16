from typing import Dict
from pydantic import Extra
from pydantic.dataclasses import dataclass

from framework.enums.health_status import HealthStatus

# -- Response Data ------------------------------------------------------------

@dataclass(config={'extra': 'allow'})
class HealthResponseData:
    status: HealthStatus
    services: Dict[str, Dict[str, ServiceHealthData]]


# -- Internal Data ------------------------------------------------------------

@dataclass(config={'extra': 'allow'})
class ServiceHealthData:
    status: HealthStatus
