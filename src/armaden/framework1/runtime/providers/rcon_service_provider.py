from returns.result import Success

from armaden.framework.classes.rcon_command_repository import RconCommandRepository
from armaden.framework.classes.rcon_discovery_hook import RconDiscoveryHook
from armaden.framework.classes.service_provider import ServiceProvider
from armaden.framework.runtime.providers.type_discovery_service_provider import DISCOVERY_HOOKS_TAG
from armaden.framework.utils.types import Result


class RconServiceProvider(ServiceProvider):
    name = 'rcon'

    def register(self) -> Result[None]:
        self._container.singleton(RconCommandRepository, RconCommandRepository)
        self._container.tag([RconDiscoveryHook], DISCOVERY_HOOKS_TAG)
        return Success(None)
