from dataclasses import dataclass
from typing import final

from armaden.games.minecraft.java.enums import TemurinImageType


@final
@dataclass
class TemurinBinaryData:
    architecture: str
    checksum: str
    image_type: TemurinImageType
    jvm_impl: str
    link: str
    name: str
    os: str
    size: int
