from typing import Any

from armaden.framework.classes.rcon_command_arg_spec import RconCommandArgSpec
from armaden.framework.protocols.rcon_command import RconCommandInterface


class BanListCommand(RconCommandInterface):
    command_name: str = '#ban'
    description: str = 'List bans'
    category: str = 'ban'
    args: list = [
        RconCommandArgSpec(
            name='page',
            type=int,
            required=False,
            default=None,
            description='Optional page number',
        ),
    ]

    async def execute(self, **kwargs: Any) -> Any:
        if kwargs.get('page') is not None:
            response = await self._client.send_command(
                self.command_name, 'list', str(kwargs['page'])
            )
        else:
            response = await self._client.send_command(self.command_name, 'list')
        return await self.on_response(response)
