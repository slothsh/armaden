from armaden.framework.protocols.rcon_command import RconCommandInterface


class LogoutCommand(RconCommandInterface):
    command_name: str = '#logout'
    description: str = 'Log out from the RCON server'
    category: str = 'auth'
    args: list = []
