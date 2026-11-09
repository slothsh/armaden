from typing import Protocol

from armaden.framework.types.result import Result
from armaden.games.minecraft.paper.dto.paper_build_data import PaperBuildData
from armaden.games.minecraft.paper.dto.paper_version_metadata_data import (
    PaperVersionMetadataData,
)


class PaperDownloadsProtocol(Protocol):
    async def build_metadata(self, version: str, build: int) -> Result[PaperBuildData]: ...

    async def latest_build(self, version: str) -> Result[PaperBuildData]: ...

    async def project_versions(self) -> Result[list[str]]: ...

    async def version_metadata(self, version: str) -> Result[PaperVersionMetadataData]: ...
