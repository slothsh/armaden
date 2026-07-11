from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from armaden.framework.runtime.supervisor import Supervisor


class ProcessFacade:
    def __init__(self, supervisor: 'Supervisor') -> None:
        self._supervisor = supervisor

    def command(self, name: str, argv: list[str]):
        from armaden.framework.runtime.builders.process_builder import ProcessBuilder
        return ProcessBuilder(self._supervisor, name, argv)

    def execute(self, name: str, argv: list[str], **kwargs):
        from armaden.framework.runtime.builders.process_builder import ProcessBuilder
        builder = ProcessBuilder(self._supervisor, name, argv)
        for key, value in kwargs.items():
            getattr(builder, key)(value)
        return builder.build()
