from __future__ import annotations

from typing import ClassVar, final, override

from armaden.games.minecraft.paper.configuration.paper_configuration_file import (
    PaperConfigurationFile,
)
from armaden.games.minecraft.paper.configuration.paper_yaml_document import YamlMapping


@final
class CommandsConfiguration(PaperConfigurationFile):
    FILE_NAME: ClassVar[str] = 'commands.yml'

    @classmethod
    @override
    def defaults(cls) -> YamlMapping:
        return {
            'command-block-overrides': [],
            'ignore-vanilla-permissions': False,
            'aliases': {
                'icanhasbukkit': ['version $1-'],
            },
        }
