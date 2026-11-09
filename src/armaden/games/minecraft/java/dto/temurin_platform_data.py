from dataclasses import dataclass
from typing import final


@final
@dataclass
class TemurinPlatformData:
    architecture: str
    os: str
