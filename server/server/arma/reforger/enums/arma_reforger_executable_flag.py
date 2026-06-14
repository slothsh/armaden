from enum import StrEnum
from returns.result import Failure, Success
from server.lib.types import Error, Result


class ArmaReforgerExecutableFlag(StrEnum):
    """Arma Reforger CLI startup flags."""

    # -- General --------------------------------------------------------------

    LOG_LEVEL = "-logLevel"
    BIND_IP = "-bindIP"
    GAME_PORT = "-gamePort"
    STEAM_PORT = "-steamPort"
    A2S_ADDRESS = "-a2s"
    A2S_PORT = "-a2sPort"
    CONFIG_FILE = "-config"
    PROFILE_DIR = "-profile"
    LOGS_DIR = "-logsDir"
    RCON_HOST = "-rcon"
    RCON_PORT = "-rconPort"
    RCON_PASSWORD = "-rconPassword"
    ADDONS = "-addons"
    SCENARIO = "-scenario"
    AUTO_RELOAD = "-autoreload"
    SERVER_ID = "-serverId"
    SERVER_REGION = "-region"
    LOAD_SESSION_SAVE = "-loadSessionSave"
    FORCE_SESSION_LOAD = "-forceSessionLoad"
    ADDONS_DIR = "-addonsDir"
    ADDON_DOWNLOAD_DIR = "-addonDownloadDir"
    ADDON_TEMP_DIR = "-addonTempDir"
    BACKEND_DISABLE_STORAGE = "-backendDisableStorage"
    BACKEND_FRESH_SESSION = "-backendFreshSession"
    BACKEND_LOCAL_STORAGE = "-backendLocalStorage"
    FREEZE_CHECK = "-freezeCheck"
    FREEZE_CHECK_MODE = "-freezeCheckMode"
    CFG = "-cfg"
    LANGUAGE = "-language"
    NO_BACKEND = "-noBackend"
    NO_SOUND = "-noSound"
    NO_SPLASH = "-noSplash"
    NO_THROW = "-noThrow"
    SINGLE_THREADED_UPDATE = "-singleThreadedUpdate"
    WORLD = "-world"

    # -- Hosting --------------------------------------------------------------

    A2S_IP_ADDRESS = "-a2sIpAddress"
    AUTOSHUTDOWN = "-autoshutdown"
    ENABLE_NIGHT_GRAIN = "-enableNightGrain"
    LIST_SCENARIOS = "-listScenarios"
    KEEP_SESSION_SAVE = "-keepSessionSave"
    LOG_STATS = "-logStats"
    LOG_VOTING = "-logVoting"
    MAX_FPS = "-maxFPS"
    PLAYER_LIMITS = "-playerLimits"
    SERVER = "-server"
    ADDONS_VERIFY = "-addonsVerify"
    ADDONS_REPAIR = "-addonsRepair"

    # -- Network Tuning -------------------------------------------------------

    NDS = "-nds"
    NWK_RESOLUTION = "-nwkResolution"
    RPL_TIMEOUT_MS = "-rpl-timeout-ms"
    STAGGERING_BUDGET = "-staggeringBudget"
    STREAMING_BUDGET = "-streamingBudget"
    STREAMS_DELTA = "-streamsDelta"

    # -- Debug ----------------------------------------------------------------

    AI_LIMIT = "-AILimit"
    AI_PARTIAL_SIM = "-AIPartialSim"
    CREATE_DB = "-createDB"
    DEBUGGER = "-debugger"
    DEBUGGER_PORT = "-debuggerPort"
    DISABLE_AI = "-disableAI"
    DISABLE_CRASH_REPORTER = "-disableCrashReporter"
    DISABLE_NAVMESH_STREAMING = "-disableNavmeshStreaming"
    DISABLE_SHADERS_BUILD = "-disableShadersBuild"
    GENERATE_SHADERS = "-generateShaders"
    RPL_ENCODE_AS_LONG_JOBS = "-rplEncodeAsLongJobs"
    JOBSYS_SHORT_WORKER_COUNT = "-jobsysShortWorkerCount"
    JOBSYS_LONG_WORKER_COUNT = "-jobsysLongWorkerCount"
    KEEP_NUM_OF_LOGS = "-keepNumOfLogs"
    LOG_RDB_CHECKSUM = "-log-rdb-checksum"
    LOG_SCR_CHECKSUM = "-log-scr-checksum"
    LOG_APPEND = "-logAppend"
    LOG_FS = "-logFS"
    LOG_TIME = "-logTime"
    KEEP_CRASH_FILES = "-keepCrashFiles"
    MINIDUMP = "-minidump"
    SCRIPT_AUTHORIZE_ALL = "-scriptAuthorizeAll"
    SILENT_CRASH_REPORT = "-silentCrashReport"
    VM_ERROR_MODE = "-VMErrorMode"

    # -- Profiling ------------------------------------------------------------

    CHECK_INSTANCE = "-checkInstance"


    @classmethod
    def from_config(cls, key: str) -> Result[str]:
        CONFIG_MAP = {
            "logLevel": ArmaReforgerExecutableFlag.LOG_LEVEL,
            "bindIp": ArmaReforgerExecutableFlag.BIND_IP,
            "gamePort": ArmaReforgerExecutableFlag.GAME_PORT,
            "steamPort": ArmaReforgerExecutableFlag.STEAM_PORT,
            "a2s": ArmaReforgerExecutableFlag.A2S_ADDRESS,
            "a2sPort": ArmaReforgerExecutableFlag.A2S_PORT,
            "config": ArmaReforgerExecutableFlag.CONFIG_FILE,
            "profileDirectory": ArmaReforgerExecutableFlag.PROFILE_DIR,
            "logsDirectory": ArmaReforgerExecutableFlag.LOGS_DIR,
            "rcon": ArmaReforgerExecutableFlag.RCON_HOST,
            "rconPort": ArmaReforgerExecutableFlag.RCON_PORT,
            "rconPassword": ArmaReforgerExecutableFlag.RCON_PASSWORD,
            "addons": ArmaReforgerExecutableFlag.ADDONS,
            "scenario": ArmaReforgerExecutableFlag.SCENARIO,
            "autoReload": ArmaReforgerExecutableFlag.AUTO_RELOAD,
            "serverId": ArmaReforgerExecutableFlag.SERVER_ID,
            "region": ArmaReforgerExecutableFlag.SERVER_REGION,
            "loadSessionSave": ArmaReforgerExecutableFlag.LOAD_SESSION_SAVE,
            "forceSessionLoad": ArmaReforgerExecutableFlag.FORCE_SESSION_LOAD,
            "addonsDirectory": ArmaReforgerExecutableFlag.ADDONS_DIR,
            "addonDownloadDirectory": ArmaReforgerExecutableFlag.ADDON_DOWNLOAD_DIR,
            "addonTempDirectory": ArmaReforgerExecutableFlag.ADDON_TEMP_DIR,
            "backendDisableStorage": ArmaReforgerExecutableFlag.BACKEND_DISABLE_STORAGE,
            "backendFreshSession": ArmaReforgerExecutableFlag.BACKEND_FRESH_SESSION,
            "backendLocalStorage": ArmaReforgerExecutableFlag.BACKEND_LOCAL_STORAGE,
            "freezeCheck": ArmaReforgerExecutableFlag.FREEZE_CHECK,
            "freezeCheckMode": ArmaReforgerExecutableFlag.FREEZE_CHECK_MODE,
            "cfg": ArmaReforgerExecutableFlag.CFG,
            "language": ArmaReforgerExecutableFlag.LANGUAGE,
            "noBackend": ArmaReforgerExecutableFlag.NO_BACKEND,
            "noSound": ArmaReforgerExecutableFlag.NO_SOUND,
            "noSplash": ArmaReforgerExecutableFlag.NO_SPLASH,
            "noThrow": ArmaReforgerExecutableFlag.NO_THROW,
            "singleThreadedUpdate": ArmaReforgerExecutableFlag.SINGLE_THREADED_UPDATE,
            "world": ArmaReforgerExecutableFlag.WORLD,
            "a2sIpAddress": ArmaReforgerExecutableFlag.A2S_IP_ADDRESS,
            "autoShutdown": ArmaReforgerExecutableFlag.AUTOSHUTDOWN,
            "enableNightGrain": ArmaReforgerExecutableFlag.ENABLE_NIGHT_GRAIN,
            "listScenarios": ArmaReforgerExecutableFlag.LIST_SCENARIOS,
            "keepSessionSave": ArmaReforgerExecutableFlag.KEEP_SESSION_SAVE,
            "logStats": ArmaReforgerExecutableFlag.LOG_STATS,
            "logVoting": ArmaReforgerExecutableFlag.LOG_VOTING,
            "maxFps": ArmaReforgerExecutableFlag.MAX_FPS,
            "playerLimits": ArmaReforgerExecutableFlag.PLAYER_LIMITS,
            "server": ArmaReforgerExecutableFlag.SERVER,
            "addonsVerify": ArmaReforgerExecutableFlag.ADDONS_VERIFY,
            "addonsRepair": ArmaReforgerExecutableFlag.ADDONS_REPAIR,
            "nds": ArmaReforgerExecutableFlag.NDS,
            "nwkResolution": ArmaReforgerExecutableFlag.NWK_RESOLUTION,
            "rplTimeoutMs": ArmaReforgerExecutableFlag.RPL_TIMEOUT_MS,
            "staggeringBudget": ArmaReforgerExecutableFlag.STAGGERING_BUDGET,
            "streamingBudget": ArmaReforgerExecutableFlag.STREAMING_BUDGET,
            "streamsDelta": ArmaReforgerExecutableFlag.STREAMS_DELTA,
            "AiLimit": ArmaReforgerExecutableFlag.AI_LIMIT,
            "AiPartialSim": ArmaReforgerExecutableFlag.AI_PARTIAL_SIM,
            "createDb": ArmaReforgerExecutableFlag.CREATE_DB,
            "debugger": ArmaReforgerExecutableFlag.DEBUGGER,
            "debuggerPort": ArmaReforgerExecutableFlag.DEBUGGER_PORT,
            "disableAi": ArmaReforgerExecutableFlag.DISABLE_AI,
            "disableCrashReporter": ArmaReforgerExecutableFlag.DISABLE_CRASH_REPORTER,
            "disableNavmeshStreaming": ArmaReforgerExecutableFlag.DISABLE_NAVMESH_STREAMING,
            "disableShadersBuild": ArmaReforgerExecutableFlag.DISABLE_SHADERS_BUILD,
            "generateShaders": ArmaReforgerExecutableFlag.GENERATE_SHADERS,
            "rplEncodeAsLongJobs": ArmaReforgerExecutableFlag.RPL_ENCODE_AS_LONG_JOBS,
            "jobSysShortWorkerCount": ArmaReforgerExecutableFlag.JOBSYS_SHORT_WORKER_COUNT,
            "jobSysLongWorkerCount": ArmaReforgerExecutableFlag.JOBSYS_LONG_WORKER_COUNT,
            "keepNumOfLogs": ArmaReforgerExecutableFlag.KEEP_NUM_OF_LOGS,
            "logRdbChecksum": ArmaReforgerExecutableFlag.LOG_RDB_CHECKSUM,
            "logScrChecksum": ArmaReforgerExecutableFlag.LOG_SCR_CHECKSUM,
            "logAppend": ArmaReforgerExecutableFlag.LOG_APPEND,
            "logFs": ArmaReforgerExecutableFlag.LOG_FS,
            "logTime": ArmaReforgerExecutableFlag.LOG_TIME,
            "keepCrashFiles": ArmaReforgerExecutableFlag.KEEP_CRASH_FILES,
            "miniDump": ArmaReforgerExecutableFlag.MINIDUMP,
            "scriptAuthorizeAll": ArmaReforgerExecutableFlag.SCRIPT_AUTHORIZE_ALL,
            "silentCrashReport": ArmaReforgerExecutableFlag.SILENT_CRASH_REPORT,
            "VmErrorMode": ArmaReforgerExecutableFlag.VM_ERROR_MODE,
            "checkInstance": ArmaReforgerExecutableFlag.CHECK_INSTANCE,
        }

        if key not in CONFIG_MAP:
            return Failure(Error(ArmaReforgerExecutableFlagError.MISSING_CONFIG_KEY_MAPPING, details={
                'key': key
            }))

        return Success(CONFIG_MAP[key])


# -- Internal Types -----------------------------------------------------------

class ArmaReforgerExecutableFlagError(StrEnum):
    MISSING_CONFIG_KEY_MAPPING = "the config key could not be found for the arma reforger executable flag"
