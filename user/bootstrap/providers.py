from typing import List

from armaden.framework.classes.service_provider import ServiceProvider
from app.providers.app_service_provider import AppServiceProvider


def providers() -> List[ServiceProvider]:
    return [AppServiceProvider]
