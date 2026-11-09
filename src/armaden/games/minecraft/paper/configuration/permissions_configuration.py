from __future__ import annotations

from typing import ClassVar, final, override

from armaden.games.minecraft.paper.configuration.paper_configuration_file import (
    PaperConfigurationFile,
)
from armaden.games.minecraft.paper.configuration.paper_yaml_document import YamlMapping


@final
class PermissionsConfiguration(PaperConfigurationFile):
    FILE_NAME: ClassVar[str] = 'permissions.yml'

    @classmethod
    @override
    def defaults(cls) -> YamlMapping:
        return {}
