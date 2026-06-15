from returns.result import Result as ReturnsResult

from ..errors import Error

type Result[S] = ReturnsResult[S, Error]
