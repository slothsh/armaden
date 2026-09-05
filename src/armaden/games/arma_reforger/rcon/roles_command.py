from armaden.framework.api.rcon.dto.rcon_command_argument_data import RconCommandArgumentData
from armaden.framework.api.rcon import RconCommand


class RolesCommand(RconCommand):
    command_name: str = '#roles'
    description: str = 'List available roles'
    category: str = 'info'
    args: list[RconCommandArgumentData] = []
