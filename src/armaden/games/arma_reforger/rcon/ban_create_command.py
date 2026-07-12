from typing import Any

from armaden.framework.classes.rcon_command_arg_spec import RconCommandArgSpec
from armaden.framework.protocols.rcon_command import RconCommandInterface


class BanCreateCommand(RconCommandInterface):
    command_name: str = '#ban'
    description: str = 'Create a ban'
    category: str = 'ban'
    args: list = [
        RconCommandArgSpec(
            name='identifier',
            type=str,
            required=True,
            description='Player identifier',
        ),
        RconCommandArgSpec(
            name='duration_seconds',
            type=int,
            required=True,
            description='Ban duration in seconds',
        ),
        RconCommandArgSpec(
            name='reason',
            type=str,
            required=False,
            default=None,
            description='Optional ban reason',
        ),
    ]

    async def execute(self, **kwargs: Any) -> Any:
        args = [
            'create',
            str(kwargs['identifier']),
            str(kwargs['duration_seconds']),
        ]
        if kwargs.get('reason') is not None:
            args.append(kwargs['reason'])
        response = await self._client.send_command(self.command_name, *args)
        return await self.on_response(response)
