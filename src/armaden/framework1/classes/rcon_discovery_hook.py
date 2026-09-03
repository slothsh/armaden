import inspect
import logging

from armaden.framework.classes.instance_container import InstanceContainer
from armaden.framework.classes.rcon_command_repository import RconCommandRepository
from armaden.framework.protocols.discovery_hook import DiscoveryHook
from armaden.framework.protocols.registers_rcon_command import RegistersRconCommand
from armaden.framework.protocols.rcon_command import RconCommandInterface

logger = logging.getLogger(__name__)


_RCON_REGISTRARS_ATTR = '__rcon_registrars__'


class RconDiscoveryHook:
    def __init__(self, repository: RconCommandRepository) -> None:
        self._repository = repository

    def on_discovery_complete(self, classes: list[type], container: InstanceContainer) -> None:
        for cls in classes:
            if not self._is_rcon_command(cls):
                continue
            self._register_rcon_command(cls, container)

    def _is_rcon_command(self, cls: type) -> bool:
        if not inspect.isclass(cls):
            return False
        try:
            if not issubclass(cls, RconCommandInterface):
                return False
        except TypeError:
            return False
        return hasattr(cls, _RCON_REGISTRARS_ATTR)

    def _register_rcon_command(self, cmd_cls: type, container: InstanceContainer) -> None:
        registrars = getattr(cmd_cls, _RCON_REGISTRARS_ATTR, None)
        if not registrars:
            logger.warning("RCON command [%s] has no registrars declared, skipping", cmd_cls.__name__)
            return

        for registrar_cls in registrars:
            if not container.bound(registrar_cls):
                logger.warning(
                    "Registrar [%s] for RCON command [%s] is not bound in the container, skipping",
                    getattr(registrar_cls, '__name__', registrar_cls),
                    cmd_cls.__name__,
                )
                continue

            try:
                registrar = container.make(registrar_cls)
            except Exception as exc:
                logger.warning(
                    "Failed to resolve registrar [%s] for RCON command [%s]: %s",
                    getattr(registrar_cls, '__name__', registrar_cls),
                    cmd_cls.__name__,
                    exc,
                )
                continue

            if not isinstance(registrar, RegistersRconCommand):
                logger.warning(
                    "Registrar [%s] for RCON command [%s] does not implement RegistersRconCommand, skipping",
                    type(registrar).__name__,
                    cmd_cls.__name__,
                )
                continue

            client = registrar.client
            if client is None:
                logger.warning(
                    "Registrar [%s] has no RCON client available for RCON command [%s]; "
                    "command will be registered with a pending client binding",
                    type(registrar).__name__,
                    cmd_cls.__name__,
                )

            try:
                command_instance = cmd_cls(client=client)
            except Exception as exc:
                logger.warning(
                    "Failed to instantiate RCON command [%s]: %s",
                    cmd_cls.__name__,
                    exc,
                )
                continue

            self._repository.register(command_instance, registrar=registrar_cls)
            logger.info(
                "Registered RCON command [%s] ('%s') with registrar [%s]",
                cmd_cls.__name__,
                getattr(command_instance, 'command_name', cmd_cls.__name__),
                type(registrar).__name__,
            )
