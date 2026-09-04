from enum import Enum
from typing import cast, override

from armaden.framework.facades.facade import Facade
from armaden.framework.protocols.supervisor_protocol import SupervisorProtocol
from armaden.framework.protocols.task_protocol import TaskProtocol


class ConcurrencyFacade[G](Facade):
    @classmethod
    def batch(
        cls,
        *tasks: TaskProtocol[Enum],
    ) -> G:
        root = cast(SupervisorProtocol[G], cls.get_facade_root())
        return root.submit(list(tasks))


    @override
    @classmethod
    def get_facade_accessor(cls) -> object:
        return SupervisorProtocol


    @classmethod
    def pipeline(
        cls,
        *tasks: TaskProtocol[Enum],
    ) -> G:
        root = cast(SupervisorProtocol[G], cls.get_facade_root())
        return root.submit(list(tasks))