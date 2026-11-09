from __future__ import annotations

from enum import StrEnum


class PaperSystemProperty(StrEnum):
    ALWAYS_PRINT_WARNING_STATE = 'paper.alwaysPrintWarningState'
    BYPASS_HOST_CHECK = 'Paper.bypassHostCheck'
    DEBUG_DYNAMIC_MISSING_KEYS = 'Paper.debugDynamicMissingKeys'
    DEBUG_ENTITIES_WITH_INVALID_IDS = 'paper.debugEntitiesWithInvalidIds'
    DEBUG_SYNC_LOADS = 'paper.debug-sync-loads'
    DISABLE_CHANNEL_LIMIT = 'paper.disableChannelLimit'
    DISABLE_CLASS_PRIORITIZATION = 'Paper.DisableClassPrioritization'
    DISABLE_FLUSH_CONSOLIDATE = 'Paper.disableFlushConsolidate'
    DISABLE_MIGRATION_DELAY = 'paper.disableMigrationDelay'
    DISABLE_OLD_API_SUPPORT = 'paper.disableOldApiSupport'
    DISABLE_STARTUP_VERSION_CHECK = 'paper.disableStartupVersionCheck'
    DISABLE_WATCHDOG = 'disable.watchdog'
    DISABLE_WORLD_SYMLINK_VALIDATION = 'paper.disableWorldSymlinkValidation'
    ENABLE_SYNC_CHUNK_WRITES = 'Paper.enable-sync-chunk-writes'
    EULA_AGREE = 'com.mojang.eula.agree'
    EXCESSIVE_TE_LIMIT = 'Paper.excessiveTELimit'
    EXPLICIT_FLUSH = 'paper.explicit-flush'
    IGNORE_JAVA_VERSION = 'Paper.IgnoreJavaVersion'
    IGNORE_WORLD_DATA_VERSION = 'Paper.ignoreWorldDataVersion'
    LET_ME_RELOAD = 'LetMeReload'
    LIBRARY_LOADER_CENTRAL_URL = 'org.bukkit.plugin.java.LibraryLoader.centralURL'
    MANAGEMENT_TLS_KEYSTORE_PASSWORD = 'management.tls.keystore.password'
    MAX_CHAT_COMMAND_INPUT_SIZE = 'paper.maxChatCommandInputSize'
    MAX_CUSTOM_CHANNEL_NAME = 'paper.maxCustomChannelName'
    MAX_SIGN_LENGTH = 'Paper.maxSignLength'
    MAX_VIEW_DISTANCE = 'Paper.MaxViewDistance'
    MIN_PRECACHED_DATAFIX_VERSION = 'Paper.minPrecachedDatafixVersion'
    PARSE_YAML_COMMENTS_BY_DEFAULT = 'Paper.parseYamlCommentsByDefault'
    PAPERCLIP_PATCH_ONLY = 'paperclip.patchonly'
    PLAYER_CONNECTION_KEEPALIVE = 'paper.playerconnection.keepalive'
    PLUGIN_MESSAGE_CHANNEL_LIMIT = 'paper.pluginMessageChannelLimit'
    PREFER_SPARK_PLUGIN = 'paper.preferSparkPlugin'
    PROFILES_API_HOST = 'minecraft.api.profiles.host'
    SERVER_PROPERTIES_COMMENTS_SKIPPED = 'Paper.skipServerPropertiesComments'
    SERVICES_API_HOST = 'minecraft.api.services.host'
    SESSION_API_HOST = 'minecraft.api.session.host'
    SOUT_NAGS_INTERVAL = 'io.papermc.paper.sout.nags.interval'
    SOUT_NAGS_TIMEOUT = 'io.papermc.paper.sout.nags.timeout'
    SUPPRESS_SOUT_NAGS = 'io.papermc.paper.suppress.sout.nags'
    TIMINGS_BYPASS_MAX = 'timings.bypassMax'
    USE_LEGACY_PLUGIN_LOADING = 'paper.useLegacyPluginLoading'
    WARN_WHEN_LEGACY_FORMATTING_DETECTED = 'net.kyori.adventure.text.warnWhenLegacyFormattingDetected'
    WORKER_THREAD_COUNT = 'Paper.WorkerThreadCount'

    @classmethod
    def caution(cls) -> frozenset[PaperSystemProperty]:
        return frozenset({
            cls.DISABLE_MIGRATION_DELAY,
            cls.LIBRARY_LOADER_CENTRAL_URL,
        })

    @classmethod
    def computed_defaults(cls) -> dict[PaperSystemProperty, str]:
        return {
            cls.MIN_PRECACHED_DATAFIX_VERSION: 'the minecraft world version plus one',
            cls.WORKER_THREAD_COUNT: 'half of the available physical cores, or one when three or fewer cores are available',
        }

    @classmethod
    def defaults(cls) -> dict[PaperSystemProperty, str]:
        return {
            cls.DEBUG_ENTITIES_WITH_INVALID_IDS: 'false',
            cls.DISABLE_OLD_API_SUPPORT: 'false',
            cls.DISABLE_WORLD_SYMLINK_VALIDATION: 'false',
            cls.EULA_AGREE: 'false',
            cls.EXCESSIVE_TE_LIMIT: '750',
            cls.IGNORE_JAVA_VERSION: 'false',
            cls.LIBRARY_LOADER_CENTRAL_URL: 'https://maven-central.storage-download.googleapis.com/maven2',
            cls.MAX_CHAT_COMMAND_INPUT_SIZE: '256',
            cls.MAX_CUSTOM_CHANNEL_NAME: '32767',
            cls.MAX_SIGN_LENGTH: '80',
            cls.MAX_VIEW_DISTANCE: '32',
            cls.PARSE_YAML_COMMENTS_BY_DEFAULT: 'true',
            cls.PAPERCLIP_PATCH_ONLY: 'false',
            cls.PLAYER_CONNECTION_KEEPALIVE: '30',
            cls.PLUGIN_MESSAGE_CHANNEL_LIMIT: '128',
            cls.PREFER_SPARK_PLUGIN: 'false',
            cls.PROFILES_API_HOST: 'https://api.mojang.com',
            cls.SERVICES_API_HOST: 'https://api.minecraftservices.com',
            cls.SESSION_API_HOST: 'https://sessionserver.mojang.com',
            cls.SOUT_NAGS_INTERVAL: '200',
            cls.SOUT_NAGS_TIMEOUT: '5000',
            cls.USE_LEGACY_PLUGIN_LOADING: 'false',
            cls.WARN_WHEN_LEGACY_FORMATTING_DETECTED: 'false',
        }

    @classmethod
    def deprecated(cls) -> frozenset[PaperSystemProperty]:
        return frozenset({cls.TIMINGS_BYPASS_MAX})

    @classmethod
    def unset_by_default(cls) -> frozenset[PaperSystemProperty]:
        return frozenset({
            cls.ALWAYS_PRINT_WARNING_STATE,
            cls.BYPASS_HOST_CHECK,
            cls.DEBUG_DYNAMIC_MISSING_KEYS,
            cls.DEBUG_SYNC_LOADS,
            cls.DISABLE_CHANNEL_LIMIT,
            cls.DISABLE_CLASS_PRIORITIZATION,
            cls.DISABLE_FLUSH_CONSOLIDATE,
            cls.DISABLE_MIGRATION_DELAY,
            cls.DISABLE_STARTUP_VERSION_CHECK,
            cls.DISABLE_WATCHDOG,
            cls.ENABLE_SYNC_CHUNK_WRITES,
            cls.EXPLICIT_FLUSH,
            cls.IGNORE_WORLD_DATA_VERSION,
            cls.LET_ME_RELOAD,
            cls.MANAGEMENT_TLS_KEYSTORE_PASSWORD,
            cls.SERVER_PROPERTIES_COMMENTS_SKIPPED,
            cls.SUPPRESS_SOUT_NAGS,
            cls.TIMINGS_BYPASS_MAX,
        })
