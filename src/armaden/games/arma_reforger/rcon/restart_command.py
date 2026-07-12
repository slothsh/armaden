from armaden.framework.protocols.rcon_command import RconCommandInterface


class RestartCommand(RconCommandInterface):
    command_name: str = '#restart'
    description: str = 'Restart the Arma Reforger server'
    category: str = 'server'
    args: list = []
