from ..protocols.error import ErrorInterface
from collections.abc import Callable, Coroutine
from returns.result import Result as ReturnsResult
from typing import Any
import asyncio

type Result[S] = ReturnsResult[S, ErrorInterface]

type AsyncStreamArg = asyncio.StreamReader | None
type AsyncStreamCallback = Callable[[str], Coroutine[Any, Any, Result[None]]]
