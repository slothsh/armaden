from typing import List

from armaden.framework.classes.service_provider import ServiceProvider
from app.providers.app_service_provider import AppServiceProvider
from app.providers.telemetry_service_provider import TelemetryServiceProvider


def providers() -> List[ServiceProvider]:
    return [AppServiceProvider, TelemetryServiceProvider]
