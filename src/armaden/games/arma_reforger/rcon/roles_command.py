from armaden.framework.protocols.rcon_command import RconCommandInterface


class RolesCommand(RconCommandInterface):
    command_name: str = '#roles'
    description: str = 'List available roles'
    category: str = 'info'
    args: list = []
