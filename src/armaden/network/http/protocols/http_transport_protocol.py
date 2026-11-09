from collections.abc import Mapping
from pathlib import Path
from typing import Protocol

from armaden.framework.types.result import Result


class HttpTransportProtocol(Protocol):
    async def download_file(
        self,
        url: str,
        destination: Path,
        *,
        sha256: str | None = None,
    ) -> Result[Path]: ...

    async def request_json(
        self,
        url: str,
        *,
        params: Mapping[str, str] | None = None,
    ) -> Result[object]: ...
