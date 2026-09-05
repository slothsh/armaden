from armaden.framework.api.rcon.dto.rcon_command_argument_data import RconCommandArgumentData
from armaden.framework.api.rcon import RconCommand


class LoginCommand(RconCommand):
    command_name: str = '#login'
    description: str = 'Authenticate as admin with the RCON server'
    category: str = 'auth'
    args: list[RconCommandArgumentData] = [
        RconCommandArgumentData(
            name='password',
            type=str,
            required=True,
            description='Admin password',
        ),
    ]
