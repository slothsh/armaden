from armaden.framework.api.rcon.dto.rcon_command_argument_data import RconCommandArgumentData
from armaden.framework.api.rcon import RconCommand


class ShutdownCommand(RconCommand):
    command_name: str = '#shutdown'
    description: str = 'Shutdown the Arma Reforger server'
    category: str = 'server'
    args: list[RconCommandArgumentData] = []
