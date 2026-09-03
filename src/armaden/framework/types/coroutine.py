from armaden.framework.types.result import Result
from collections.abc import Coroutine, Callable
from typing import Any
import asyncio


type AsyncStreamArg = asyncio.StreamReader | None
type AsyncStreamCallback = Callable[[str], Coroutine[Any, Any, Result[None]]]
