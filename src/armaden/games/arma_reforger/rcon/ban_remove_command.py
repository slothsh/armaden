from typing import Any

from armaden.framework.classes.rcon_command_arg_spec import RconCommandArgSpec
from armaden.framework.protocols.rcon_command import RconCommandInterface


class BanRemoveCommand(RconCommandInterface):
    command_name: str = '#ban'
    description: str = 'Remove a ban'
    category: str = 'ban'
    args: list = [
        RconCommandArgSpec(
            name='identity_id',
            type=str,
            required=True,
            description='Ban identity ID to remove',
        ),
    ]

    async def execute(self, **kwargs: Any) -> Any:
        response = await self._client.send_command(
            self.command_name, 'remove', str(kwargs['identity_id'])
        )
        return await self.on_response(response)
