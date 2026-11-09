from __future__ import annotations

from typing import ClassVar, final, override

from armaden.games.minecraft.paper.configuration.paper_configuration_file import (
    PaperConfigurationFile,
)
from armaden.games.minecraft.paper.configuration.paper_yaml_document import YamlMapping


@final
class HelpConfiguration(PaperConfigurationFile):
    FILE_NAME: ClassVar[str] = 'help.yml'

    @classmethod
    @override
    def defaults(cls) -> YamlMapping:
        return {
            'general-topics': {},
            'index-topics': {},
            'amended-topics': {},
            'ignore-plugins': [],
            'command-topics-in-master-index': True,
        }
