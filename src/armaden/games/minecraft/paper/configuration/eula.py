from __future__ import annotations

from enum import StrEnum
from pathlib import Path
from typing import ClassVar, final

from javaproperties.propfile import PropertiesFile
from returns.pipeline import is_successful
from returns.result import Failure, Success

from armaden.framework.api.error import Error
from armaden.framework.types.result import Result


@final
class EulaFile:
    FILE_NAME: ClassVar[str] = 'eula.txt'

    def __init__(self, path: Path) -> None:
        self._path: Path = path


    def read(self) -> Result[bool | None]:
        if not self._path.exists():
            return Success(None)

        if not is_successful(raw := self._read_text()):
            return Failure(raw.failure())

        if not is_successful(properties := self._parse(raw.unwrap())):
            return Failure(properties.failure())

        consent = properties.unwrap().get('eula')

        if consent is None:
            return Success(None)

        if consent == 'true':
            return Success(True)

        if consent == 'false':
            return Success(False)

        return Failure(
            Error(
                EulaFileError.INVALID_VALUE,
                details={'path': str(self._path), 'value': consent},
            )
        )


    def write(self, accepted: bool) -> Result[None]:
        if not is_successful(properties := self._load_or_empty()):
            return properties.map(lambda _: None)

        properties.unwrap()['eula'] = 'true' if accepted else 'false'
        return self._write(properties.unwrap().dumps())


    def _load_or_empty(self) -> Result[PropertiesFile]:
        if not self._path.exists():
            return Success(PropertiesFile())

        if not is_successful(raw := self._read_text()):
            return Failure(raw.failure())

        return self._parse(raw.unwrap())


    def _parse(self, raw: str) -> Result[PropertiesFile]:
        try:
            return Success(PropertiesFile.loads(raw))
        except ValueError as failure:
            return Failure(
                Error(
                    EulaFileError.INVALID_DOCUMENT,
                    details={'path': str(self._path), 'error': str(failure)},
                )
            )


    def _read_text(self) -> Result[str]:
        try:
            return Success(self._path.read_text(encoding='utf-8'))
        except OSError as failure:
            return Failure(
                Error(
                    EulaFileError.READ_FAILED,
                    details={'path': str(self._path), 'error': str(failure)},
                )
            )


    def _write(self, text: str) -> Result[None]:
        try:
            _ = self._path.parent.mkdir(parents=True, exist_ok=True)
            _ = self._path.write_text(text, encoding='utf-8')
        except OSError as failure:
            return Failure(
                Error(
                    EulaFileError.WRITE_FAILED,
                    details={'path': str(self._path), 'error': str(failure)},
                )
            )

        return Success(None)


# --- Internal Types ----------------------------------------------------------

class EulaFileError(StrEnum):
    INVALID_DOCUMENT = 'the eula.txt file could not be parsed'
    INVALID_VALUE = 'the eula.txt consent value is not true or false'
    READ_FAILED = 'the eula.txt file could not be read'
    WRITE_FAILED = 'the eula.txt file could not be written'
