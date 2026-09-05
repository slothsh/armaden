from pydantic.dataclasses import dataclass

from app.http.enums.api_health_status import ApiHealthStatus


@dataclass
class RestartRequestData:
    id: int


@dataclass
class ShutdownRequestData:
    id: int


@dataclass(config={'extra': 'allow'})
class HealthResponseData:
    status: ApiHealthStatus
    services: dict[str, dict[str, object]]


@dataclass(config={'extra': 'allow'})
class RestartResponseData:
    success: bool


@dataclass(config={'extra': 'allow'})
class ShutdownResponseData:
    success: bool


@dataclass(config={'extra': 'allow'})
class ServiceHealthData:
    status: ApiHealthStatus
