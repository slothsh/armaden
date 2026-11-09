from __future__ import annotations

from pathlib import Path

from returns.pipeline import is_successful

from armaden.games.minecraft.paper.configuration.paper_world_configuration import (
    PaperWorldConfiguration,
)
from armaden.games.minecraft.paper.configuration.paper_world_defaults_configuration import (
    PaperWorldDefaultsConfiguration,
)
from tests.games.minecraft.paper.configuration.config_support import at
from tests.games.minecraft.paper.paper_reference import (
    WORLD_CONFIGURATION_SNAPSHOT,
    WORLD_CONFIGURATION_URL,
)


def make_files(tmp_path: Path) -> tuple[PaperWorldDefaultsConfiguration, PaperWorldConfiguration]:
    defaults_file = PaperWorldDefaultsConfiguration(tmp_path / 'config' / 'paper-world-defaults.yml')
    world_file = PaperWorldConfiguration(tmp_path / 'world' / 'paper-world.yml', defaults_file)
    return defaults_file, world_file


def test_reference_snapshot_is_recorded() -> None:
    assert WORLD_CONFIGURATION_URL == 'https://docs.papermc.io/paper/reference/world-configuration/'
    assert WORLD_CONFIGURATION_SNAPSHOT['commit'] == '44a9ebb'


def test_defaults_cover_the_documented_top_level_sections() -> None:
    assert set(PaperWorldDefaultsConfiguration.defaults()) == {
        'anticheat',
        'chunks',
        'collisions',
        'command-blocks',
        'entities',
        'environment',
        'feature-seeds',
        'fishing-time-range',
        'fixes',
        'hopper',
        'lootables',
        'maps',
        'max-growth-height',
        'misc',
        'scoreboards',
        'spawn',
        'tick-rates',
        'unsupported-settings',
    }


def test_defaults_match_representative_reference_values() -> None:
    defaults = PaperWorldDefaultsConfiguration.defaults()

    assert at(defaults, ('anticheat', 'anti-xray')) == {
        'enabled': False,
        'engine-mode': 1,
        'hidden-blocks': [
            'copper_ore', 'deepslate_copper_ore', 'raw_copper_block', 'gold_ore', 'deepslate_gold_ore',
            'iron_ore', 'deepslate_iron_ore', 'raw_iron_block', 'coal_ore', 'deepslate_coal_ore',
            'lapis_ore', 'deepslate_lapis_ore', 'mossy_cobblestone', 'obsidian', 'chest',
            'diamond_ore', 'deepslate_diamond_ore', 'redstone_ore', 'deepslate_redstone_ore',
            'clay', 'emerald_ore', 'deepslate_emerald_ore', 'ender_chest',
        ],
        'lava-obscures': False,
        'max-block-height': 64,
        'replacement-blocks': ['stone', 'oak_planks', 'deepslate'],
        'update-radius': 2,
        'use-permission': False,
    }
    assert at(defaults, ('chunks', 'delay-chunk-unloads-by')) == '10s'
    assert at(defaults, ('collisions', 'max-entity-collisions')) == 8
    assert at(defaults, ('command-blocks', 'permissions-level')) == 2
    assert at(defaults, ('entities', 'spawning', 'per-player-mob-spawns')) is True
    assert at(defaults, ('entities', 'spawning', 'spawn-limits', 'monster')) == -1
    assert at(defaults, ('entities', 'behavior', 'door-breaking-difficulty', 'vindicator')) == ['NORMAL', 'HARD']
    assert at(defaults, ('entities', 'behavior', 'mobs-can-always-pick-up-loot', 'skeletons')) is False
    assert at(defaults, ('entities', 'spawning', 'despawn-ranges')) == {}
    assert at(defaults, ('environment', 'frosted-ice')) == {'delay': {'max': 40, 'min': 20}, 'enabled': True}
    assert at(defaults, ('environment', 'nether-ceiling-void-damage-height')) == 'disabled'
    assert at(defaults, ('fixes', 'falling-block-height-nerf')) == 'disabled'
    assert at(defaults, ('lootables',)) == {
        'auto-replenish': False,
        'max-refills': -1,
        'refresh-max': '2d',
        'refresh-min': '12h',
        'reset-seed-on-fill': True,
        'restrict-player-reloot': True,
        'restrict-player-reloot-time': 'disabled',
        'retain-unlooted-shulker-box-loot-table-on-non-player-break': True,
    }
    assert at(defaults, ('maps', 'item-frame-cursor-limit')) == 128
    assert at(defaults, ('max-growth-height', 'bamboo')) == {'max': 16, 'min': 11}
    assert at(defaults, ('misc', 'redstone-implementation')) == 'VANILLA'
    assert at(defaults, ('misc', 'alternate-current-update-order')) == 'HORIZONTAL_FIRST_OUTWARD'
    assert at(defaults, ('tick-rates', 'sensor', 'villager', 'secondarypoisensor')) == 40
    assert at(defaults, ('unsupported-settings', 'ticking')) == {'chunks': True, 'block-entities': True}


