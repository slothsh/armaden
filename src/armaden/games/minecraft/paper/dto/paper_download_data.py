from dataclasses import dataclass
from typing import final


@final
@dataclass
class PaperDownloadData:
    name: str
    sha256: str
    size: int
    url: str
