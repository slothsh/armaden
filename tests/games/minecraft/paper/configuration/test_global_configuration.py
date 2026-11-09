from __future__ import annotations

from pathlib import Path

from returns.pipeline import is_successful

from armaden.games.minecraft.paper.configuration.global_configuration import (
    PaperGlobalConfiguration,
)
from tests.games.minecraft.paper.configuration.config_support import at
from tests.games.minecraft.paper.paper_reference import (
    GLOBAL_CONFIGURATION_SNAPSHOT,
    GLOBAL_CONFIGURATION_URL,
)


def test_reference_snapshot_is_recorded() -> None:
    assert GLOBAL_CONFIGURATION_URL == 'https://docs.papermc.io/paper/reference/global-configuration/'
    assert GLOBAL_CONFIGURATION_SNAPSHOT['commit'] == '09e1a6a'


def test_defaults_cover_the_documented_top_level_sections() -> None:
    assert set(PaperGlobalConfiguration.defaults()) == {
        'anticheat',
        'block-updates',
        'chunk-loading-advanced',
        'chunk-loading-basic',
        'chunk-system',
        'collisions',
        'commands',
        'console',
        'item-validation',
        'messages',
        'misc',
        'packet-limiter',
        'player-auto-save',
        'proxies',
        'scoreboards',
        'spam-limiter',
        'spark',
        'time',
        'unsupported-settings',
        'update-checker',
        'watchdog',
    }


def test_defaults_match_representative_reference_values() -> None:
    defaults = PaperGlobalConfiguration.defaults()

    assert at(defaults, ('anticheat', 'obfuscation', 'items', 'all-models')) == {
        'also-obfuscate': [],
        'dont-obfuscate': ['minecraft:lodestone_tracker'],
        'sanitize-count': True,
    }
    assert at(defaults, ('anticheat', 'obfuscation', 'items', 'enable-item-obfuscation')) is False
    assert at(defaults, ('anticheat', 'obfuscation', 'items', 'model-overrides', 'minecraft:elytra')) == {
        'also-obfuscate': [],
        'dont-obfuscate': ['minecraft:damage'],
        'sanitize-count': True,
    }
    assert at(defaults, ('block-updates', 'disable-chorus-plant-updates')) is False
    assert at(defaults, ('chunk-loading-basic', 'player-max-chunk-generate-rate')) == -1.0
    assert at(defaults, ('chunk-system', 'io-threads')) == -1
    assert at(defaults, ('item-validation', 'book')) == {'author': 8192, 'page': 16384, 'title': 8192}
    assert at(defaults, ('item-validation', 'book-size')) == {'page-max': 2560, 'total-multiplier': 0.98}
    assert at(defaults, ('item-validation', 'display-name')) == 8192
    assert at(defaults, ('messages', 'kick')) == {
        'authentication-servers-down': '<lang:multiplayer.disconnect.authservers_down>',
        'connection-throttle': 'Connection throttled! Please wait before reconnecting.',
        'flying-player': '<lang:multiplayer.disconnect.flying>',
        'flying-vehicle': '<lang:multiplayer.disconnect.flying>',
    }
    assert at(defaults, ('misc', 'compression-level')) == 'default'
    assert at(defaults, ('misc', 'xp-orb-groups-per-area')) == 'default'
    assert at(defaults, ('packet-limiter', 'all-packets')) == {'action': 'KICK', 'interval': 7.0, 'max-packet-rate': 500.0}
    assert at(defaults, ('packet-limiter', 'overrides', 'minecraft:place_recipe')) == {
        'action': 'KICK',
        'interval': 7.0,
        'max-packet-rate': 500.0,
    }
    assert at(defaults, ('proxies', 'velocity')) == {'enabled': False, 'online-mode': True, 'secret': ''}
    assert at(defaults, ('proxies', 'bungee-cord', 'online-mode')) is True
    assert at(defaults, ('spark', 'enabled')) is True
    assert at(defaults, ('time', 'affects-all-worlds')) is False
    assert at(defaults, ('unsupported-settings', 'oversized-item-component-sanitizer')) == {'dont-sanitize': []}
    assert at(defaults, ('update-checker', 'enabled')) is True
    assert at(defaults, ('watchdog',)) == {'early-warning-delay': 10000, 'early-warning-every': 5000}


def test_file_name_matches_the_reference() -> None:
    assert PaperGlobalConfiguration.FILE_NAME == 'paper-global.yml'


def test_ensure_writes_defaults_and_round_trips(tmp_path: Path) -> None:
    configuration = PaperGlobalConfiguration(tmp_path / 'paper-global.yml')

    assert is_successful(configuration.ensure())

    tree = configuration.read()
    assert is_successful(tree)
    assert tree.unwrap() == PaperGlobalConfiguration.defaults()

    typed = configuration.str_value(('messages', 'kick', 'flying-player'))
    assert is_successful(typed) and typed.unwrap() == '<lang:multiplayer.disconnect.flying>'

    rate = configuration.float_value(('packet-limiter', 'all-packets', 'max-packet-rate'))
    assert is_successful(rate) and rate.unwrap() == 500.0


def test_apply_updates_a_nested_leaf_without_losing_others(tmp_path: Path) -> None:
    path = tmp_path / 'paper-global.yml'
    _ = path.write_text(
        'proxies:\n  velocity:\n    enabled: false\n    secret: ""\n',
        encoding='utf-8',
    )
    configuration = PaperGlobalConfiguration(path)

    result = configuration.apply({'proxies': {'velocity': {'secret': 'new-shared-secret'}}})

    assert is_successful(result)
    tree = configuration.read()
    assert is_successful(tree)
    assert tree.unwrap() is not None
    assert at(tree.unwrap(), ('proxies', 'velocity')) == {'enabled': False, 'secret': 'new-shared-secret'}
