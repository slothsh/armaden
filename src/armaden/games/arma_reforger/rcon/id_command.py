from armaden.framework.api.rcon.dto.rcon_command_argument_data import RconCommandArgumentData
from armaden.framework.api.rcon import RconCommand


class IdCommand(RconCommand):
    command_name: str = '#id'
    description: str = 'Get the server ID'
    category: str = 'info'
    args: list[RconCommandArgumentData] = []
