from __future__ import annotations

import asyncio
import logging
from collections.abc import Coroutine
from typing import cast, override

from armaden.framework.api.rcon.exceptions.rcon_command_argument_error import (
    RconCommandArgumentError,
)
from armaden.framework.api.rcon.rcon_command import RconCommand
from armaden.framework.api.rcon.rcon_server_message_handler import RconServerMessageHandler
from armaden.framework.protocols.rcon_server_message_handler_protocol import RconServerMessageHandlerProtocol
from armaden.framework.protocols.registered_rcon_client_protocol import (
    RegisteredRconClientProtocol,
)
from armaden.framework.protocols.rcon_command_protocol import RconCommandProtocol
from armaden.framework.protocols.rcon_command_repository_protocol import (
    RconCommandRepositoryProtocol,
)
from armaden.framework.protocols.rcon_send_command_protocol import RconSendCommandProtocol

logger = logging.getLogger(__name__)


class RegisteredRconClient(RegisteredRconClientProtocol):
    BUILTIN_COMMAND_CLASSES: list[type[RconCommand]] = []
    SERVER_MESSAGE_HANDLERS_CLASSES: list[type[RconServerMessageHandler]] = []

    def _initialize_registered_rcon(
        self,
        repository: RconCommandRepositoryProtocol | None = None,
        builtin_command_overrides: list[type[RconCommand]] | None = None,
        server_message_handler_overrides: list[type[RconServerMessageHandler]] | None = None,
    ) -> None:
        self._loop: asyncio.AbstractEventLoop | None = None
        self._registered_commands: dict[str, RconCommand] = {}
        self._registered_server_messager_handlers: dict[str, RconServerMessageHandler] = {}
        self._repository: RconCommandRepositoryProtocol | None = repository
        self._register_builtin_commands(builtin_command_overrides or [])
        self._register_server_message_handlers(server_message_handler_overrides or [])


    def _register_builtin_commands(self, overrides: list[type[RconCommand]]) -> None:
        overrides_by_name = {command.command_name: command for command in overrides}
        builtin_names = {
            command.command_name for command in self.BUILTIN_COMMAND_CLASSES
        }
        for command_type in self.BUILTIN_COMMAND_CLASSES:
            selected_type = overrides_by_name.get(
                command_type.command_name,
                command_type,
            )
            command = selected_type(client=self.client)
            self.register_rcon_command(command)
        for name in set(overrides_by_name) - builtin_names:
            logger.warning(
                "Unrecognized builtin_command_overrides entry '%s'",
                name,
            )


    def _register_server_message_handlers(self, overrides: list[type[RconServerMessageHandler]]) -> None:
        overrides_by_name = {handler.name: handler for handler in overrides}
        builtin_names = {
            handler.name for handler in self.SERVER_MESSAGE_HANDLERS_CLASSES
        }
        for handler_type in self.SERVER_MESSAGE_HANDLERS_CLASSES:
            selected_type = overrides_by_name.get(
                handler_type.name,
                handler_type,
            )
            handler = selected_type()
            self.register_rcon_server_message_handler(handler)
        for name in set(overrides_by_name) - builtin_names:
            logger.warning(
                "Unrecognized server_message_handler_overrides entry '%s'",
                name,
            )


    async def _run_on_rcon_loop(self, coroutine: Coroutine[object, object, object]) -> object:
        if self._loop is not None and self._loop is not asyncio.get_running_loop():
            future = asyncio.run_coroutine_threadsafe(coroutine, self._loop)
            return await asyncio.wrap_future(future)
        return await coroutine


    @property
    @override
    def client(self) -> RconSendCommandProtocol:
        return cast(RconSendCommandProtocol, cast(object, self))


    @override
    async def connect(self) -> None:
        self._loop = asyncio.get_running_loop()
        connect = getattr(super(), 'connect', None)
        if callable(connect):
            result = connect()
            if asyncio.iscoroutine(result):
                await result


    @override
    async def dispatch_command(self, coroutine: Coroutine[object, object, object]) -> object:
        return await self._run_on_rcon_loop(coroutine)


    @override
    async def dispatch_registered_command(
        self,
        command_name: str,
        **kwargs: object,
    ) -> object:
        command = (
            self._repository.get(command_name)
            if self._repository is not None
            else self._registered_commands.get(command_name)
        )
        if command is None:
            raise KeyError(f"No registered RCON command '{command_name}'")
        validated, errors = command.validate(**kwargs)
        if errors:
            raise RconCommandArgumentError(command_name, validated, errors)
        return await self._run_on_rcon_loop(command.execute(**validated))


    @override
    def register_rcon_command(self, command: RconCommandProtocol) -> None:
        concrete_command = cast(RconCommand, command)
        if self._repository is not None:
            self._repository.register(concrete_command)
        else:
            self._registered_commands[command.command_name] = concrete_command
        logger.info(
            "Registered RCON command '%s' (category: %s)",
            command.command_name,
            command.category,
        )


    @override
    def register_rcon_server_message_handler(self, handler: RconServerMessageHandlerProtocol) -> None:
        concrete_handler = cast(RconServerMessageHandler, handler)
        self._registered_server_messager_handlers[handler.name] = concrete_handler
        logger.info(
            "Registered RCON server message handler '%s' (category: %s)",
            handler.name,
            handler.category
        )


__all__ = [
    'RegisteredRconClient',
]
