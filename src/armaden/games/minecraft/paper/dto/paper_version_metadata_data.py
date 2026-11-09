from dataclasses import dataclass, field
from typing import final


@final
@dataclass
class PaperVersionMetadataData:
    builds: list[int] = field(default_factory=list)
    java_minimum_major: int = 0
    version: str = ''
