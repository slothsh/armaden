from __future__ import annotations

import asyncio
import logging
from abc import ABC
from typing import TYPE_CHECKING, Any, Protocol, runtime_checkable

from armaden.framework.classes.rcon_command_arg_spec import _MISSING

if TYPE_CHECKING:
    from armaden.framework.classes.rcon_command_arg_spec import RconCommandArgSpec
    from armaden.network.rcon.battle_eye.battle_eye_rcon_client import CommandResponse

logger = logging.getLogger(__name__)


@runtime_checkable
class SendCommandProtocol(Protocol):
    def send_command(self, command: str, *args: str) -> asyncio.Future[CommandResponse]:
        ...


class RconCommandInterface(ABC):
    command_name: str
    description: str
    category: str = 'custom'
    args: list[RconCommandArgSpec] = []

    def __init__(self, client: SendCommandProtocol) -> None:
        self._client = client

    def validate(self, **kwargs: Any) -> tuple[dict[str, Any], list[str]]:
        errors: list[str] = []
        validated: dict[str, Any] = dict(kwargs)

        declared: set[str] = {spec.name for spec in self.args}

        for spec in self.args:
            if spec.name in validated:
                value = validated[spec.name]
                expected_type = spec.type
                if expected_type is not None and expected_type is not Any:
                    try:
                        type_ok = isinstance(value, expected_type)
                    except TypeError:
                        type_ok = True
                    if not type_ok:
                        errors.append(
                            f"Argument '{spec.name}' for command '{self.command_name}' "
                            f"expected type {getattr(expected_type, '__name__', expected_type)}, "
                            f"got {type(value).__name__}"
                        )
                continue

            if spec.required:
                errors.append(
                    f"Required argument '{spec.name}' for command '{self.command_name}' is missing"
                )
                continue

            if spec.default is _MISSING:
                errors.append(
                    f"Optional argument '{spec.name}' for command '{self.command_name}' "
                    f"has no default value and was not provided"
                )
                continue

            validated[spec.name] = spec.default

        for extra in set(validated) - declared:
            logger.warning(
                "RCON command '%s' received undeclared argument '%s'; passing through",
                self.command_name,
                extra,
            )

        return validated, errors

    async def on_response(self, response: CommandResponse) -> Any:
        return response

    def __call__(self, *args: Any) -> Any:
        kwargs = {
            spec.name: value
            for spec, value in zip(self.args, args)
        }
        return self.execute(**kwargs)

    async def execute(self, **kwargs: Any) -> Any:
        positional = [
            kwargs[spec.name]
            for spec in self.args
            if spec.name in kwargs
        ]
        response = await self._client.send_command(self.command_name, *positional)
        return await self.on_response(response)
