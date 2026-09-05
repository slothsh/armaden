from typing import cast, override

from armaden.framework.facades.facade import Facade
from armaden.framework.protocols.scheduler_protocol import SchedulerProtocol


class ScheduleFacade(Facade):
    @override
    @classmethod
    def get_facade_accessor(cls) -> object:
        return SchedulerProtocol


    @classmethod
    def get_jobs(cls) -> list[object]:
        root = cast(SchedulerProtocol, cls.get_facade_root())
        return root.get_jobs()


    @classmethod
    def remove_job(cls, name: str) -> object:
        root = cast(SchedulerProtocol, cls.get_facade_root())
        return root.remove_job(name)


    @classmethod
    def shutdown(cls, wait: bool = True) -> object:
        root = cast(SchedulerProtocol, cls.get_facade_root())
        return root.shutdown(wait)


    @classmethod
    def start(cls) -> object:
        root = cast(SchedulerProtocol, cls.get_facade_root())
        return root.start()