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
