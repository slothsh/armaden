import logging

from armaden.framework.classes.registered_rcon_client import RegisteredRconClient
from armaden.framework.protocols.registers_rcon_command import RegistersRconCommand
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
from armaden.network.rcon.battle_eye.battle_eye_rcon_client import BattleEyeRconClient

logger = logging.getLogger(__name__)


class ArmaReforgerRconClient(RegisteredRconClient, BattleEyeRconClient, RegistersRconCommand):
    """High-level RCON client for Arma Reforger.

    Command registration, dispatch, argument validation, and built-in
    command auto-registration are inherited from ``RegisteredRconClient``
    (framework layer); the BattleEye transport and wire protocol from
    ``BattleEyeRconClient`` (network layer). This subclass only declares
    which built-in Arma Reforger command classes to auto-register.

    Dispatch built-in commands via ``dispatch_registered_command`` and
    override individuals via ``builtin_command_overrides={'#players': ...}``.
    """

    BUILTIN_COMMAND_CLASSES: list = [
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
