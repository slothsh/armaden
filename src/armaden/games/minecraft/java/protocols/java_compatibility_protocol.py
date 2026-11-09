from typing import Protocol

from armaden.framework.types.result import Result
from armaden.games.minecraft.java.dto import JavaCompatibilityData


class JavaCompatibilityProtocol(Protocol):
    async def java_compatibility(self, paper_version: str) -> Result[JavaCompatibilityData]: ...
