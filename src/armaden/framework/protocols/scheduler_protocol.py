from collections.abc import Callable
from typing import Protocol


class SchedulerProtocol(Protocol):
    def add_job(
        self,
        func: Callable[..., object],
        trigger: object,
        args: list[object],
        id: str,
        replace_existing: bool = False,
    ) -> object: ...

    def get_jobs(self) -> list[object]: ...

    def remove_job(self, name: str) -> object: ...

    def shutdown(self, wait: bool = True) -> object: ...

    def start(self) -> object: ...
