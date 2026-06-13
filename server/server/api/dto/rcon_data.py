from typing import Self
from pydantic.dataclasses import dataclass

@dataclass
class SayRequestData:
    message: str


@dataclass
class KickRequestData:
    player_id: str | int
    reason: str | None = None


@dataclass
class BanRequestData:
    player_id: str | int
    duration: str | None = None
    reason: str | None = None


@dataclass
class AddBanRequestData:
    guid_or_ip: str
    duration: str | None = None
    reason: str | None = None


@dataclass
class RemoveBanRequestData:
    ban_id: str


@dataclass
class LoadMissionRequestData:
    name: str
    difficulty: str | None = None


@dataclass
class ServerAdminRequestData:
    cmd: str


@dataclass
class CommandRequestData:
    cmd: str


@dataclass(frozen=True)
class PlayerResponseData:
    """A connected player returned by the ``players`` command."""

    slot: int
    """BattlerEye slot number (used for ``kick`` / ``ban``)."""
    uid: str
    """In-game player UID."""
    name: str
    """Player display name."""

    @classmethod
    def from_line(cls, line: str) -> Self | None:
        """Parse a single data row from ``players`` output.

        Returns ``None``  if the line is a header or otherwise
        unparsable.
        """
        parts = [p.strip() for p in line.split(";")]
        if len(parts) < 3:
            return None
        try:
            slot = int(parts[0])
        except ValueError:
            # Header line (e.g. "Players on server: [Player#]")
            return None
        return cls(slot=slot, uid=parts[1], name=parts[2])

