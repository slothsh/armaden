from armaden.framework.api.rcon.dto.rcon_command_argument_data import RconCommandArgumentData
from armaden.framework.api.rcon import RconCommand


class PlayersCommand(RconCommand):
    command_name: str = '#players'
    description: str = 'List connected players'
    category: str = 'info'
    args: list[RconCommandArgumentData] = []
