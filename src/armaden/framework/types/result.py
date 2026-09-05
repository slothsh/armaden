from armaden.framework.protocols.error_protocol import ErrorProtocol
from returns.result import Result as ReturnsResult

type Result[S] = ReturnsResult[S, ErrorProtocol]
