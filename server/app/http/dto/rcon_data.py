from pydantic.dataclasses import dataclass


@dataclass(frozen=True)
class SayRequestData:
    message: str


@dataclass(frozen=True)
class KickRequestData:
    player_id: str | int
    reason: str | None = None


@dataclass(frozen=True)
class BanRequestData:
    player_id: str | int
    duration: str | None = None
    reason: str | None = None


@dataclass(frozen=True)
class AddBanRequestData:
    guid_or_ip: str
    duration: str | None = None
    reason: str | None = None


@dataclass(frozen=True)
class RemoveBanRequestData:
    ban_id: str


@dataclass(frozen=True)
class LoadMissionRequestData:
    name: str
    difficulty: str | None = None


@dataclass(frozen=True)
class ServerAdminRequestData:
    cmd: str


@dataclass(frozen=True)
class CommandRequestData:
    cmd: str