def test_world_defaults_file_name_matches_the_reference() -> None:
    assert PaperWorldDefaultsConfiguration.FILE_NAME == 'paper-world-defaults.yml'
    assert PaperWorldConfiguration.FILE_NAME == 'paper-world.yml'


def test_world_file_defaults_are_sparingly_empty() -> None:
    assert PaperWorldConfiguration.defaults() == {}


def test_world_overrides_stay_sparse_and_inherit_from_defaults(tmp_path: Path) -> None:
    defaults_file, world_file = make_files(tmp_path)

    assert is_successful(defaults_file.ensure())
    assert is_successful(world_file.apply({'entities': {'spawning': {'spawn-limits': {'monster': 90}}}}))

    world_text = (tmp_path / 'world' / 'paper-world.yml').read_text(encoding='utf-8')
    assert 'monster: 90' in world_text
    assert 'lootables' not in world_text
    assert 'anticheat' not in world_text

    override = world_file.effective(('entities', 'spawning', 'spawn-limits', 'monster'))
    inherited = world_file.effective(('anticheat', 'anti-xray', 'enabled'))
    inherited_default = world_file.effective(('lootables', 'auto-replenish'))

    assert is_successful(override) and override.unwrap() == 90
    assert is_successful(inherited) and inherited.unwrap() is False
    assert is_successful(inherited_default) and inherited_default.unwrap() is False


def test_world_inheritance_follows_the_documented_example(tmp_path: Path) -> None:
    defaults_file, world_file = make_files(tmp_path)

    assert is_successful(defaults_file.apply({
        'lootables': {'auto-replenish': True},
        'entities': {'spawning': {'spawn-limits': {
            'ambient': 70,
            'axolotls': 10,
            'creature': 15,
            'monster': 5,
            'underground_water_creature': 5,
            'water_ambient': 5,
            'water_creature': 20,
        }}},
    }))
    assert is_successful(world_file.apply({'entities': {'spawning': {'spawn-limits': {'monster': 90}}}}))

    assert world_file.int_value(('entities', 'spawning', 'spawn-limits', 'monster')).unwrap() == 90
    assert world_file.int_value(('entities', 'spawning', 'spawn-limits', 'ambient')).unwrap() == 70
    assert world_file.int_value(('entities', 'spawning', 'spawn-limits', 'axolotls')).unwrap() == 10
    assert world_file.bool_value(('lootables', 'auto-replenish')).unwrap() is True


def test_ensure_on_a_world_file_never_copies_defaults(tmp_path: Path) -> None:
    defaults_file, world_file = make_files(tmp_path)

    assert is_successful(defaults_file.ensure())
    assert is_successful(world_file.ensure({'lootables': {'auto-replenish': False}}))

    world_text = (tmp_path / 'world' / 'paper-world.yml').read_text(encoding='utf-8')
    assert 'auto-replenish: false' in world_text
    assert 'anticheat:' not in world_text
    assert 'environment:' not in world_text

    tree = world_file.read()
    assert is_successful(tree)
    assert tree.unwrap() == {'lootables': {'auto-replenish': False}}
