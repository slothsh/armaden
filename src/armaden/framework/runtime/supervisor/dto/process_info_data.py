from dataclasses import dataclass
from asyncio.subprocess import Process


@dataclass(frozen=True)
class ProcessInfoData:
    name: str
    process: Process
