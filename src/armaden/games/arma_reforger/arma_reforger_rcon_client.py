import logging
from collections.abc import Callable
from typing import cast, final, override

from armaden.framework.api.rcon import (
    RegisteredRconClient,
    RconCommand,
    RconCommandRepositoryProtocol,
)
from armaden.framework.api.rcon.rcon_server_message_handler import RconServerMessageHandler
from armaden.games.arma_reforger.rcon import (
    BanCreateCommand,
    BanListCommand,
    BanRemoveCommand,
    IdCommand,
    KickCommand,
    LoginCommand,
    LogoutCommand,
    PlayersCommand,
    RestartCommand,
    RolesCommand,
    ShutdownCommand,
)
from armaden.games.arma_reforger.rcon.dispatch_event_server_message_handler import DispatchEventServerMessageHandler
from armaden.network.rcon.battle_eye.battle_eye_rcon_client import BattleEyeRconClient, ServerMessage

logger = logging.getLogger(__name__)


@final
class ArmaReforgerRconClient(RegisteredRconClient, BattleEyeRconClient):
    """High-level RCON client for Arma Reforger.

    Command registration, dispatch, argument validation, and built-in
    command auto-registration are inherited from ``RegisteredRconClient``
    (framework layer); the BattleEye transport and wire protocol from
    ``BattleEyeRconClient`` (network layer). This subclass only declares
    which built-in Arma Reforger command classes to auto-register.

    Dispatch built-in commands via ``dispatch_registered_command`` and
    override individuals via ``builtin_command_overrides={'#players': ...}``.
    """

    BUILTIN_COMMAND_CLASSES: list[type[RconCommand]] = [
        LoginCommand,
        LogoutCommand,
        RolesCommand,
        IdCommand,
        PlayersCommand,
        RestartCommand,
        ShutdownCommand,
        KickCommand,
        BanCreateCommand,
        BanRemoveCommand,
        BanListCommand,
    ]

    SERVER_MESSAGE_HANDLERS_CLASSES: list[type[RconServerMessageHandler]] = [
        DispatchEventServerMessageHandler
    ]

    def __init__(
        self,
        *args: object,
        repository: RconCommandRepositoryProtocol | None = None,
        builtin_command_overrides: list[type[RconCommand]] | None = None,
        server_message_handler_overrides: list[type[RconServerMessageHandler]] | None = None,
        **kwargs: object,
    ) -> None:
        initialize_network = cast(Callable[..., object], BattleEyeRconClient.__init__)
        _ = initialize_network(self, *args, **kwargs)
        self._initialize_registered_rcon(repository, builtin_command_overrides, server_message_handler_overrides)
        _ = super().__init__(*args, **kwargs)


    @override
    async def connect(self) -> None:
        await BattleEyeRconClient.connect(self)


    @override
    async def shutdown(self) -> None:
        await BattleEyeRconClient.shutdown(self)

    
    @override
    async def on_server_message(self, message: ServerMessage) -> None:
        await super().on_server_message(message)
        for handler in self._registered_server_messager_handlers.values():
            _ = await handler.handle(message.message)
