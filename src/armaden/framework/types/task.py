from collections.abc import Awaitable, Callable

from armaden.framework.types.result import Result


type TaskCallback = Callable[
    ...,
    Result[object] | Awaitable[Result[object]],
]

type TaskStatusCallback = Callable[
    ...,
    Result[dict[str, object]] | Awaitable[Result[dict[str, object]]],
]
