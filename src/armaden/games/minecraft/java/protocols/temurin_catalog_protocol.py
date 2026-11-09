from typing import Protocol

from armaden.framework.types.result import Result
from armaden.games.minecraft.java.dto import TemurinPlatformData, TemurinReleaseData
from armaden.games.minecraft.java.enums import TemurinImageType


class TemurinCatalogProtocol(Protocol):
    async def latest_release(
        self,
        image_type: TemurinImageType,
        major: int,
        platform: TemurinPlatformData,
    ) -> Result[TemurinReleaseData]: ...
