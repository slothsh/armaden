from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import cast, final

from returns.pipeline import is_successful
from returns.result import Failure, Success

from armaden.framework.api.error import Error
from armaden.framework.types.result import Result
from armaden.games.minecraft.java.enums import JavaRuntimeSource, TemurinImageType


@final
@dataclass
class JavaRuntimeManifestData:
    architecture: str = ''
    artifact_name: str = ''
    checksum: str = ''
    directory: str = ''
    executable: str = ''
    full_version: str = ''
    image_type: TemurinImageType | None = None
    major: int = 0
    os: str = ''
    selection: str = ''
    source: JavaRuntimeSource = JavaRuntimeSource.MANAGED
    vendor: str = ''


    @classmethod
    def from_mapping(cls, payload: object) -> Result[JavaRuntimeManifestData]:
        document = _mapping(payload)

        if document is None:
            return Failure(Error(JavaRuntimeManifestError.INVALID, details={'payload': payload}))

        architecture = _string(document, 'architecture')
        artifact_name = _string(document, 'artifact_name')
        checksum = _string(document, 'checksum')
        directory = _string(document, 'directory')
        executable = _string(document, 'executable')
        full_version = _string(document, 'full_version')
        major = _integer(document, 'major')
        os_name = _string(document, 'os')
        selection = _string(document, 'selection')
        vendor = _string(document, 'vendor')

        for value in (
            architecture,
            artifact_name,
            checksum,
            directory,
            executable,
            full_version,
            major,
            os_name,
            selection,
            vendor,
        ):
            if not is_successful(value):
                return Failure(value.failure())

        if (
            executable.unwrap() == ''
            or full_version.unwrap() == ''
            or major.unwrap() <= 0
            or selection.unwrap() == ''
        ):
            return Failure(
                Error(
                    JavaRuntimeManifestError.INVALID,
                    details={'reason': 'a required value is missing'},
                )
            )

        source_raw: object | None = document.get('source')
        image_type_raw: object | None = document.get('image_type')

        if not isinstance(source_raw, str):
            return Failure(Error(JavaRuntimeManifestError.INVALID, details={'field': 'source'}))

        try:
            source = JavaRuntimeSource(source_raw)
        except ValueError:
            return Failure(
                Error(JavaRuntimeManifestError.INVALID, details={'field': 'source', 'value': source_raw})
            )

        image_type: TemurinImageType | None = None

        if image_type_raw is not None:
            if not isinstance(image_type_raw, str):
                return Failure(Error(JavaRuntimeManifestError.INVALID, details={'field': 'image_type'}))

            try:
                image_type = TemurinImageType(image_type_raw)
            except ValueError:
                return Failure(
                    Error(
                        JavaRuntimeManifestError.INVALID,
                        details={'field': 'image_type', 'value': image_type_raw},
                    )
                )

        return Success(
            JavaRuntimeManifestData(
                architecture=architecture.unwrap(),
                artifact_name=artifact_name.unwrap(),
                checksum=checksum.unwrap(),
                directory=directory.unwrap(),
                executable=executable.unwrap(),
                full_version=full_version.unwrap(),
                image_type=image_type,
                major=major.unwrap(),
                os=os_name.unwrap(),
                selection=selection.unwrap(),
                source=source,
                vendor=vendor.unwrap(),
            )
        )


    def to_mapping(self) -> dict[str, object]:
        return {
            'architecture': self.architecture,
            'artifact_name': self.artifact_name,
            'checksum': self.checksum,
            'directory': self.directory,
            'executable': self.executable,
            'full_version': self.full_version,
            'image_type': self.image_type.value if self.image_type is not None else None,
            'major': self.major,
            'os': self.os,
            'selection': self.selection,
            'source': self.source.value,
            'vendor': self.vendor,
        }


# --- Internal Types ----------------------------------------------------------

class JavaRuntimeManifestError(StrEnum):
    INVALID = 'the java runtime manifest is missing or invalid'


def _integer(payload: dict[str, object], key: str) -> Result[int]:
    value = payload.get(key)

    if not isinstance(value, int) or isinstance(value, bool):
        return Failure(Error(JavaRuntimeManifestError.INVALID, details={'field': key}))

    return Success(value)


def _mapping(value: object) -> dict[str, object] | None:
    if isinstance(value, dict):
        return cast('dict[str, object]', value)

    return None


def _string(payload: dict[str, object], key: str) -> Result[str]:
    value = payload.get(key)

    if not isinstance(value, str):
        return Failure(Error(JavaRuntimeManifestError.INVALID, details={'field': key}))

    return Success(value)
