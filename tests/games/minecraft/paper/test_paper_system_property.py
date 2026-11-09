from __future__ import annotations

from returns.pipeline import is_successful

from armaden.games.minecraft.paper.dto import PaperJvmLaunchData
from armaden.games.minecraft.paper.enums import PaperSystemProperty
from tests.games.minecraft.paper.paper_reference import SYSTEM_PROPERTIES_SNAPSHOT, SYSTEM_PROPERTIES_URL

DOCUMENTED_PROPERTIES: dict[PaperSystemProperty, str] = {
    PaperSystemProperty.ALWAYS_PRINT_WARNING_STATE: 'paper.alwaysPrintWarningState',
    PaperSystemProperty.BYPASS_HOST_CHECK: 'Paper.bypassHostCheck',
    PaperSystemProperty.DEBUG_DYNAMIC_MISSING_KEYS: 'Paper.debugDynamicMissingKeys',
    PaperSystemProperty.DEBUG_ENTITIES_WITH_INVALID_IDS: 'paper.debugEntitiesWithInvalidIds',
    PaperSystemProperty.DEBUG_SYNC_LOADS: 'paper.debug-sync-loads',
    PaperSystemProperty.DISABLE_CHANNEL_LIMIT: 'paper.disableChannelLimit',
    PaperSystemProperty.DISABLE_CLASS_PRIORITIZATION: 'Paper.DisableClassPrioritization',
    PaperSystemProperty.DISABLE_FLUSH_CONSOLIDATE: 'Paper.disableFlushConsolidate',
    PaperSystemProperty.DISABLE_MIGRATION_DELAY: 'paper.disableMigrationDelay',
    PaperSystemProperty.DISABLE_OLD_API_SUPPORT: 'paper.disableOldApiSupport',
    PaperSystemProperty.DISABLE_STARTUP_VERSION_CHECK: 'paper.disableStartupVersionCheck',
    PaperSystemProperty.DISABLE_WATCHDOG: 'disable.watchdog',
    PaperSystemProperty.DISABLE_WORLD_SYMLINK_VALIDATION: 'paper.disableWorldSymlinkValidation',
    PaperSystemProperty.ENABLE_SYNC_CHUNK_WRITES: 'Paper.enable-sync-chunk-writes',
    PaperSystemProperty.EULA_AGREE: 'com.mojang.eula.agree',
    PaperSystemProperty.EXCESSIVE_TE_LIMIT: 'Paper.excessiveTELimit',
    PaperSystemProperty.EXPLICIT_FLUSH: 'paper.explicit-flush',
    PaperSystemProperty.IGNORE_JAVA_VERSION: 'Paper.IgnoreJavaVersion',
    PaperSystemProperty.IGNORE_WORLD_DATA_VERSION: 'Paper.ignoreWorldDataVersion',
    PaperSystemProperty.LET_ME_RELOAD: 'LetMeReload',
    PaperSystemProperty.LIBRARY_LOADER_CENTRAL_URL: 'org.bukkit.plugin.java.LibraryLoader.centralURL',
    PaperSystemProperty.MANAGEMENT_TLS_KEYSTORE_PASSWORD: 'management.tls.keystore.password',
    PaperSystemProperty.MAX_CHAT_COMMAND_INPUT_SIZE: 'paper.maxChatCommandInputSize',
    PaperSystemProperty.MAX_CUSTOM_CHANNEL_NAME: 'paper.maxCustomChannelName',
    PaperSystemProperty.MAX_SIGN_LENGTH: 'Paper.maxSignLength',
    PaperSystemProperty.MAX_VIEW_DISTANCE: 'Paper.MaxViewDistance',
    PaperSystemProperty.MIN_PRECACHED_DATAFIX_VERSION: 'Paper.minPrecachedDatafixVersion',
    PaperSystemProperty.PARSE_YAML_COMMENTS_BY_DEFAULT: 'Paper.parseYamlCommentsByDefault',
    PaperSystemProperty.PAPERCLIP_PATCH_ONLY: 'paperclip.patchonly',
    PaperSystemProperty.PLAYER_CONNECTION_KEEPALIVE: 'paper.playerconnection.keepalive',
    PaperSystemProperty.PLUGIN_MESSAGE_CHANNEL_LIMIT: 'paper.pluginMessageChannelLimit',
    PaperSystemProperty.PREFER_SPARK_PLUGIN: 'paper.preferSparkPlugin',
    PaperSystemProperty.PROFILES_API_HOST: 'minecraft.api.profiles.host',
    PaperSystemProperty.SERVER_PROPERTIES_COMMENTS_SKIPPED: 'Paper.skipServerPropertiesComments',
    PaperSystemProperty.SERVICES_API_HOST: 'minecraft.api.services.host',
    PaperSystemProperty.SESSION_API_HOST: 'minecraft.api.session.host',
    PaperSystemProperty.SOUT_NAGS_INTERVAL: 'io.papermc.paper.sout.nags.interval',
    PaperSystemProperty.SOUT_NAGS_TIMEOUT: 'io.papermc.paper.sout.nags.timeout',
    PaperSystemProperty.SUPPRESS_SOUT_NAGS: 'io.papermc.paper.suppress.sout.nags',
    PaperSystemProperty.TIMINGS_BYPASS_MAX: 'timings.bypassMax',
    PaperSystemProperty.USE_LEGACY_PLUGIN_LOADING: 'paper.useLegacyPluginLoading',
    PaperSystemProperty.WARN_WHEN_LEGACY_FORMATTING_DETECTED: 'net.kyori.adventure.text.warnWhenLegacyFormattingDetected',
    PaperSystemProperty.WORKER_THREAD_COUNT: 'Paper.WorkerThreadCount',
}


