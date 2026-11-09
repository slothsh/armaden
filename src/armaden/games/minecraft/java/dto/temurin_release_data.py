from dataclasses import dataclass, field
from typing import final

from armaden.games.minecraft.java.dto.temurin_binary_data import TemurinBinaryData


@final
@dataclass
class TemurinReleaseData:
    binaries: list[TemurinBinaryData] = field(default_factory=list)
    full_version: str = ''
    major: int = 0
    release_name: str = ''
    vendor: str = ''
