from typing import Protocol


class TaskPolicyProtocol(Protocol):
    continue_on_failure: bool

    @property
    def priority(self) -> int: ...

    @property
    def ready_timeout(self) -> float | None: ...

    @property
    def restart(self) -> str: ...

    @property
    def retries(self) -> int: ...

    @property
    def retry_backoff(self) -> float: ...

    @property
    def retry_delay(self) -> float: ...

    @property
    def timeout(self) -> float | None: ...
