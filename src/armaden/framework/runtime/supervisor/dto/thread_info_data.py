from dataclasses import dataclass

@dataclass(frozen=True)
class ThreadInfoData:
    id: int
    name: str
