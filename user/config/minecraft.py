from typing import cast

from armaden.framework.support.env import Env

from armaden.games.minecraft import MinecraftServerBackend, MinecraftServerConfig


def _json_string_list(name: str) -> list[str] | None:
    value: object | None = Env.json(name)

    if value is None:
        return None

    if not isinstance(value, list):
        return None

    items: list[object] = cast(list[object], value)

    return [item for item in items if isinstance(item, str)]


def config() -> MinecraftServerConfig:
    return cast(MinecraftServerConfig, cast(object, {
        'arguments': {
            'extra': _json_string_list('MINECRAFT_ARGUMENTS_EXTRA'),
            'nogui': Env.bool('MINECRAFT_NOGUI', True),
        },
        'backend': Env.string('MINECRAFT_BACKEND', MinecraftServerBackend.PAPER.value),
        'eula': {
            'accepted': Env.bool('MINECRAFT_EULA_ACCEPTED', True),
        },
        'installation': {
            'directory': Env.string('MINECRAFT_INSTALL_DIR'),
        },
        'java': {
            'executable': Env.string('MINECRAFT_JAVA_EXECUTABLE'),
            'pin': Env.bool('MINECRAFT_JAVA_PIN', False),
            'version': Env.int('MINECRAFT_JAVA_VERSION', 25),
        },
        'jvm': {
            'initialMemoryMb': Env.int('MINECRAFT_JVM_INITIAL_MEMORY_MB'),
            'maximumMemoryMb': Env.int('MINECRAFT_JVM_MAXIMUM_MEMORY_MB'),
            'options': _json_string_list('MINECRAFT_JVM_OPTIONS'),
        },
        'paper': {
            'build': Env.int('MINECRAFT_PAPER_BUILD'),
            'version': Env.string('MINECRAFT_PAPER_VERSION'),
        },
        'server': {
            'difficulty': Env.string('MINECRAFT_DIFFICULTY'),
            'gamemode': Env.string('MINECRAFT_GAMEMODE'),
            'levelName': Env.string('MINECRAFT_LEVEL_NAME'),
            'levelSeed': Env.string('MINECRAFT_LEVEL_SEED'),
            'maxPlayers': Env.int('MINECRAFT_MAX_PLAYERS'),
            'motd': Env.string('MINECRAFT_MOTD'),
            'onlineMode': Env.bool('MINECRAFT_ONLINE_MODE'),
            'serverPort': Env.int('MINECRAFT_SERVER_PORT'),
            'simulationDistance': Env.int('MINECRAFT_SIMULATION_DISTANCE'),
            'viewDistance': Env.int('MINECRAFT_VIEW_DISTANCE'),
            'whiteList': Env.bool('MINECRAFT_WHITE_LIST', False),
        },
    }))
