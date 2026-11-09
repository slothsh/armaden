from __future__ import annotations

from enum import StrEnum
from typing import cast, final, override

from returns.pipeline import is_successful
from returns.result import Failure, Success

from armaden.framework.api.error import Error
from armaden.framework.types.result import Result
from armaden.network.http.protocols.http_transport_protocol import (
    HttpTransportProtocol,
)
from armaden.games.minecraft.java.dto import (
    TemurinBinaryData,
    TemurinPlatformData,
    TemurinReleaseData,
)
from armaden.games.minecraft.java.enums import TemurinImageType
from armaden.games.minecraft.java.protocols import TemurinCatalogProtocol

_ADOPTIUM_LATEST_URL = 'https://api.adoptium.net/v3/assets/latest/{major}/{implementation}'
_JVM_IMPL = 'hotspot'
_VENDOR = 'eclipse'


@final
class AdoptiumTemurinCatalog(TemurinCatalogProtocol):
    def __init__(self, transport: HttpTransportProtocol) -> None:
        self._transport: HttpTransportProtocol = transport


    @override
    async def latest_release(
        self,
        image_type: TemurinImageType,
        major: int,
        platform: TemurinPlatformData,
    ) -> Result[TemurinReleaseData]:
        payload_result = await self._transport.request_json(
            _ADOPTIUM_LATEST_URL.format(major=major, implementation=_JVM_IMPL),
            params={
                'architecture': platform.architecture,
                'image_type': image_type.value,
                'os': platform.os,
                'vendor': _VENDOR,
            },
        )

        if not is_successful(payload_result):
            return Failure(payload_result.failure())

        payload: object = payload_result.unwrap()

        if not isinstance(payload, list) or not payload:
            return Failure(
                Error(
                    TemurinCatalogError.RELEASE_NOT_FOUND,
                    details={
                        'image_type': image_type.value,
                        'major': major,
                        'os': platform.os,
                        'architecture': platform.architecture,
                    },
                )
            )

        releases = cast('list[object]', payload)

        return _parse_release(releases[0], image_type, platform)


# --- Internal Types ----------------------------------------------------------

class TemurinCatalogError(StrEnum):
    METADATA_INVALID = 'the adoptium metadata response does not match the documented schema'
    RELEASE_NOT_FOUND = 'no temurin release exists for the requested version and platform'


def _mapping(value: object) -> dict[str, object] | None:
    if isinstance(value, dict):
        return cast('dict[str, object]', value)

    return None


def _parse_release(
    payload: object,
    image_type: TemurinImageType,
    platform: TemurinPlatformData,
) -> Result[TemurinReleaseData]:
    document = _mapping(payload)

    if document is None:
        return Failure(Error(TemurinCatalogError.METADATA_INVALID))

    version_raw = _mapping(document.get('version'))
    binary_raw = _mapping(document.get('binary'))

    if version_raw is None or binary_raw is None:
        return Failure(Error(TemurinCatalogError.METADATA_INVALID))

    major: object | None = version_raw.get('major')
    full_version: object | None = version_raw.get('openjdk_version')
    release_name: object | None = document.get('release_name')
    vendor: object | None = document.get('vendor')

    if not isinstance(major, int) or not isinstance(full_version, str):
        return Failure(Error(TemurinCatalogError.METADATA_INVALID))

    if not isinstance(release_name, str) or not isinstance(vendor, str):
        return Failure(Error(TemurinCatalogError.METADATA_INVALID))

    package_raw = _mapping(binary_raw.get('package'))
    binary_image_raw: object | None = binary_raw.get('image_type')

    if package_raw is None or not isinstance(binary_image_raw, str):
        return Failure(Error(TemurinCatalogError.METADATA_INVALID))

    try:
        binary_image_type = TemurinImageType(binary_image_raw)
    except ValueError:
        return Failure(
            Error(
                TemurinCatalogError.METADATA_INVALID,
                details={'image_type': binary_image_raw},
            )
        )

    checksum: object | None = package_raw.get('checksum')
    link: object | None = package_raw.get('link')
    name: object | None = package_raw.get('name')
    size: object | None = package_raw.get('size')

    if not isinstance(checksum, str) or not isinstance(link, str) or not isinstance(name, str):
        return Failure(Error(TemurinCatalogError.METADATA_INVALID))

    if not checksum or not link or not name:
        return Failure(Error(TemurinCatalogError.METADATA_INVALID))

    if not isinstance(size, int) or isinstance(size, bool):
        return Failure(Error(TemurinCatalogError.METADATA_INVALID))

    binary = TemurinBinaryData(
        architecture=platform.architecture,
        checksum=checksum,
        image_type=binary_image_type,
        jvm_impl=_JVM_IMPL,
        link=link,
        name=name,
        os=platform.os,
        size=size,
    )

    if binary.image_type != image_type:
        return Failure(Error(TemurinCatalogError.METADATA_INVALID, details={'expected': image_type.value}))

    return Success(
        TemurinReleaseData(
            binaries=[binary],
            full_version=full_version,
            major=major,
            release_name=release_name,
            vendor=vendor,
        )
    )
