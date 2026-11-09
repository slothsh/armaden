from typing import Protocol

from armaden.framework.types.result import Result
from armaden.games.minecraft.paper.dto.paper_artifact_manifest_data import (
    PaperArtifactManifestData,
)


class PaperArtifactInstallerProtocol(Protocol):
    async def install(self) -> Result[PaperArtifactManifestData]: ...

    def artifact(self) -> Result[PaperArtifactManifestData]: ...

    async def update(self) -> Result[PaperArtifactManifestData]: ...
