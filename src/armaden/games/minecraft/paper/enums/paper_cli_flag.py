from __future__ import annotations

from enum import StrEnum

from returns.result import Failure, Success

from armaden.framework.api.error import Error
from armaden.framework.types.result import Result


class PaperCliFlag(StrEnum):
    ADD_PLUGIN_DIR = '--add-plugin-dir'
    ADD_PLUGIN_JAR = '--add-plugin'
    BONUS_CHEST = '--bonusChest'
    BUKKIT_SETTINGS = '--bukkit-settings'
    COMMANDS_SETTINGS = '--commands-settings'
    CONFIG = '--config'
    DEMO = '--demo'
    ERASE_CACHE = '--eraseCache'
    FORCE_UPGRADE = '--forceUpgrade'
    HELP = '-?'
    HOST = '--host'
    INIT_SETTINGS = '--initSettings'
    JFR_PROFILE = '--jfrProfile'
    LEVEL_NAME = '--level-name'
    MAX_PLAYERS = '--max-players'
    NOCONSOLE = '--noconsole'
    NOGUI = '--nogui'
    NOJLINE = '--nojline'
    ONLINE_MODE = '--online-mode'
    PAPER_DIR = '--paper-dir'
    PAPER_SETTINGS = '--paper-settings'
    PID_FILE = '--pidFile'
    PLUGINS = '--plugins'
    PORT = '--port'
    RECREATE_REGION_FILES = '--recreateRegionFiles'
    SAFE_MODE = '--safeMode'
    SERVER_ID = '--serverId'
    SERVER_NAME = '--server-name'
    SPIGOT_SETTINGS = '--spigot-settings'
    UNIVERSE = '--universe'
    VERSION = '--version'

    @classmethod
    def aliases(cls) -> dict[str, PaperCliFlag]:
        return {
            '-?': cls.HELP,
            '--help': cls.HELP,
            '-C': cls.COMMANDS_SETTINGS,
            '--commands-settings': cls.COMMANDS_SETTINGS,
            '-P': cls.PLUGINS,
            '--plugins': cls.PLUGINS,
            '-S': cls.SPIGOT_SETTINGS,
            '--spigot-settings': cls.SPIGOT_SETTINGS,
            '-W': cls.UNIVERSE,
            '--universe': cls.UNIVERSE,
            '--world-container': cls.UNIVERSE,
            '--world-dir': cls.UNIVERSE,
            '--add-extra-plugin-dir': cls.ADD_PLUGIN_DIR,
            '--add-plugin-dir': cls.ADD_PLUGIN_DIR,
            '--add-extra-plugin-jar': cls.ADD_PLUGIN_JAR,
            '--add-plugin': cls.ADD_PLUGIN_JAR,
            '-b': cls.BUKKIT_SETTINGS,
            '--bukkit-settings': cls.BUKKIT_SETTINGS,
            '-c': cls.CONFIG,
            '--config': cls.CONFIG,
            '--demo': cls.DEMO,
            '--bonusChest': cls.BONUS_CHEST,
            '--eraseCache': cls.ERASE_CACHE,
            '--forceUpgrade': cls.FORCE_UPGRADE,
            '-h': cls.HOST,
            '--host': cls.HOST,
            '--server-ip': cls.HOST,
            '--initSettings': cls.INIT_SETTINGS,
            '--jfrProfile': cls.JFR_PROFILE,
            '--noconsole': cls.NOCONSOLE,
            '--nogui': cls.NOGUI,
            '--nojline': cls.NOJLINE,
            '-o': cls.ONLINE_MODE,
            '--online-mode': cls.ONLINE_MODE,
            '-p': cls.PORT,
            '--port': cls.PORT,
            '--server-port': cls.PORT,
            '--paper': cls.PAPER_SETTINGS,
            '--paper-settings': cls.PAPER_SETTINGS,
            '--paper-dir': cls.PAPER_DIR,
            '--paper-settings-directory': cls.PAPER_DIR,
            '--pidFile': cls.PID_FILE,
            '--recreateRegionFiles': cls.RECREATE_REGION_FILES,
            '-s': cls.MAX_PLAYERS,
            '--max-players': cls.MAX_PLAYERS,
            '--size': cls.MAX_PLAYERS,
            '--safeMode': cls.SAFE_MODE,
            '--server-name': cls.SERVER_NAME,
            '--serverId': cls.SERVER_ID,
            '-v': cls.VERSION,
            '--version': cls.VERSION,
            '-w': cls.LEVEL_NAME,
            '--level-name': cls.LEVEL_NAME,
            '--world': cls.LEVEL_NAME,
        }

    @classmethod
    def defaults(cls) -> dict[PaperCliFlag, str]:
        return {
            cls.BUKKIT_SETTINGS: 'bukkit.yml',
            cls.COMMANDS_SETTINGS: 'commands.yml',
            cls.CONFIG: 'server.properties',
            cls.PAPER_DIR: 'config',
            cls.PAPER_SETTINGS: 'paper.yml',
            cls.PLUGINS: 'plugins',
            cls.SERVER_NAME: 'Unknown Server',
            cls.SPIGOT_SETTINGS: 'spigot.yml',
            cls.UNIVERSE: '.',
        }

    @classmethod
    def from_token(cls, token: str) -> Result[PaperCliFlag]:
        flag = cls.aliases().get(token)

        if flag is None:
            return Failure(Error(PaperCliFlagError.UNKNOWN_FLAG, details={'token': token}))

        return Success(flag)

    @classmethod
    def migration_only_flags(cls) -> frozenset[PaperCliFlag]:
        return frozenset({cls.PAPER_SETTINGS})

    @classmethod
    def path_flags(cls) -> frozenset[PaperCliFlag]:
        return frozenset({
            cls.ADD_PLUGIN_DIR,
            cls.ADD_PLUGIN_JAR,
            cls.BUKKIT_SETTINGS,
            cls.COMMANDS_SETTINGS,
            cls.CONFIG,
            cls.PAPER_DIR,
            cls.PAPER_SETTINGS,
            cls.PID_FILE,
            cls.PLUGINS,
            cls.SPIGOT_SETTINGS,
            cls.UNIVERSE,
        })

    @classmethod
    def repeatable_flags(cls) -> frozenset[PaperCliFlag]:
        return frozenset({cls.ADD_PLUGIN_DIR, cls.ADD_PLUGIN_JAR})

    @classmethod
    def server_preventing_flags(cls) -> frozenset[PaperCliFlag]:
        return frozenset({cls.HELP, cls.VERSION})

    @classmethod
    def server_properties_counterparts(cls) -> dict[PaperCliFlag, str]:
        return {
            cls.HOST: 'server-ip',
            cls.LEVEL_NAME: 'level-name',
            cls.MAX_PLAYERS: 'max-players',
            cls.ONLINE_MODE: 'online-mode',
            cls.PORT: 'server-port',
        }

    @classmethod
    def settings_only_flags(cls) -> frozenset[PaperCliFlag]:
        return frozenset({cls.INIT_SETTINGS})

    @classmethod
    def value_flags(cls) -> frozenset[PaperCliFlag]:
        return frozenset({
            cls.BUKKIT_SETTINGS,
            cls.COMMANDS_SETTINGS,
            cls.CONFIG,
            cls.HOST,
            cls.LEVEL_NAME,
            cls.MAX_PLAYERS,
            cls.ONLINE_MODE,
            cls.PAPER_DIR,
            cls.PAPER_SETTINGS,
            cls.PID_FILE,
            cls.PLUGINS,
            cls.PORT,
            cls.SERVER_ID,
            cls.SERVER_NAME,
            cls.SPIGOT_SETTINGS,
            cls.UNIVERSE,
        })


# --- Internal Types ----------------------------------------------------------

class PaperCliFlagError(StrEnum):
    UNKNOWN_FLAG = 'the token does not match any documented paper cli argument'
