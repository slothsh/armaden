from armaden.framework.protocols.rcon_command import RconCommandInterface


class LoginCommand(RconCommandInterface):
    command_name: str = '#login'
    description: str = 'Authenticate with the RCON server'
    category: str = 'auth'
    args: list = []
