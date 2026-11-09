from __future__ import annotations

from pathlib import Path
from typing import ClassVar, final, override

from returns.pipeline import is_successful
from returns.result import Success

from armaden.framework.types.result import Result
from armaden.games.minecraft.paper.configuration.paper_configuration_file import (
    PaperConfigurationFile,
)
from armaden.games.minecraft.paper.configuration.paper_world_defaults_configuration import (
    PaperWorldDefaultsConfiguration,
)
from armaden.games.minecraft.paper.configuration.paper_yaml_document import (
    YamlMapping,
    YamlValue,
)


@final
class PaperWorldConfiguration(PaperConfigurationFile):
    FILE_NAME: ClassVar[str] = 'paper-world.yml'

    _defaults_file: PaperWorldDefaultsConfiguration

    def __init__(self, path: Path, defaults_file: PaperWorldDefaultsConfiguration) -> None:
        super().__init__(path)
        self._defaults_file = defaults_file


    @classmethod
    @override
    def defaults(cls) -> YamlMapping:
        return {}


    @override
    def effective(self, path: tuple[str, ...]) -> Result[YamlValue | None]:
        if not is_successful(tree := self.read()):
            return tree.map(lambda _: None)

        node: YamlValue = tree.unwrap()

        for key in path:
            if not isinstance(node, dict) or key not in node:
                return self._defaults_file.effective(path)

            node = node[key]

        return Success(node)


    @override
    def ensure(self, overrides: YamlMapping | None = None) -> Result[None]:
        return self.apply(overrides or {})
