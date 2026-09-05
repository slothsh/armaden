from armaden.framework.protocols.service_provider_protocol import ServiceProviderProtocol
from app.providers.app_service_provider import AppServiceProvider
from app.providers.telemetry_service_provider import TelemetryServiceProvider


def providers() -> list[type[ServiceProviderProtocol]]:
    return [AppServiceProvider, TelemetryServiceProvider]
