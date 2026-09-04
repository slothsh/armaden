from collections.abc import Awaitable, Callable

from armaden.framework.types.result import Result


type ProcessStreamCallback = Callable[
    [str],
    Result[None] | Awaitable[Result[None]],
]