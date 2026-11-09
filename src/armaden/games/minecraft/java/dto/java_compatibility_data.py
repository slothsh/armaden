from dataclasses import dataclass
from typing import final


@final
@dataclass
class JavaCompatibilityData:
    minimum_major: int
    paper_version: str