def test_reference_snapshot_is_recorded() -> None:
    assert SYSTEM_PROPERTIES_URL == 'https://docs.papermc.io/paper/reference/system-properties/'
    assert SYSTEM_PROPERTIES_SNAPSHOT['commit'] == '68ac55d'


def test_every_documented_property_is_represented() -> None:
    for property_, documented_value in DOCUMENTED_PROPERTIES.items():
        assert property_.value == documented_value

    assert len(DOCUMENTED_PROPERTIES) == len(PaperSystemProperty)


def test_defaults_match_the_reference() -> None:
    defaults = PaperSystemProperty.defaults()

    assert defaults[PaperSystemProperty.PLAYER_CONNECTION_KEEPALIVE] == '30'
    assert defaults[PaperSystemProperty.PLUGIN_MESSAGE_CHANNEL_LIMIT] == '128'
    assert defaults[PaperSystemProperty.WARN_WHEN_LEGACY_FORMATTING_DETECTED] == 'false'
    assert defaults[PaperSystemProperty.MAX_CUSTOM_CHANNEL_NAME] == '32767'
    assert defaults[PaperSystemProperty.MAX_SIGN_LENGTH] == '80'
    assert defaults[PaperSystemProperty.MAX_VIEW_DISTANCE] == '32'
    assert defaults[PaperSystemProperty.EXCESSIVE_TE_LIMIT] == '750'
    assert defaults[PaperSystemProperty.SOUT_NAGS_TIMEOUT] == '5000'
    assert defaults[PaperSystemProperty.SOUT_NAGS_INTERVAL] == '200'
    assert defaults[PaperSystemProperty.PARSE_YAML_COMMENTS_BY_DEFAULT] == 'true'
    assert defaults[PaperSystemProperty.PAPERCLIP_PATCH_ONLY] == 'false'
    assert defaults[PaperSystemProperty.IGNORE_JAVA_VERSION] == 'false'
    assert defaults[PaperSystemProperty.USE_LEGACY_PLUGIN_LOADING] == 'false'
    assert defaults[PaperSystemProperty.DISABLE_OLD_API_SUPPORT] == 'false'
    assert defaults[PaperSystemProperty.PREFER_SPARK_PLUGIN] == 'false'
    assert defaults[PaperSystemProperty.DISABLE_WORLD_SYMLINK_VALIDATION] == 'false'
    assert defaults[PaperSystemProperty.SESSION_API_HOST] == 'https://sessionserver.mojang.com'
    assert defaults[PaperSystemProperty.SERVICES_API_HOST] == 'https://api.minecraftservices.com'
    assert defaults[PaperSystemProperty.PROFILES_API_HOST] == 'https://api.mojang.com'
    assert defaults[PaperSystemProperty.EULA_AGREE] == 'false'
    assert defaults[PaperSystemProperty.LIBRARY_LOADER_CENTRAL_URL] == 'https://maven-central.storage-download.googleapis.com/maven2'
    assert defaults[PaperSystemProperty.DEBUG_ENTITIES_WITH_INVALID_IDS] == 'false'
    assert defaults[PaperSystemProperty.MAX_CHAT_COMMAND_INPUT_SIZE] == '256'


def test_every_property_has_exactly_one_default_semantics() -> None:
    defaults = set(PaperSystemProperty.defaults())
    computed = set(PaperSystemProperty.computed_defaults())
    unset = set(PaperSystemProperty.unset_by_default())

    assert not defaults & computed
    assert not defaults & unset
    assert not computed & unset
    assert defaults | computed | unset == set(PaperSystemProperty)


def test_computed_defaults_match_the_reference() -> None:
    assert set(PaperSystemProperty.computed_defaults()) == {
        PaperSystemProperty.MIN_PRECACHED_DATAFIX_VERSION,
        PaperSystemProperty.WORKER_THREAD_COUNT,
    }


def test_deprecated_properties_match_the_reference() -> None:
    assert PaperSystemProperty.deprecated() == frozenset({PaperSystemProperty.TIMINGS_BYPASS_MAX})


def test_caution_properties_match_the_reference() -> None:
    assert PaperSystemProperty.caution() == frozenset({
        PaperSystemProperty.DISABLE_MIGRATION_DELAY,
        PaperSystemProperty.LIBRARY_LOADER_CENTRAL_URL,
    })


def test_system_properties_serialize_as_dash_d_tokens() -> None:
    jvm = PaperJvmLaunchData(system_properties={
        PaperSystemProperty.EULA_AGREE: True,
        PaperSystemProperty.MAX_SIGN_LENGTH: '100',
        PaperSystemProperty.PAPERCLIP_PATCH_ONLY: False,
    })

    result = jvm.to_tokens()

    assert is_successful(result)
    assert result.unwrap() == [
        '-Dcom.mojang.eula.agree=true',
        '-DPaper.maxSignLength=100',
        '-Dpaperclip.patchonly=false',
    ]


def test_empty_system_property_value_is_rejected() -> None:
    jvm = PaperJvmLaunchData(system_properties={PaperSystemProperty.LET_ME_RELOAD: ''})

    assert not is_successful(jvm.to_tokens())
