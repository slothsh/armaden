from typing import final, override

from returns.pipeline import is_successful
from returns.result import Failure, Success

from armaden.framework.types.result import Result
from armaden.games.minecraft.java.dto import JavaCompatibilityData
from armaden.games.minecraft.java.protocols import JavaCompatibilityProtocol
from armaden.games.minecraft.paper.protocols.paper_downloads_protocol import (
    PaperDownloadsProtocol,
)


@final
class PaperJavaCompatibility(JavaCompatibilityProtocol):
    def __init__(self, downloads: PaperDownloadsProtocol) -> None:
        self._downloads: PaperDownloadsProtocol = downloads


    @override
    async def java_compatibility(self, paper_version: str) -> Result[JavaCompatibilityData]:
        metadata = await self._downloads.version_metadata(paper_version)

        if not is_successful(metadata):
            return Failure(metadata.failure())

        resolved = metadata.unwrap()

        return Success(
            JavaCompatibilityData(
                minimum_major=resolved.java_minimum_major,
                paper_version=resolved.version,
            )
        )
