from framework.protocols.service import ServiceInterface
from framework.runtime.default_application import DefaultApplication


def api(key: str) -> ApiService | None:
    service = [service for service in DefaultApplication.services() if service.name == key]
    if not service:
        return None
    return service[0]
