from typing import TypedDict

from armaden.games.minecraft.enums import MinecraftServerBackend


class ArgumentsConfig(TypedDict, total=False):
    nogui: bool | None
    extra: list[str] | None


class EulaConfig(TypedDict, total=False):
    accepted: bool | None


class InstallationConfig(TypedDict, total=False):
    directory: str | None


class JavaConfig(TypedDict, total=False):
    executable: str | None
    pin: bool | None
    version: int | None


class JvmConfig(TypedDict, total=False):
    initialMemoryMb: int | None
    maximumMemoryMb: int | None
    options: list[str] | None


class PaperConfig(TypedDict, total=False):
    build: int | None
    version: str | None


class ServerPropertiesConfig(TypedDict, total=False):
    difficulty: str | None
    gamemode: str | None
    levelName: str | None
    levelSeed: str | None
    maxPlayers: int | None
    motd: str | None
    onlineMode: bool | None
    pvp: bool | None
    serverPort: int | None
    simulationDistance: int | None
    viewDistance: int | None
    whiteList: bool | None


class Config(TypedDict, total=False):
    arguments: ArgumentsConfig | None
    backend: str | None
    eula: EulaConfig | None
    installation: InstallationConfig | None
    java: JavaConfig | None
    jvm: JvmConfig | None
    paper: PaperConfig | None
    server: ServerPropertiesConfig | None


DEFAULT_CONFIG: Config = {
    'arguments': {
        'nogui': True,
        'extra': [],
    },
    'backend': MinecraftServerBackend.PAPER,
    'eula': {
        'accepted': True,
    },
    'installation': {
        'directory': None,
    },
    'java': {
        'executable': None,
        'pin': False,
        'version': 25,
    },
    'jvm': {
        'initialMemoryMb': None,
        'maximumMemoryMb': None,
        'options': [],
    },
    'paper': {
        'build': None,
        'version': None,
    },
}