from __future__ import annotations

from dataclasses import replace
from enum import StrEnum
from pathlib import Path
from typing import final

from returns.pipeline import is_successful
from returns.result import Failure, Success

from armaden.framework.api.error import Error
from armaden.framework.types.result import Result
from armaden.games.minecraft.minecraft_server_config import (
    Config as MinecraftServerConfig,
)
from armaden.games.minecraft.paper.dto import (
    PaperCliArgumentsData,
    PaperJvmLaunchData,
    PaperLaunchConfigData,
)


def resolve_cli_precedence[T](cli_value: T | None, properties_value: T | None) -> T | None:
    return cli_value if cli_value is not None else properties_value


@final
class PaperLaunchCommand:
    def __init__(
        self,
        config: PaperLaunchConfigData,
        *,
        java_executable: str | Path,
        paper_jar: str | Path,
        working_directory: str | Path | None = None,
    ) -> None:
        self._config: PaperLaunchConfigData = config
        self._java_executable: str = str(java_executable)
        self._paper_jar: str = str(paper_jar)
        self._working_directory: Path | None = (
            Path(working_directory) if working_directory is not None else None
        )


    def argv(self) -> Result[list[str]]:
        jvm_tokens = self._config.jvm.to_tokens()

        if not is_successful(jvm_tokens):
            return Failure(jvm_tokens.failure())

        cli_tokens = self._config.cli_arguments.to_tokens(self._working_directory)

        if not is_successful(cli_tokens):
            return Failure(cli_tokens.failure())

        return Success(
            [
                self._java_executable,
                *jvm_tokens.unwrap(),
                '-jar',
                self._paper_jar,
                *cli_tokens.unwrap(),
            ]
        )


    def environment(self) -> dict[str, str]:
        return {
            variable.value: value
            for variable, value in self._config.environment.items()
        }


    @classmethod
    def from_server_config(
        cls,
        config: MinecraftServerConfig,
        *,
        paper_jar: str | Path,
        java_executable: str | Path | None = None,
        working_directory: str | Path | None = None,
    ) -> Result[PaperLaunchCommand]:
        java_group = config.get('java') or {}
        executable = str(java_executable) if java_executable is not None else java_group.get('executable')

        if executable is None:
            return Failure(
                Error(PaperLaunchCommandError.MISSING_JAVA_EXECUTABLE, details={'java': java_group})
            )

        jvm_group = config.get('jvm') or {}
        arguments_group = config.get('arguments') or {}
        extra = arguments_group.get('extra') or []

        parsed = PaperCliArgumentsData.from_tokens(list(extra))

        if not is_successful(parsed):
            return Failure(parsed.failure())

        cli_arguments = replace(
            parsed.unwrap(),
            nogui=parsed.unwrap().nogui or bool(arguments_group.get('nogui')),
        )
        jvm = PaperJvmLaunchData(
            initial_memory_mb=jvm_group.get('initialMemoryMb'),
            maximum_memory_mb=jvm_group.get('maximumMemoryMb'),
            options=list(jvm_group.get('options') or []),
        )
        launch_config = PaperLaunchConfigData(cli_arguments=cli_arguments, jvm=jvm)

        return Success(
            cls(
                launch_config,
                java_executable=executable,
                paper_jar=paper_jar,
                working_directory=working_directory,
            )
        )


# --- Internal Types ----------------------------------------------------------

class PaperLaunchCommandError(StrEnum):
    MISSING_JAVA_EXECUTABLE = 'no java executable was provided or configured for the paper launch command'
