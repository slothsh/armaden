from __future__ import annotations

from abc import ABC, abstractmethod
from copy import deepcopy
from enum import StrEnum
from pathlib import Path
from typing import ClassVar

from returns.pipeline import is_successful
from returns.result import Failure, Success

from armaden.framework.api.error import Error
from armaden.framework.types.result import Result
from armaden.games.minecraft.paper.configuration.paper_yaml_document import (
    PaperYamlDocument,
    YamlMapping,
    YamlValue,
)


def _deep_merge(base: YamlMapping, overrides: YamlMapping) -> YamlMapping:
    merged: YamlMapping = {}

    for key, value in base.items():
        merged[key] = deepcopy(value)

    for key, value in overrides.items():
        existing = merged.get(key)

        if isinstance(existing, dict) and isinstance(value, dict):
            merged[key] = _deep_merge(existing, value)
            continue

        merged[key] = deepcopy(value)

    return merged


def _lookup(tree: YamlMapping | None, path: tuple[str, ...]) -> tuple[bool, YamlValue | None]:
    node: YamlValue = tree

    for key in path:
        if not isinstance(node, dict) or key not in node:
            return False, None

        node = node[key]

    return True, node


class PaperConfigurationFile(ABC):
    FILE_NAME: ClassVar[str]

    def __init__(self, path: Path) -> None:
        self._document: PaperYamlDocument = PaperYamlDocument(path)


    def apply(self, overrides: YamlMapping) -> Result[None]:
        return self._document.apply(overrides)


    def bool_value(self, path: tuple[str, ...]) -> Result[bool | None]:
        if not is_successful(value := self.effective(path)):
            return value.map(lambda _: None)

        unwrapped = value.unwrap()

        if unwrapped is None or isinstance(unwrapped, bool):
            return Success(unwrapped)

        return Failure(self._invalid_value(path, unwrapped, 'bool'))


    @classmethod
    @abstractmethod
    def defaults(cls) -> YamlMapping: ...


    def effective(self, path: tuple[str, ...]) -> Result[YamlValue | None]:
        if not is_successful(tree := self.read()):
            return tree.map(lambda _: None)

        found, value = _lookup(tree.unwrap(), path)

        if found:
            return Success(value)

        has_default, default = _lookup(self.defaults(), path)
        return Success(default if has_default else None)


    def ensure(self, overrides: YamlMapping | None = None) -> Result[None]:
        if self._document.exists():
            return self._document.apply(overrides or {})

        return self._document.write(_deep_merge(self.defaults(), overrides or {}))


    def float_value(self, path: tuple[str, ...]) -> Result[float | None]:
        if not is_successful(value := self.effective(path)):
            return value.map(lambda _: None)

        unwrapped = value.unwrap()

        if unwrapped is None or isinstance(unwrapped, (int, float)) and not isinstance(unwrapped, bool):
            return Success(None if unwrapped is None else float(unwrapped))

        return Failure(self._invalid_value(path, unwrapped, 'float'))


    def int_value(self, path: tuple[str, ...]) -> Result[int | None]:
        if not is_successful(value := self.effective(path)):
            return value.map(lambda _: None)

        unwrapped = value.unwrap()

        if unwrapped is None or isinstance(unwrapped, int) and not isinstance(unwrapped, bool):
            return Success(unwrapped)

        return Failure(self._invalid_value(path, unwrapped, 'int'))


    def list_value(self, path: tuple[str, ...]) -> Result[list[YamlValue] | None]:
        if not is_successful(value := self.effective(path)):
            return value.map(lambda _: None)

        unwrapped = value.unwrap()

        if unwrapped is None or isinstance(unwrapped, list):
            return Success(unwrapped)

        return Failure(self._invalid_value(path, unwrapped, 'list'))


    def mapping_value(self, path: tuple[str, ...]) -> Result[YamlMapping | None]:
        if not is_successful(value := self.effective(path)):
            return value.map(lambda _: None)

        unwrapped = value.unwrap()

        if unwrapped is None or isinstance(unwrapped, dict):
            return Success(unwrapped)

        return Failure(self._invalid_value(path, unwrapped, 'mapping'))


    def read(self) -> Result[YamlMapping | None]:
        return self._document.read()


    def str_value(self, path: tuple[str, ...]) -> Result[str | None]:
        if not is_successful(value := self.effective(path)):
            return value.map(lambda _: None)

        unwrapped = value.unwrap()

        if unwrapped is None or isinstance(unwrapped, str):
            return Success(unwrapped)

        return Failure(self._invalid_value(path, unwrapped, 'str'))


    def _invalid_value(self, path: tuple[str, ...], value: YamlValue, expected: str) -> Error:
        return Error(
            PaperConfigurationFileError.INVALID_VALUE,
            details={'path': list(path), 'value': value, 'expected': expected},
        )


# --- Internal Types ----------------------------------------------------------

class PaperConfigurationFileError(StrEnum):
    INVALID_VALUE = 'the configuration value does not match the requested type'
