from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from armaden.framework.runtime.supervisor import Supervisor
    from armaden.framework.runtime.task import Task


class ConcurrencyFacade:
    def __init__(self, supervisor: 'Supervisor') -> None:
        self._supervisor = supervisor

    def batch(self, *tasks: 'Task'):
        from armaden.framework.runtime.builders.concurrency_builder import ConcurrencyBuilder
        return ConcurrencyBuilder(self._supervisor, list(tasks), mode='parallel')

    def pipeline(self, *tasks: 'Task'):
        from armaden.framework.runtime.builders.concurrency_builder import ConcurrencyBuilder
        return ConcurrencyBuilder(self._supervisor, list(tasks), mode='sequential')
