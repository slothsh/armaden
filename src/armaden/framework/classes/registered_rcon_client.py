from __future__ import annotations

import asyncio
import logging
from typing import TYPE_CHECKING, cast

from armaden.framework.classes.rcon_command_repository import RconCommandRepository
from armaden.framework.errors import RconCommandArgumentError
from armaden.framework.protocols.rcon_command import SendCommandProtocol

if TYPE_CHECKING:
    from armaden.framework.protocols.rcon_command import RconCommandInterface
    from armaden.network.rcon.battle_eye.battle_eye_rcon_client import CommandResponse

logger = logging.getLogger(__name__)


class RegisteredRconClient:
    """Mixin adding registered RCON command dispatch to any client that
    exposes a ``send_command(command, *args) -> Future[CommandResponse]``
    method (e.g. ``BattleEyeRconClient``).

    Combine with a concrete transport client via cooperative multiple
    inheritance. ``__init__`` extracts the optional ``repository`` and
    ``builtin_command_overrides`` keywords and forwards every other
    argument to the next class in the MRO.

    Subclasses populate ``BUILTIN_COMMAND_CLASSES`` with the built-in
    command classes appropriate to their game/protocol; those commands
    are instantiated and registered automatically at construction time.
    """

    BUILTIN_COMMAND_CLASSES: list[type[RconCommandInterface]] = []

    def __init__(
        self,
        *args,
        repository: RconCommandRepository | None = None,
        builtin_command_overrides: list[type[RconCommandInterface]] | None = None,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)
        self._repository: RconCommandRepository | None = repository
        self._registered_commands: dict[str, RconCommandInterface] = {}
        self._register_builtin_commands(builtin_command_overrides or [])

    @property
    def client(self) -> SendCommandProtocol:
        return cast(SendCommandProtocol, self)

    def register_rcon_command(self, command: RconCommandInterface) -> None:
        if self._repository is not None:
            self._repository.register(command)
        else:
            self._registered_commands[command.command_name] = command
        logger.info("Registered RCON command '%s' (category: %s)", command.command_name, command.category)

    def dispatch_registered_command(self, command_name: str, **kwargs) -> asyncio.Future[CommandResponse]:
        command = (
            self._repository.get(command_name)
            if self._repository is not None
            else self._registered_commands.get(command_name)
        )
        if command is None:
            return self._failed_future(KeyError(f"No registered RCON command '{command_name}'"))

        try:
            validated_kwargs, errors = command.validate(**kwargs)
        except Exception as exc:
            return self._failed_future(exc)

        if errors:
            return self._failed_future(RconCommandArgumentError(command_name, validated_kwargs, errors))

        return asyncio.ensure_future(command.execute(**validated_kwargs))

    def _register_builtin_commands(self, overrides: list[type[RconCommandInterface]]) -> None:
        overrides_by_name = {cls.command_name: cls for cls in overrides}
        builtin_names = {cls.command_name for cls in self.BUILTIN_COMMAND_CLASSES}

        for cls in self.BUILTIN_COMMAND_CLASSES:
            selected_cls = overrides_by_name.get(cls.command_name, cls)
            command = selected_cls(client=cast(SendCommandProtocol, self))
            self.register_rcon_command(command)
            logger.info(
                "Registered built-in RCON command '%s' (%s)%s",
                command.command_name,
                selected_cls.__name__,
                f" via override {selected_cls.__name__}" if selected_cls is not cls else "",
            )

        unrecognized = set(overrides_by_name) - builtin_names
        for name in unrecognized:
            logger.warning(
                "Unrecognized builtin_command_overrides entry '%s' — no built-in command "
                "with that name; override ignored",
                name,
            )

    def _failed_future(self, exception: Exception) -> asyncio.Future[CommandResponse]:
        loop = asyncio.get_running_loop()
        future: asyncio.Future[CommandResponse] = loop.create_future()
        future.set_exception(exception)
        return future
