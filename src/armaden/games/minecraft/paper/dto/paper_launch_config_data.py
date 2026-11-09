from __future__ import annotations

from dataclasses import dataclass, field
from typing import final

from armaden.games.minecraft.paper.dto.paper_cli_arguments_data import PaperCliArgumentsData
from armaden.games.minecraft.paper.dto.paper_jvm_launch_data import PaperJvmLaunchData
from armaden.games.minecraft.paper.enums import PaperEnvironmentVariable


@final
@dataclass
class PaperLaunchConfigData:
    cli_arguments: PaperCliArgumentsData = field(default_factory=PaperCliArgumentsData)
    environment: dict[PaperEnvironmentVariable, str] = field(default_factory=dict)
    jvm: PaperJvmLaunchData = field(default_factory=PaperJvmLaunchData)
