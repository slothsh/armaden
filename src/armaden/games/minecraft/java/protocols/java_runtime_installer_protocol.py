from typing import Protocol

from armaden.framework.types.result import Result
from armaden.games.minecraft.java.dto import JavaRuntimeManifestData


class JavaRuntimeInstallerProtocol(Protocol):
    async def install(self, paper_version: str) -> Result[JavaRuntimeManifestData]: ...

    def runtime(self) -> Result[JavaRuntimeManifestData]: ...

    async def update(self, paper_version: str) -> Result[JavaRuntimeManifestData]: ...
