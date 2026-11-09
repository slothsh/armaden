from __future__ import annotations

from pathlib import Path

from returns.pipeline import is_successful

from armaden.games.minecraft.paper.configuration.bukkit_configuration import (
    BukkitConfiguration,
)
from armaden.games.minecraft.paper.configuration.commands_configuration import (
    CommandsConfiguration,
)
from armaden.games.minecraft.paper.configuration.help_configuration import (
    HelpConfiguration,
)
from armaden.games.minecraft.paper.configuration.permissions_configuration import (
    PermissionsConfiguration,
)
from armaden.games.minecraft.paper.configuration.spigot_configuration import (
    SpigotConfiguration,
)
from tests.games.minecraft.paper.configuration.config_support import at
from tests.games.minecraft.paper.paper_reference import (
    COMMANDS_CONFIGURATION_URL,
    HELP_CONFIGURATION_URL,
    PERMISSIONS_CONFIGURATION_URL,
    SPIGOT_CONFIGURATION_SNAPSHOT,
    SPIGOT_CONFIGURATION_URL,
)


def test_spigot_reference_snapshot_is_recorded() -> None:
    assert SPIGOT_CONFIGURATION_URL == 'https://docs.papermc.io/paper/reference/spigot-configuration/'
    assert SPIGOT_CONFIGURATION_SNAPSHOT['commit'] == '09e1a6a'


def test_spigot_defaults_match_representative_reference_values() -> None:
    defaults = SpigotConfiguration.defaults()

    assert at(defaults, ('settings', 'sample-count')) == 12
    assert at(defaults, ('settings', 'restart-script')) == './start.sh'
    assert at(defaults, ('settings', 'attribute', 'maxHealth')) == {'max': 1024.0}
    assert at(defaults, ('settings', 'netty-threads')) == 4
    assert at(defaults, ('advancements', 'disabled')) == ['minecraft:story/disabled']
    assert at(defaults, ('messages', 'whitelist')) == 'You are not whitelisted on this server!'
    assert at(defaults, ('config-version',)) == ''
    assert at(defaults, ('world-settings', 'default', 'hopper-amount')) == 1
    assert at(defaults, ('world-settings', 'default', 'seed-mineshaft')) == 'default'
    assert at(defaults, ('world-settings', 'default', 'seed-shipwreck')) == 165745295
    assert at(defaults, ('world-settings', 'default', 'entity-activation-range', 'animals')) == 32
    assert at(defaults, ('world-settings', 'default', 'entity-activation-range', 'wake-up-inactive', 'animals-every')) == 1200
    assert at(defaults, ('world-settings', 'default', 'hunger', 'combat-exhaustion')) == 0.1
    assert at(defaults, ('world-settings', 'default', 'growth', 'cactus-modifier')) == 100
    assert at(defaults, ('world-settings', 'default', 'max-tick-time')) == {'tile': 50, 'entity': 50}
    assert at(defaults, ('world-settings', 'default', 'view-distance')) == 'default'
    assert at(defaults, ('world-settings', 'default', 'verbose')) is False
    assert at(defaults, ('commands', 'replace-commands')) == ['setblock', 'summon', 'testforblock', 'tellraw']
    assert at(defaults, ('commands', 'spam-exclusions')) == ['/skill']
    assert at(defaults, ('stats', 'forced-stats')) == {}


def test_spigot_world_settings_follow_the_documented_per_world_override_scope(tmp_path: Path) -> None:
    path = tmp_path / 'spigot.yml'
    _ = path.write_text(
        'world-settings:\n  default:\n    view-distance: default\n  custom_world:\n    view-distance: 8\n',
        encoding='utf-8',
    )
    configuration = SpigotConfiguration(path)

    tree = configuration.read()

    assert is_successful(tree)
    assert tree.unwrap() is not None
    assert at(tree.unwrap(), ('world-settings', 'custom_world')) == {'view-distance': 8}
    assert at(tree.unwrap(), ('world-settings', 'default', 'view-distance')) == 'default'

    assert is_successful(configuration.apply({'world-settings': {'another_world': {'view-distance': 12}}}))
    tree = configuration.read()
    assert tree.unwrap() is not None
    assert at(tree.unwrap(), ('world-settings', 'another_world')) == {'view-distance': 12}
    assert at(tree.unwrap(), ('world-settings', 'default', 'view-distance')) == 'default'


