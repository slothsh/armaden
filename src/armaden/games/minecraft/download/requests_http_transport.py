from __future__ import annotations

import asyncio
import hashlib
import os
import uuid
from collections.abc import Mapping
from enum import StrEnum
from pathlib import Path
from typing import final, override

import requests
from requests.adapters import HTTPAdapter
from returns.result import Failure, Success
from urllib3.util.retry import Retry

from armaden.framework.api.error import Error
from armaden.framework.types.result import Result
from armaden.games.minecraft.download.protocols.http_transport_protocol import (
    HttpTransportProtocol,
)

_ERROR_BODY_LIMIT = 2048
_DOWNLOAD_CHUNK_BYTES = 64 * 1024
_RETRIED_STATUSES = (429, 500, 502, 503, 504)


@final
class RequestsHttpTransport(HttpTransportProtocol):
    def __init__(
        self,
        *,
        connect_timeout: float = 10.0,
        read_timeout: float = 30.0,
        retries: int = 3,
        retry_backoff: float = 0.5,
    ) -> None:
        self._timeout: tuple[float, float] = (connect_timeout, read_timeout)
        self._session: requests.Session = requests.Session()
        retry: Retry = Retry(
            total=retries,
            connect=retries,
            read=retries,
            backoff_factor=retry_backoff,
            status_forcelist=_RETRIED_STATUSES,
            allowed_methods=frozenset({'GET'}),
        )
        adapter: HTTPAdapter = HTTPAdapter(max_retries=retry)
        self._session.mount('https://', adapter)
        self._session.mount('http://', adapter)


    @override
    async def download_file(
        self,
        url: str,
        destination: Path,
        *,
        sha256: str | None = None,
    ) -> Result[Path]:
        return await asyncio.to_thread(self._download_file, url, destination, sha256)


    @override
    async def request_json(
        self,
        url: str,
        *,
        params: Mapping[str, str] | None = None,
    ) -> Result[object]:
        return await asyncio.to_thread(self._request_json, url, params)


    def _download_file(
        self,
        url: str,
        destination: Path,
        sha256: str | None,
    ) -> Result[Path]:
        target: Path = Path(destination)
        temporary: Path = target.with_name(f'.{target.name}.{uuid.uuid4().hex}.tmp')
        digest = hashlib.sha256()

        try:
            target.parent.mkdir(parents=True, exist_ok=True)
            response: requests.Response = self._session.get(
                url,
                timeout=self._timeout,
                stream=True,
            )
            response.raise_for_status()

            with temporary.open('wb') as stream:
                for chunk in response.iter_content(chunk_size=_DOWNLOAD_CHUNK_BYTES):
                    if not chunk:
                        continue
                    digest.update(chunk)
                    _ = stream.write(chunk)

            if sha256 is not None and digest.hexdigest() != sha256.strip().lower():
                return Failure(
                    Error(
                        RequestsHttpTransportError.CHECKSUM_MISMATCH,
                        details={
                            'url': url,
                            'expected': sha256,
                            'actual': digest.hexdigest(),
                        },
                    )
                )

            os.replace(temporary, target)
        except requests.RequestException as exception:
            return Failure(
                Error(
                    RequestsHttpTransportError.DOWNLOAD_FAILED,
                    details={
                        'url': url,
                        'reason': str(exception),
                    },
                )
            )
        except OSError as exception:
            return Failure(
                Error(
                    RequestsHttpTransportError.DOWNLOAD_FAILED,
                    details={
                        'destination': str(destination),
                        'reason': str(exception),
                    },
                )
            )
        finally:
            temporary.unlink(missing_ok=True)

        return Success(target)


    def _request_json(
        self,
        url: str,
        params: Mapping[str, str] | None,
    ) -> Result[object]:
        try:
            response: requests.Response = self._session.get(
                url,
                params=params,
                timeout=self._timeout,
            )
            response.raise_for_status()
            payload: object = response.json()
        except requests.exceptions.JSONDecodeError as exception:
            return Failure(
                Error(
                    RequestsHttpTransportError.INVALID_RESPONSE,
                    details={
                        'url': url,
                        'reason': str(exception),
                    },
                )
            )
        except requests.RequestException as exception:
            response_status: int | None = None
            body: str | None = None
            failure_response: requests.Response | None = exception.response

            if failure_response is not None:
                response_status = failure_response.status_code
                body = failure_response.text[:_ERROR_BODY_LIMIT]

            return Failure(
                Error(
                    RequestsHttpTransportError.REQUEST_FAILED,
                    details={
                        'url': url,
                        'status': response_status,
                        'body': body,
                        'reason': str(exception),
                    },
                )
            )

        return Success(payload)


# --- Internal Types ----------------------------------------------------------

class RequestsHttpTransportError(StrEnum):
    CHECKSUM_MISMATCH = 'the downloaded artifact does not match its published sha-256 checksum'
    DOWNLOAD_FAILED = 'the artifact download failed'
    INVALID_RESPONSE = 'the http response body is not valid json'
    REQUEST_FAILED = 'the http request failed after retries'
