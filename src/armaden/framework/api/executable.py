from __future__ import annotations

from abc import ABC
from collections.abc import Callable
from pathlib import Path
from typing import Self, override

from armaden.framework.protocols.executable_protocol import (
    ExecutableProtocol,
    PushValue,
)
from armaden.framework.types.result import Result


class Executable(ExecutableProtocol, ABC):
    def __init__(
        self,
        resolve_executable: Callable[[], Result[Path]] | None = None,
    ) -> None:
        self._params: list[str] = []
        self._scratch_params: list[str] = []
        self._executable: Path | None = None
        if resolve_executable is not None:
            self._executable = resolve_executable().value_or(None)


    def _serialize_value(self, value: PushValue) -> str | None:
        if value == '':
            return None
        if isinstance(value, bool):
            return 'true' if value else 'false'
        if isinstance(value, list):
            parts: list[str] = []
            for item in value:
                serialized = self._serialize_value(item)
                if serialized is not None:
                    parts.append(serialized)
            return ','.join(parts) if parts else None
        if isinstance(value, Path):
            return str(value)
        return str(value)


    @override
    def build_argv(self) -> list[str]:
        return [str(self._executable), *self._params]


    @override
    def clear_params(self) -> Self:
        self.reset_params()
        return self


    @override
    def consume_argv(self) -> list[str]:
        argv = self.build_argv()
        self.reset_params()
        return argv


    @override
    def push(self, flag: str, *values: PushValue) -> None:
        truthy_values: list[str] = []
        for value in values:
            serialized = self._serialize_value(value)
            if serialized is not None:
                truthy_values.append(serialized)
        if values and not truthy_values:
            return
        self._params.append(flag)
        self._params.extend(truthy_values)


    @override
    def reset_params(self) -> None:
        self._params.clear()


    @override
    def restore_params(self) -> None:
        self._params = self._scratch_params
        self._scratch_params = []


    @override
    def save_params(self) -> Self:
        self._scratch_params = list(self._params)
        self._params.clear()
        return self


__all__ = [
    'Executable',
    'PushValue',
]
