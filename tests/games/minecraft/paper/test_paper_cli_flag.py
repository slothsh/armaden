from __future__ import annotations

from typing import cast

from returns.pipeline import is_successful

from armaden.framework.api.error import Error
from armaden.games.minecraft.paper.enums import PaperCliFlag, PaperCliFlagError
from tests.games.minecraft.paper.paper_reference import CLI_ARGUMENTS_SNAPSHOT, CLI_ARGUMENTS_URL

DOCUMENTED_TOKENS: dict[str, PaperCliFlag] = {
    '-?': PaperCliFlag.HELP,
    '--help': PaperCliFlag.HELP,
    '-C': PaperCliFlag.COMMANDS_SETTINGS,
    '--commands-settings': PaperCliFlag.COMMANDS_SETTINGS,
    '-P': PaperCliFlag.PLUGINS,
    '--plugins': PaperCliFlag.PLUGINS,
    '-S': PaperCliFlag.SPIGOT_SETTINGS,
    '--spigot-settings': PaperCliFlag.SPIGOT_SETTINGS,
    '-W': PaperCliFlag.UNIVERSE,
    '--universe': PaperCliFlag.UNIVERSE,
    '--world-container': PaperCliFlag.UNIVERSE,
    '--world-dir': PaperCliFlag.UNIVERSE,
    '--add-extra-plugin-dir': PaperCliFlag.ADD_PLUGIN_DIR,
    '--add-plugin-dir': PaperCliFlag.ADD_PLUGIN_DIR,
    '--add-extra-plugin-jar': PaperCliFlag.ADD_PLUGIN_JAR,
    '--add-plugin': PaperCliFlag.ADD_PLUGIN_JAR,
    '-b': PaperCliFlag.BUKKIT_SETTINGS,
    '--bukkit-settings': PaperCliFlag.BUKKIT_SETTINGS,
    '-c': PaperCliFlag.CONFIG,
    '--config': PaperCliFlag.CONFIG,
    '--demo': PaperCliFlag.DEMO,
    '--bonusChest': PaperCliFlag.BONUS_CHEST,
    '--eraseCache': PaperCliFlag.ERASE_CACHE,
    '--forceUpgrade': PaperCliFlag.FORCE_UPGRADE,
    '-h': PaperCliFlag.HOST,
    '--host': PaperCliFlag.HOST,
    '--server-ip': PaperCliFlag.HOST,
    '--initSettings': PaperCliFlag.INIT_SETTINGS,
    '--jfrProfile': PaperCliFlag.JFR_PROFILE,
    '--noconsole': PaperCliFlag.NOCONSOLE,
    '--nogui': PaperCliFlag.NOGUI,
    '--nojline': PaperCliFlag.NOJLINE,
    '-o': PaperCliFlag.ONLINE_MODE,
    '--online-mode': PaperCliFlag.ONLINE_MODE,
    '-p': PaperCliFlag.PORT,
    '--port': PaperCliFlag.PORT,
    '--server-port': PaperCliFlag.PORT,
    '--paper': PaperCliFlag.PAPER_SETTINGS,
    '--paper-settings': PaperCliFlag.PAPER_SETTINGS,
    '--paper-dir': PaperCliFlag.PAPER_DIR,
    '--paper-settings-directory': PaperCliFlag.PAPER_DIR,
    '--pidFile': PaperCliFlag.PID_FILE,
    '--recreateRegionFiles': PaperCliFlag.RECREATE_REGION_FILES,
    '-s': PaperCliFlag.MAX_PLAYERS,
    '--max-players': PaperCliFlag.MAX_PLAYERS,
    '--size': PaperCliFlag.MAX_PLAYERS,
    '--safeMode': PaperCliFlag.SAFE_MODE,
    '--server-name': PaperCliFlag.SERVER_NAME,
    '--serverId': PaperCliFlag.SERVER_ID,
    '-v': PaperCliFlag.VERSION,
    '--version': PaperCliFlag.VERSION,
    '-w': PaperCliFlag.LEVEL_NAME,
    '--level-name': PaperCliFlag.LEVEL_NAME,
    '--world': PaperCliFlag.LEVEL_NAME,
}


def test_reference_snapshot_is_recorded() -> None:
    assert CLI_ARGUMENTS_URL == 'https://docs.papermc.io/paper/reference/cli-arguments/'
    assert CLI_ARGUMENTS_SNAPSHOT['commit'] == '2f8f228'


def test_every_documented_token_maps_to_one_canonical_flag() -> None:
    for token, canonical in DOCUMENTED_TOKENS.items():
        result = PaperCliFlag.from_token(token)

        assert is_successful(result)
        assert result.unwrap() is canonical


def test_alias_registry_covers_exactly_the_documented_tokens() -> None:
    assert set(PaperCliFlag.aliases()) == set(DOCUMENTED_TOKENS)


def test_unknown_token_is_rejected() -> None:
    result = PaperCliFlag.from_token('--not-a-paper-flag')

    assert not is_successful(result)
    error = cast(Error, result.failure())
    assert error.kind is PaperCliFlagError.UNKNOWN_FLAG
    assert error.details == {'token': '--not-a-paper-flag'}