def test_commands_reference_snapshot_is_recorded() -> None:
    assert COMMANDS_CONFIGURATION_URL == 'https://docs.papermc.io/paper/reference/bukkit-commands-configuration/'
    assert CommandsConfiguration.FILE_NAME == 'commands.yml'


def test_commands_defaults_match_the_reference() -> None:
    assert CommandsConfiguration.defaults() == {
        'command-block-overrides': [],
        'ignore-vanilla-permissions': False,
        'aliases': {'icanhasbukkit': ['version $1-']},
    }


def test_commands_allows_alias_entries_with_string_targets(tmp_path: Path) -> None:
    configuration = CommandsConfiguration(tmp_path / 'commands.yml')

    result = configuration.apply({'aliases': {'icanhasbukkit': [], 'stop-all': ['stop', 'save-all']}})

    assert is_successful(result)
    tree = configuration.read()
    assert tree.unwrap() == {
        'aliases': {'icanhasbukkit': [], 'stop-all': ['stop', 'save-all']}
    }


def test_help_reference_snapshot_is_recorded() -> None:
    assert HELP_CONFIGURATION_URL == 'https://docs.papermc.io/paper/reference/bukkit-help-configuration/'
    assert HelpConfiguration.FILE_NAME == 'help.yml'


def test_help_defaults_match_the_reference() -> None:
    assert HelpConfiguration.defaults() == {
        'general-topics': {},
        'index-topics': {},
        'amended-topics': {},
        'ignore-plugins': [],
        'command-topics-in-master-index': True,
    }


def test_help_supports_custom_topic_entries(tmp_path: Path) -> None:
    configuration = HelpConfiguration(tmp_path / 'help.yml')

    result = configuration.apply({
        'general-topics': {'rules': {'shortText': 'The rules', 'fullText': 'See &cwebsite&f for the rules.', 'permission': ''}},
        'index-topics': {'Default': {'shortText': 'Index', 'preamble': '', 'permission': '', 'commands': ['rules']}},
        'amended-topics': {'/stop': {'shortText': '<text>', 'fullText': '<text>', 'permission': 'bukkit.command.stop'}},
        'ignore-plugins': ['All'],
    })

    assert is_successful(result)
    tree = configuration.read()
    assert tree.unwrap() is not None
    assert at(tree.unwrap(), ('general-topics', 'rules', 'fullText')) == 'See &cwebsite&f for the rules.'
    assert at(tree.unwrap(), ('index-topics', 'Default', 'commands')) == ['rules']
    assert at(tree.unwrap(), ('ignore-plugins',)) == ['All']


def test_permissions_reference_snapshot_is_recorded() -> None:
    assert PERMISSIONS_CONFIGURATION_URL == 'https://docs.papermc.io/paper/reference/bukkit-permissions-configuration/'
    assert PermissionsConfiguration.FILE_NAME == 'permissions.yml'


def test_permissions_have_no_static_defaults() -> None:
    assert PermissionsConfiguration.defaults() == {}


def test_permissions_support_documented_entries(tmp_path: Path) -> None:
    configuration = PermissionsConfiguration(tmp_path / 'permissions.yml')

    result = configuration.apply({
        'bukkit.command.kill': {
            'description': 'Allows you to kill players',
            'default': 'op',
            'children': {'bukkit.command.kill.player': True},
        },
    })

    assert is_successful(result)
    tree = configuration.read()
    assert tree.unwrap() is not None
    assert at(tree.unwrap(), ('bukkit.command.kill', 'default')) == 'op'
    assert at(tree.unwrap(), ('bukkit.command.kill', 'children')) == {'bukkit.command.kill.player': True}


def test_bukkit_worlds_section_stays_user_owned(tmp_path: Path) -> None:
    path = tmp_path / 'bukkit.yml'
    _ = path.write_text(
        'worlds:\n  custom_world:\n    generator: my_plugin:flatlands\n',
        encoding='utf-8',
    )
    configuration = BukkitConfiguration(path)

    result = configuration.apply({'settings': {'connection-throttle': 2000}})

    assert is_successful(result)
    tree = configuration.read()
    assert tree.unwrap() is not None
    assert at(tree.unwrap(), ('worlds', 'custom_world')) == {'generator': 'my_plugin:flatlands'}
