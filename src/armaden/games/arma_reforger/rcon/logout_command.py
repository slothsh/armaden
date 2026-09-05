from armaden.framework.api.rcon.dto.rcon_command_argument_data import RconCommandArgumentData
from armaden.framework.api.rcon import RconCommand


class LogoutCommand(RconCommand):
    command_name: str = '#logout'
    description: str = 'Log out from the RCON server'
    category: str = 'auth'
    args: list[RconCommandArgumentData] = []
