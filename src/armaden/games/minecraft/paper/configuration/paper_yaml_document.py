from __future__ import annotations

from copy import deepcopy
from enum import StrEnum
from io import StringIO
from pathlib import Path
from typing import TypeGuard, cast, final

from returns.pipeline import is_successful
from returns.result import Failure, Success
from ruamel.yaml import YAML
from ruamel.yaml.error import YAMLError

from armaden.framework.api.error import Error
from armaden.framework.types.result import Result

type YamlValue = str | int | float | bool | list[YamlValue] | dict[str, YamlValue] | None
type YamlMapping = dict[str, YamlValue]


def _is_yaml_value(value: object) -> TypeGuard[YamlValue]:
    if value is None or isinstance(value, (str, int, float, bool)):
        return True

    if isinstance(value, list):
        items = cast(list[object], value)
        return all(_is_yaml_value(item) for item in items)

    if isinstance(value, dict):
        entries = cast(dict[object, object], value)
        return all(
            isinstance(key, str) and _is_yaml_value(item)
            for key, item in entries.items()
        )

    return False


def _is_yaml_mapping(value: object) -> TypeGuard[YamlMapping]:
    return _is_yaml_value(value) and isinstance(value, dict)


def _merge_into(document: YamlMapping, updates: YamlMapping) -> None:
    for key, value in updates.items():
        existing = document.get(key)

        if isinstance(value, dict) and value and isinstance(existing, dict):
            _merge_into(existing, value)
            continue

        document[key] = deepcopy(value)


@final
class PaperYamlDocument:
    def __init__(self, path: Path) -> None:
        self._path: Path = path
        self._yaml = YAML(typ='rt')
        self._yaml.preserve_quotes = True
        self._yaml.width = 10**6
        self._yaml.allow_unicode = True


    def exists(self) -> bool:
        return self._path.exists()


    def read(self) -> Result[YamlMapping | None]:
        if not self._path.exists():
            return Success(None)

        if not is_successful(raw := self._read_text()):
            return raw.map(lambda _: None)

        return self._load(raw.unwrap())


    def apply(self, updates: YamlMapping) -> Result[None]:
        if not updates:
            return Success(None)

        if not self._path.exists():
            return self.write(deepcopy(updates))

        if not is_successful(raw := self._read_text()):
            return raw.map(lambda _: None)

        if not is_successful(loaded := self._load(raw.unwrap())):
            return loaded.map(lambda _: None)

        document = loaded.unwrap()
        _merge_into(document, updates)
        return self._write_dump(document)


    def write(self, tree: YamlMapping) -> Result[None]:
        return self._write_dump(deepcopy(tree))


    def _load(self, raw: str) -> Result[YamlMapping]:
        try:
            loaded: object = self._yaml.load(raw)
        except YAMLError as failure:
            return Failure(
                Error(
                    PaperYamlDocumentError.INVALID_DOCUMENT,
                    details={'path': str(self._path), 'error': str(failure)},
                )
            )

        if loaded is None:
            return Success({})

        if not _is_yaml_mapping(loaded):
            return Failure(
                Error(
                    PaperYamlDocumentError.INVALID_DOCUMENT,
                    details={'path': str(self._path), 'error': 'the document root must be a mapping'},
                )
            )

        return Success(loaded)


    def _read_text(self) -> Result[str]:
        try:
            return Success(self._path.read_text(encoding='utf-8'))
        except OSError as failure:
            return Failure(
                Error(
                    PaperYamlDocumentError.READ_FAILED,
                    details={'path': str(self._path), 'error': str(failure)},
                )
            )


    def _write_dump(self, tree: YamlMapping) -> Result[None]:
        stream = StringIO()
        self._yaml.dump(tree, stream)
        return self._write_text(stream.getvalue())


    def _write_text(self, text: str) -> Result[None]:
        try:
            _ = self._path.parent.mkdir(parents=True, exist_ok=True)
            _ = self._path.write_text(text, encoding='utf-8')
        except OSError as failure:
            return Failure(
                Error(
                    PaperYamlDocumentError.WRITE_FAILED,
                    details={'path': str(self._path), 'error': str(failure)},
                )
            )

        return Success(None)


# --- Internal Types ----------------------------------------------------------

class PaperYamlDocumentError(StrEnum):
    INVALID_DOCUMENT = 'the yaml document could not be parsed as a paper configuration mapping'
    READ_FAILED = 'the yaml document could not be read'
    WRITE_FAILED = 'the yaml document could not be written'
