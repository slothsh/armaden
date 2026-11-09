from __future__ import annotations

from typing import ClassVar, final, override

from armaden.games.minecraft.paper.configuration.paper_configuration_file import (
    PaperConfigurationFile,
)
from armaden.games.minecraft.paper.configuration.paper_yaml_document import YamlMapping


@final
class PaperWorldDefaultsConfiguration(PaperConfigurationFile):
    FILE_NAME: ClassVar[str] = 'paper-world-defaults.yml'

    @classmethod
    @override
    def defaults(cls) -> YamlMapping:
        return {
            'anticheat': {
                'anti-xray': {
                    'enabled': False,
                    'engine-mode': 1,
                    'hidden-blocks': [
                        'copper_ore',
                        'deepslate_copper_ore',
                        'raw_copper_block',
                        'gold_ore',
                        'deepslate_gold_ore',
                        'iron_ore',
                        'deepslate_iron_ore',
                        'raw_iron_block',
                        'coal_ore',
                        'deepslate_coal_ore',
                        'lapis_ore',
                        'deepslate_lapis_ore',
                        'mossy_cobblestone',
                        'obsidian',
                        'chest',
                        'diamond_ore',
                        'deepslate_diamond_ore',
                        'redstone_ore',
                        'deepslate_redstone_ore',
                        'clay',
                        'emerald_ore',
                        'deepslate_emerald_ore',
                        'ender_chest'
                    ],
                    'lava-obscures': False,
                    'max-block-height': 64,
                    'replacement-blocks': ['stone', 'oak_planks', 'deepslate'],
                    'update-radius': 2,
                    'use-permission': False,
                },
            },
            'chunks': {
                'auto-save-interval': 'default',
                'delay-chunk-unloads-by': '10s',
                'entity-per-chunk-save-limit': {
                    'experience_orb': -1,
                },
                'fixed-chunk-inhabited-time': -1,
                'flush-regions-on-save': False,
                'max-auto-save-chunks-per-tick': 24,
                'min-chunk-unload-count': 50,
                'min-chunk-unload-fraction': 0.05,
                'prevent-moving-into-unloaded-chunks': False,
            },
            'collisions': {
                'allow-player-cramming-damage': False,
                'allow-vehicle-collisions': True,
                'fix-climbing-bypassing-cramming-rule': False,
                'max-entity-collisions': 8,
                'only-players-collide': False,
            },
            'command-blocks': {
                'force-follow-perm-level': True,
                'permissions-level': 2,
            },
            'entities': {
                'armor-stands': {
                    'do-collision-entity-lookups': True,
                    'tick': True,
                },
                'behavior': {
                    'allow-spider-world-border-climbing': True,
                    'baby-zombie-movement-modifier': 0.5,
                    'cooldown-failed-beehive-releases': True,
                    'disable-chest-cat-detection': False,
                    'disable-creeper-lingering-effect': False,
                    'disable-player-crits': False,
                    'door-breaking-difficulty': {
                        'vindicator': ['NORMAL', 'HARD'],
                    },
                    'ender-dragons-death-always-places-dragon-egg': False,
                    'experience-merge-max-value': -1,
                    'mobs-can-always-pick-up-loot': {
                        'skeletons': False,
                        'zombies': False,
                    },
                    'nerf-pigmen-from-nether-portals': False,
                    'only-merge-items-horizontally': False,
                    'parrots-are-unaffected-by-player-movement': False,
                    'phantoms-do-not-spawn-on-creative-players': True,
                    'phantoms-only-attack-insomniacs': True,
                    'phantoms-spawn-attempt-max-seconds': 119,
                    'phantoms-spawn-attempt-min-seconds': 60,
                    'piglins-guard-chests': True,
                    'pillager-patrols': {
                        'disable': False,
                        'spawn-chance': 0.2,
                        'spawn-delay': {
                            'ticks': 12000,
                            'per-player': False,
                        },
                        'start': {
                            'day': 5,
                            'per-player': False,
                        },
                    },
                    'player-insomnia-start-ticks': 72000,
                    'should-remove-dragon': False,
                    'spawner-nerfed-mobs-should-jump': False,
                    'stuck-entity-poi-retry-delay': 200,
                    'zombie-villager-infection-chance': 'default',
                    'zombies-target-turtle-eggs': True,
                    'inactive-mob-goal-selector-throttle-rate': 'disabled',
                },
                'entities-target-with-follow-range': False,
                'markers': {
                    'tick': True,
                },
                'mob-effects': {
                    'immune-to-wither-effect': True,
                    'spiders-immune-to-poison-effect': True,
                },
                'sniffer': {
                    'boosted-hatch-time': 'default',
                    'hatch-time': 'default',
                },
                'spawning': {
                    'all-chunks-are-slime-chunks': False,
                    'alt-item-despawn-rate': {
                        'enabled': False,
                        'items': {
                            'cobblestone': 300,
                        },
                    },
                    'max-arrow-despawn-invulnerability': 200,
                    'count-all-mobs-for-spawning': False,
                    'creative-arrow-despawn-rate': 'default',
                    'despawn-range-shape': 'ELLIPSOID',
                    'despawn-ranges': {},
                    'despawn-time': {},
                    'disable-mob-spawner-spawn-egg-transformation': False,
                    'duplicate-uuid': {
                        'mode': 'SAFE_REGEN',
                        'safe-regen-delete-range': 32,
                    },
                    'filter-bad-tile-entity-nbt-from-falling-blocks': True,
                    'filtered-entity-tag-nbt-paths': ['Pos', 'Motion', 'sleeping_pos'],
                    'iron-golems-can-spawn-in-air': False,
                    'monster-spawn-max-light-level': 'default',
                    'non-player-arrow-despawn-rate': 'default',
                    'per-player-mob-spawns': True,
                    'scan-for-legacy-ender-dragon': True,
                    'skeleton-horse-thunder-spawn-chance': 'default',
                    'slime-spawn-height': {
                        'slime-chunk': {
                            'maximum': 40,
                        },
                        'surface-biome': {
                            'minimum': 50,
                            'maximum': 70,
                        },
                    },
                    'spawn-limits': {
                        'ambient': -1,
                        'axolotls': -1,
                        'creature': -1,
                        'monster': -1,
                        'underground_water_creature': -1,
                        'water_ambient': -1,
                        'water_creature': -1,
                    },
                    'ticks-per-spawn': {
                        'ambient': -1,
                        'axolotls': -1,
                        'creature': -1,
                        'monster': -1,
                        'underground_water_creature': -1,
                        'water_ambient': -1,
                        'water_creature': -1,
                    },
                    'wandering-trader': {
                        'spawn-chance-failure-increment': 25,
                        'spawn-chance-max': 75,
                        'spawn-chance-min': 25,
                        'spawn-day-length': 24000,
                        'spawn-minute-length': 1200,
                    },
                    'wateranimal-spawn-height': {
                        'maximum': 'default',
                        'minimum': 'default',
                    },
                },
                'tracking-range-y': {
                    'animal': 'default',
                    'display': 'default',
                    'enabled': False,
                    'misc': 'default',
                    'monster': 'default',
                    'other': 'default',
                    'player': 'default',
                },
            },
            'environment': {
                'disable-explosion-knockback': False,
                'disable-ice-and-snow': False,
                'disable-thunder': False,
                'fire-tick-delay': 30,
                'frosted-ice': {
                    'delay': {
                        'max': 40,
                        'min': 20,
                    },
                    'enabled': True,
                },
                'generate-flat-bedrock': False,
                'locate-structures-outside-world-border': False,
                'max-block-ticks': 65536,
                'max-fluid-ticks': 65536,
                'nether-ceiling-void-damage-height': 'disabled',
                'optimize-explosions': False,
                'portal-create-radius': 16,
                'portal-search-radius': 128,
                'portal-search-vanilla-dimension-scaling': True,
                'treasure-maps': {
                    'enabled': True,
                    'find-already-discovered': {
                        'loot-tables': 'default',
                        'villager-trade': False,
                    },
                },
                'void-damage-amount': 4,
                'void-damage-min-build-height-offset': -64,
                'water-over-lava-flow-speed': 5,
            },
            'feature-seeds': {
                'generate-random-seeds-for-all': False,
            },
            'fishing-time-range': {
                'maximum': 600,
                'minimum': 100,
            },
            'fixes': {
                'disable-unloaded-chunk-enderpearl-exploit': False,
                'falling-block-height-nerf': 'disabled',
                'fix-items-merging-through-walls': False,
                'prevent-tnt-from-moving-in-water': False,
                'split-overstacked-loot': True,
                'tnt-entity-height-nerf': 'disabled',
            },
            'hopper': {
                'cooldown-when-full': True,
                'disable-move-event': False,
                'ignore-occluding-blocks': False,
            },
            'lootables': {
                'auto-replenish': False,
                'max-refills': -1,
                'refresh-max': '2d',
                'refresh-min': '12h',
                'reset-seed-on-fill': True,
                'restrict-player-reloot': True,
                'restrict-player-reloot-time': 'disabled',
                'retain-unlooted-shulker-box-loot-table-on-non-player-break': True,
            },
            'maps': {
                'item-frame-cursor-limit': 128,
                'item-frame-cursor-update-interval': 10,
            },
            'max-growth-height': {
                'bamboo': {
                    'max': 16,
                    'min': 11,
                },
                'cactus': 3,
                'reeds': 3,
            },
            'misc': {
                'allow-remote-ender-dragon-respawning': False,
                'alternate-current-update-order': 'HORIZONTAL_FIRST_OUTWARD',
                'disable-end-credits': False,
                'disable-relative-projectile-velocity': False,
                'disable-sprint-interruption-on-attack': False,
                'legacy-ender-pearl-behavior': False,
                'max-leash-distance': 'default',
                'redstone-implementation': 'VANILLA',
                'show-sign-click-command-failure-msgs-to-player': False,
                'update-pathfinding-on-block-update': True,
            },
            'scoreboards': {
                'allow-non-player-entities-on-scoreboards': True,
                'use-vanilla-world-scoreboard-name-coloring': False,
            },
            'spawn': {
                'allow-using-signs-inside-spawn-protection': False,
            },
            'tick-rates': {
                'behavior': {
                    'villager': {
                        'validatenearbypoi': -1,
                    },
                },
                'container-update': 1,
                'dry-farmland': 1,
                'grass-spread': 1,
                'mob-spawner': 1,
                'sensor': {
                    'villager': {
                        'secondarypoisensor': 40,
                    },
                },
                'wet-farmland': 1,
            },
            'unsupported-settings': {
                'disable-world-ticking-when-empty': False,
                'fix-invulnerable-end-crystal-exploit': True,
                'ticking': {
                    'chunks': True,
                    'block-entities': True,
                },
            },
        }
