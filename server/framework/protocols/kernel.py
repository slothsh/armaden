from typing import Any, Protocol, TYPE_CHECKING

if TYPE_CHECKING:
    from ..classes.supervisor import Supervisor


class KernelInterface(Protocol):
    supervisor: "Supervisor"
    def version(self) -> str: ...
    def environment(self, name: str, default: str | None = None) -> str | None: ...
    def config(self, key: str, default: Any | None = None) -> Any: ...

    @classmethod
    def instance(cls) -> "ApplicationInterface": ...
