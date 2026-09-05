from armaden.framework.api.rcon.dto.rcon_command_argument_data import RconCommandArgumentData
from armaden.framework.api.rcon import RconCommand


class RestartCommand(RconCommand):
    command_name: str = '#restart'
    description: str = 'Restart the Arma Reforger server'
    category: str = 'server'
    args: list[RconCommandArgumentData] = []
