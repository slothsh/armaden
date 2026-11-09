from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import cast, final

from returns.pipeline import is_successful
from returns.result import Failure, Success

from armaden.framework.api.error import Error
from armaden.framework.types.result import Result


@final
@dataclass
class PaperArtifactManifestData:
    artifact_path: str = ''
    build: int = 0
    build_policy: str = ''
    channel: str = ''
    name: str = ''
    sha256: str = ''
    size: int = 0
    time: str = ''
    url: str = ''
    version: str = ''


    @classmethod
    def from_mapping(cls, payload: object) -> Result[PaperArtifactManifestData]:
        document = _mapping(payload)

        if document is None:
            return Failure(Error(PaperArtifactManifestError.INVALID, details={'payload': payload}))

        artifact_path = _string(document, 'artifact_path')
        build = _integer(document, 'build')
        build_policy = _string(document, 'build_policy')
        channel = _string(document, 'channel')
        name = _string(document, 'name')
        sha256 = _string(document, 'sha256')
        size = _integer(document, 'size')
        time = _string(document, 'time')
        url = _string(document, 'url')
        version = _string(document, 'version')

        for value in (
            artifact_path,
            build,
            build_policy,
            channel,
            name,
            sha256,
            size,
            time,
            url,
            version,
        ):
            if not is_successful(value):
                return Failure(value.failure())

        if (
            artifact_path.unwrap() == ''
            or build.unwrap() <= 0
            or build_policy.unwrap() == ''
            or name.unwrap() == ''
            or sha256.unwrap() == ''
            or size.unwrap() <= 0
            or url.unwrap() == ''
            or version.unwrap() == ''
        ):
            return Failure(
                Error(
                    PaperArtifactManifestError.INVALID,
                    details={'reason': 'a required value is missing'},
                )
            )

        return Success(
            PaperArtifactManifestData(
                artifact_path=artifact_path.unwrap(),
                build=build.unwrap(),
                build_policy=build_policy.unwrap(),
                channel=channel.unwrap(),
                name=name.unwrap(),
                sha256=sha256.unwrap(),
                size=size.unwrap(),
                time=time.unwrap(),
                url=url.unwrap(),
                version=version.unwrap(),
            )
        )


    def to_mapping(self) -> dict[str, object]:
        return {
            'artifact_path': self.artifact_path,
            'build': self.build,
            'build_policy': self.build_policy,
            'channel': self.channel,
            'name': self.name,
            'sha256': self.sha256,
            'size': self.size,
            'time': self.time,
            'url': self.url,
            'version': self.version,
        }


# --- Internal Types ----------------------------------------------------------

class PaperArtifactManifestError(StrEnum):
    INVALID = 'the paper artifact manifest is missing or invalid'


def _integer(payload: dict[str, object], key: str) -> Result[int]:
    value = payload.get(key)

    if not isinstance(value, int) or isinstance(value, bool):
        return Failure(Error(PaperArtifactManifestError.INVALID, details={'field': key}))

    return Success(value)


def _mapping(value: object) -> dict[str, object] | None:
    if isinstance(value, dict):
        return cast('dict[str, object]', value)

    return None


def _string(payload: dict[str, object], key: str) -> Result[str]:
    value = payload.get(key)

    if not isinstance(value, str):
        return Failure(Error(PaperArtifactManifestError.INVALID, details={'field': key}))

    return Success(value)
