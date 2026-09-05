from __future__ import annotations

import logging
from abc import ABC
from collections.abc import Awaitable
from typing import override

from armaden.framework.api.rcon.dto.rcon_command_argument_data import (
    RconCommandArgumentData,
)
from armaden.framework.api.rcon.tags.rcon_missing_argument_tag import (
    RCON_MISSING_ARGUMENT,
)
from armaden.framework.protocols.rcon_command_protocol import RconCommandProtocol
from armaden.framework.protocols.rcon_send_command_protocol import RconSendCommandProtocol

logger = logging.getLogger(__name__)


class RconCommand(RconCommandProtocol, ABC):
    args: list[RconCommandArgumentData] = []
    category: str = 'custom'
    command_name: str
    description: str

    def __init__(self, client: RconSendCommandProtocol) -> None:
        self._client: RconSendCommandProtocol = client


    def __call__(self, **kwargs: object) -> Awaitable[object]:
        return self.execute(**kwargs)


    @override
    async def execute(self, **kwargs: object) -> object:
        positional = [
            kwargs[argument.name]
            for argument in self.args
            if argument.name in kwargs
        ]
        values = [str(value) for value in positional]
        response = await self._client.send_command(self.command_name, *values)
        return await self.on_response(response)


    @override
    async def on_response(self, response: object) -> object:
        return response


    @override
    def validate(self, **kwargs: object) -> tuple[dict[str, object], list[str]]:
        errors: list[str] = []
        validated: dict[str, object] = dict(kwargs)
        declared = {argument.name for argument in self.args}

        for argument in self.args:
            if argument.name in validated:
                value = validated[argument.name]
                expected_type = argument.type
                if expected_type is not None and not isinstance(value, expected_type):
                    errors.append(f"Argument '{argument.name}' for command '{self.command_name}' expected type {expected_type.__name__}, got {type(value).__name__}")
                continue

            if argument.required:
                errors.append(
                    f"Required argument '{argument.name}' for command '{self.command_name}' is missing"
                )
                continue

            if argument.default is RCON_MISSING_ARGUMENT:
                errors.append(f"Optional argument '{argument.name}' for command '{self.command_name}' has no default value and was not provided")
                continue

            validated[argument.name] = argument.default

        for extra in set(validated) - declared:
            logger.warning(
                "RCON command '%s' received undeclared argument '%s'; passing through",
                self.command_name,
                extra,
            )

        return validated, errors


__all__ = [
    'RconCommand',
]
