from __future__ import annotations

from typing import ClassVar, final, override

from armaden.games.minecraft.paper.configuration.paper_configuration_file import (
    PaperConfigurationFile,
)
from armaden.games.minecraft.paper.configuration.paper_yaml_document import YamlMapping


@final
class BukkitConfiguration(PaperConfigurationFile):
    FILE_NAME: ClassVar[str] = 'bukkit.yml'

    @classmethod
    @override
    def defaults(cls) -> YamlMapping:
        return {
            'settings': {
                'allow-end': True,
                'warn-on-overload': True,
                'permissions-file': 'permissions.yml',
                'update-folder': 'update',
                'plugin-profiling': False,
                'connection-throttle': 4000,
                'query-plugins': True,
                'deprecated-verbose': 'default',
                'shutdown-message': 'Server closed',
                'minimum-api': 'none',
                'use-map-color-cache': True,
                'world-container': 'N/A',
            },
            'spawn-limits': {
                'monsters': 70,
                'animals': 10,
                'water-animals': 5,
                'water-ambient': 20,
                'water-underground-creature': 5,
                'axolotls': 5,
                'ambient': 15,
            },
            'chunk-gc': {
                'period-in-ticks': 600,
            },
            'ticks-per': {
                'animal-spawns': 400,
                'monster-spawns': 1,
                'water-spawns': 1,
                'water-ambient-spawns': 1,
                'water-underground-creature-spawns': 1,
                'axolotl-spawns': 1,
                'ambient-spawns': 1,
                'autosave': 6000,
            },
            'aliases': 'now-in-commands.yml',
            'worlds': {},
        }
