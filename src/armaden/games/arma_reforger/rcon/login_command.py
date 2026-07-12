from armaden.framework.classes.rcon_command_arg_spec import RconCommandArgSpec
from armaden.framework.protocols.rcon_command import RconCommandInterface


class LoginCommand(RconCommandInterface):
    command_name: str = '#login'
    description: str = 'Authenticate as admin with the RCON server'
    category: str = 'auth'
    args: list = [
        RconCommandArgSpec(
            name='password',
            type=str,
            required=True,
            description='Admin password',
        ),
    ]
