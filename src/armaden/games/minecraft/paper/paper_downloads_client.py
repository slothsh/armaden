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
from armaden.games.minecraft.paper.dto.paper_build_data import PaperBuildData
from armaden.games.minecraft.paper.dto.paper_download_data import PaperDownloadData
from armaden.games.minecraft.paper.dto.paper_version_metadata_data import (
    PaperVersionMetadataData,
)
from armaden.games.minecraft.paper.protocols.paper_downloads_protocol import (
    PaperDownloadsProtocol,
)

_BUILD_ENDPOINT = 'https://fill.papermc.io/v3/projects/paper/versions/{version}/builds/{build}'
_BUILDS_LATEST_ENDPOINT = (
    'https://fill.papermc.io/v3/projects/paper/versions/{version}/builds/latest'
)
_PROJECT_ENDPOINT = 'https://fill.papermc.io/v3/projects/paper'
_VERSION_ENDPOINT = 'https://fill.papermc.io/v3/projects/paper/versions/{version}'


@final
class FillPaperDownloadsClient(PaperDownloadsProtocol):
    def __init__(self, transport: HttpTransportProtocol) -> None:
        self._transport: HttpTransportProtocol = transport


    @override
    async def build_metadata(self, version: str, build: int) -> Result[PaperBuildData]:
        payload = await self._request(
            _BUILD_ENDPOINT.format(version=version, build=build),
            not_found=PaperDownloadsError.BUILD_NOT_FOUND,
        )

        if not is_successful(payload):
            return Failure(payload.failure())

        return _parse_build(payload.unwrap())


    @override
    async def latest_build(self, version: str) -> Result[PaperBuildData]:
        payload = await self._request(
            _BUILDS_LATEST_ENDPOINT.format(version=version),
            not_found=PaperDownloadsError.BUILD_NOT_FOUND,
        )

        if not is_successful(payload):
            return Failure(payload.failure())

        return _parse_build(payload.unwrap())


    @override
    async def project_versions(self) -> Result[list[str]]:
        payload = await self._request(
            _PROJECT_ENDPOINT,
            not_found=PaperDownloadsError.VERSION_NOT_FOUND,
        )

        if not is_successful(payload):
            return Failure(payload.failure())

        document = _mapping(payload.unwrap())

        if document is None:
            return Failure(Error(PaperDownloadsError.RESPONSE_INVALID))

        versions_raw = _mapping(document.get('versions'))

        if versions_raw is None:
            return Failure(Error(PaperDownloadsError.RESPONSE_INVALID))

        versions: list[str] = []

        for family_raw in versions_raw.values():
            family = _sequence(family_raw)

            if family is None:
                return Failure(Error(PaperDownloadsError.RESPONSE_INVALID))

            for version in family:
                if not isinstance(version, str):
                    return Failure(Error(PaperDownloadsError.RESPONSE_INVALID))

                versions.append(version)

        return Success(versions)


    @override
    async def version_metadata(self, version: str) -> Result[PaperVersionMetadataData]:
        payload = await self._request(
            _VERSION_ENDPOINT.format(version=version),
            not_found=PaperDownloadsError.VERSION_NOT_FOUND,
        )

        if not is_successful(payload):
            return Failure(payload.failure())

        return _parse_version_metadata(payload.unwrap())


    async def _request(self, url: str, *, not_found: PaperDownloadsError) -> Result[object]:
        response = await self._transport.request_json(url)

        if is_successful(response):
            return response

        failure = response.failure()

        if isinstance(failure, Error):
            status: object | None = failure.details.get('status')

            if status == 404:
                return Failure(
                    Error(
                        not_found,
                        details={'url': url, 'body': failure.details.get('body')},
                    )
                )

        return Failure(failure)


# --- Internal Types ----------------------------------------------------------

class PaperDownloadsError(StrEnum):
    BUILD_NOT_FOUND = 'no paper build exists with the given identifier'
    RESPONSE_INVALID = 'the paper downloads api response does not match the documented schema'
    VERSION_NOT_FOUND = 'no paper version exists with the given identifier'


def _mapping(value: object) -> dict[str, object] | None:
    if isinstance(value, dict):
        return cast('dict[str, object]', value)

    return None


def _parse_build(payload: object) -> Result[PaperBuildData]:
    document = _mapping(payload)

    if document is None:
        return Failure(Error(PaperDownloadsError.RESPONSE_INVALID))

    number: object | None = document.get('id')
    channel: object | None = document.get('channel')
    time: object | None = document.get('time')
    downloads_raw = _mapping(document.get('downloads'))

    if (
        not isinstance(number, int)
        or isinstance(number, bool)
        or not isinstance(channel, str)
        or not isinstance(time, str)
        or downloads_raw is None
    ):
        return Failure(Error(PaperDownloadsError.RESPONSE_INVALID))

    downloads: dict[str, PaperDownloadData] = {}

    for download_name, download_value in downloads_raw.items():
        download_raw = _mapping(download_value)

        if download_raw is None:
            return Failure(Error(PaperDownloadsError.RESPONSE_INVALID))

        checksums_raw = _mapping(download_raw.get('checksums'))
        name: object | None = download_raw.get('name')
        size: object | None = download_raw.get('size')
        url: object | None = download_raw.get('url')

        if checksums_raw is None or not isinstance(name, str):
            return Failure(Error(PaperDownloadsError.RESPONSE_INVALID))

        sha256: object | None = checksums_raw.get('sha256')

        if (
            not isinstance(sha256, str)
            or not sha256
            or not isinstance(size, int)
            or isinstance(size, bool)
            or not isinstance(url, str)
        ):
            return Failure(Error(PaperDownloadsError.RESPONSE_INVALID))

        downloads[download_name] = PaperDownloadData(
            name=name,
            sha256=sha256,
            size=size,
            url=url,
        )

    return Success(
        PaperBuildData(
            channel=channel,
            downloads=downloads,
            number=number,
            time=time,
        )
    )


def _parse_version_metadata(payload: object) -> Result[PaperVersionMetadataData]:
    document = _mapping(payload)

    if document is None:
        return Failure(Error(PaperDownloadsError.RESPONSE_INVALID))

    version_raw = _mapping(document.get('version'))
    builds_raw = _sequence(document.get('builds'))

    if version_raw is None or builds_raw is None:
        return Failure(Error(PaperDownloadsError.RESPONSE_INVALID))

    identifier: object | None = version_raw.get('id')
    java_raw = _mapping(version_raw.get('java'))

    if not isinstance(identifier, str) or java_raw is None:
        return Failure(Error(PaperDownloadsError.RESPONSE_INVALID))

    java_version_raw = _mapping(java_raw.get('version'))

    if java_version_raw is None:
        return Failure(Error(PaperDownloadsError.RESPONSE_INVALID))

    java_minimum: object | None = java_version_raw.get('minimum')

    if not isinstance(java_minimum, int) or isinstance(java_minimum, bool):
        return Failure(Error(PaperDownloadsError.RESPONSE_INVALID))

    builds: list[int] = []

    for build in builds_raw:
        if not isinstance(build, int) or isinstance(build, bool):
            return Failure(Error(PaperDownloadsError.RESPONSE_INVALID))

        builds.append(build)

    return Success(
        PaperVersionMetadataData(
            builds=builds,
            java_minimum_major=java_minimum,
            version=identifier,
        )
    )


def _sequence(value: object) -> list[object] | None:
    if isinstance(value, list):
        return cast('list[object]', value)

    return None
