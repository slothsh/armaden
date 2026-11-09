from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import final

from returns.pipeline import is_successful
from returns.result import Failure, Success

from armaden.framework.api.error import Error
from armaden.framework.types.result import Result
from armaden.games.minecraft.paper.enums import PaperSystemProperty


def _serialize_property_value(value: str | bool) -> Result[str]:
    if value is True:
        return Success('true')

    if value is False:
        return Success('false')

    if value == '':
        return Failure(Error(PaperJvmLaunchError.INVALID_PROPERTY_VALUE, details={'value': value}))

    return Success(value)


@final
@dataclass
class PaperJvmLaunchData:
    initial_memory_mb: int | None = None
    maximum_memory_mb: int | None = None
    options: list[str] = field(default_factory=list)
    system_properties: dict[PaperSystemProperty, str | bool] = field(default_factory=dict)

    def to_tokens(self) -> Result[list[str]]:
        tokens: list[str] = []

        for memory, prefix in (
            (self.initial_memory_mb, '-Xms'),
            (self.maximum_memory_mb, '-Xmx'),
        ):
            if memory is None:
                continue

            if memory <= 0:
                return Failure(Error(PaperJvmLaunchError.INVALID_MEMORY, details={'megabytes': memory}))

            tokens.append(f'{prefix}{memory}M')

        for option in self.options:
            if option == '':
                return Failure(Error(PaperJvmLaunchError.INVALID_OPTION, details={'option': option}))

            tokens.append(option)

        for prop, value in self.system_properties.items():
            if not is_successful(serialized := _serialize_property_value(value)):
                return serialized.map(lambda _: tokens)

            tokens.append(f'-D{prop.value}={serialized.unwrap()}')

        return Success(tokens)


# --- Internal Types ----------------------------------------------------------

class PaperJvmLaunchError(StrEnum):
    INVALID_MEMORY = 'the jvm memory setting must be a positive amount of megabytes'
    INVALID_OPTION = 'the jvm option token is empty'
    INVALID_PROPERTY_VALUE = 'the paper system property value is invalid'
