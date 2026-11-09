from dataclasses import dataclass, field
from typing import final

from armaden.games.minecraft.paper.dto.paper_download_data import PaperDownloadData


@final
@dataclass
class PaperBuildData:
    downloads: dict[str, PaperDownloadData] = field(default_factory=dict)
    number: int = 0
    channel: str = ''
    time: str = ''
