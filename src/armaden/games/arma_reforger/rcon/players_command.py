from armaden.framework.protocols.rcon_command import RconCommandInterface


class PlayersCommand(RconCommandInterface):
    command_name: str = '#players'
    description: str = 'List connected players'
    category: str = 'info'
    args: list = []
