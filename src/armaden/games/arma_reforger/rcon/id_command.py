from armaden.framework.protocols.rcon_command import RconCommandInterface


class IdCommand(RconCommandInterface):
    command_name: str = '#id'
    description: str = 'Get the server ID'
    category: str = 'info'
    args: list = []