def test_documented_defaults_match_the_reference() -> None:
    assert PaperCliFlag.defaults() == {
        PaperCliFlag.BUKKIT_SETTINGS: 'bukkit.yml',
        PaperCliFlag.COMMANDS_SETTINGS: 'commands.yml',
        PaperCliFlag.CONFIG: 'server.properties',
        PaperCliFlag.PAPER_DIR: 'config',
        PaperCliFlag.PAPER_SETTINGS: 'paper.yml',
        PaperCliFlag.PLUGINS: 'plugins',
        PaperCliFlag.SERVER_NAME: 'Unknown Server',
        PaperCliFlag.SPIGOT_SETTINGS: 'spigot.yml',
        PaperCliFlag.UNIVERSE: '.',
    }


def test_value_taking_flags_match_the_reference() -> None:
    assert PaperCliFlag.value_flags() == frozenset({
        PaperCliFlag.BUKKIT_SETTINGS,
        PaperCliFlag.COMMANDS_SETTINGS,
        PaperCliFlag.CONFIG,
        PaperCliFlag.HOST,
        PaperCliFlag.LEVEL_NAME,
        PaperCliFlag.MAX_PLAYERS,
        PaperCliFlag.ONLINE_MODE,
        PaperCliFlag.PAPER_DIR,
        PaperCliFlag.PAPER_SETTINGS,
        PaperCliFlag.PID_FILE,
        PaperCliFlag.PLUGINS,
        PaperCliFlag.PORT,
        PaperCliFlag.SERVER_ID,
        PaperCliFlag.SERVER_NAME,
        PaperCliFlag.SPIGOT_SETTINGS,
        PaperCliFlag.UNIVERSE,
    })


def test_repeatable_flags_match_the_reference() -> None:
    assert PaperCliFlag.repeatable_flags() == frozenset({
        PaperCliFlag.ADD_PLUGIN_DIR,
        PaperCliFlag.ADD_PLUGIN_JAR,
    })


def test_path_valued_flags_are_classified() -> None:
    assert PaperCliFlag.path_flags() == frozenset({
        PaperCliFlag.ADD_PLUGIN_DIR,
        PaperCliFlag.ADD_PLUGIN_JAR,
        PaperCliFlag.BUKKIT_SETTINGS,
        PaperCliFlag.COMMANDS_SETTINGS,
        PaperCliFlag.CONFIG,
        PaperCliFlag.PAPER_DIR,
        PaperCliFlag.PAPER_SETTINGS,
        PaperCliFlag.PID_FILE,
        PaperCliFlag.PLUGINS,
        PaperCliFlag.SPIGOT_SETTINGS,
        PaperCliFlag.UNIVERSE,
    })


def test_legacy_paper_settings_flag_is_migration_only() -> None:
    assert PaperCliFlag.migration_only_flags() == frozenset({PaperCliFlag.PAPER_SETTINGS})


def test_help_and_version_prevent_the_server_from_starting() -> None:
    assert PaperCliFlag.server_preventing_flags() == frozenset({
        PaperCliFlag.HELP,
        PaperCliFlag.VERSION,
    })


def test_init_settings_is_settings_only() -> None:
    assert PaperCliFlag.settings_only_flags() == frozenset({PaperCliFlag.INIT_SETTINGS})


def test_server_properties_counterparts_match_the_reference() -> None:
    assert PaperCliFlag.server_properties_counterparts() == {
        PaperCliFlag.HOST: 'server-ip',
        PaperCliFlag.LEVEL_NAME: 'level-name',
        PaperCliFlag.MAX_PLAYERS: 'max-players',
        PaperCliFlag.ONLINE_MODE: 'online-mode',
        PaperCliFlag.PORT: 'server-port',
    }


def test_value_and_repeatable_classifications_are_disjoint() -> None:
    assert not (PaperCliFlag.value_flags() & PaperCliFlag.repeatable_flags())


def test_every_flag_is_value_taking_repeatable_or_boolean() -> None:
    classified = PaperCliFlag.value_flags() | PaperCliFlag.repeatable_flags()
    boolean_flags = set(PaperCliFlag) - classified

    assert len(PaperCliFlag) == len(classified) + len(boolean_flags)
    assert PaperCliFlag.DEMO in boolean_flags
    assert PaperCliFlag.HELP in boolean_flags


def test_flags_preserve_the_documented_spelling() -> None:
    assert PaperCliFlag.BONUS_CHEST.value == '--bonusChest'
    assert PaperCliFlag.ERASE_CACHE.value == '--eraseCache'
    assert PaperCliFlag.FORCE_UPGRADE.value == '--forceUpgrade'
    assert PaperCliFlag.INIT_SETTINGS.value == '--initSettings'
    assert PaperCliFlag.JFR_PROFILE.value == '--jfrProfile'
    assert PaperCliFlag.NOCONSOLE.value == '--noconsole'
    assert PaperCliFlag.NOGUI.value == '--nogui'
    assert PaperCliFlag.NOJLINE.value == '--nojline'
    assert PaperCliFlag.SAFE_MODE.value == '--safeMode'
    assert PaperCliFlag.RECREATE_REGION_FILES.value == '--recreateRegionFiles'
    assert PaperCliFlag.PID_FILE.value == '--pidFile'
    assert PaperCliFlag.SERVER_ID.value == '--serverId'
    assert PaperCliFlag.HELP.value == '-?'
