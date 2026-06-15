from typing import Any, Protocol, TYPE_CHECKING

if TYPE_CHECKING:
    from ..utils.types import Result


class ServiceInterface(Protocol):
    def __call__(self, *args: Any, **kwargs: Any) -> "Result[None]": ...
