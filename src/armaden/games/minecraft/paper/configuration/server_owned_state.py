from __future__ import annotations

from enum import StrEnum
from pathlib import Path
from typing import ClassVar, final


class PaperServerOwnedFile(StrEnum):
    BANNED_IPS = 'banned-ips.json'
    BANNED_PLAYERS = 'banned-players.json'
    OPS = 'ops.json'
    USERCACHE = 'usercache.json'
    WHITELIST = 'whitelist.json'


@final
class PaperServerOwnedState:
    OWNED_FILES: ClassVar[frozenset[str]] = frozenset(
        member.value for member in PaperServerOwnedFile
    )

    MANAGED_LOCATIONS: ClassVar[frozenset[str]] = frozenset({
        '.paper-remapped',
        'bStats',
        'logs',
        'plugins',
        'spark',
        'world',
        'world_nether',
        'world_the_end',
    })

    @classmethod
    def is_managed_location(cls, name: str) -> bool:
        return name in cls.MANAGED_LOCATIONS


    @classmethod
    def is_owned_file(cls, path: Path) -> bool:
        return path.name in cls.OWNED_FILES
