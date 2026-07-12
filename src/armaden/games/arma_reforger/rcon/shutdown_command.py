from armaden.framework.protocols.rcon_command import RconCommandInterface


class ShutdownCommand(RconCommandInterface):
    command_name: str = '#shutdown'
    description: str = 'Shutdown the Arma Reforger server'
    category: str = 'server'
    args: list = []
