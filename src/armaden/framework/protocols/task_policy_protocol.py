from typing import Protocol


class TaskPolicyProtocol(Protocol):
    @property
    def continue_on_failure(self) -> bool: ...

    @property
    def priority(self) -> int: ...

    @property
    def ready_timeout(self) -> float | None: ...
