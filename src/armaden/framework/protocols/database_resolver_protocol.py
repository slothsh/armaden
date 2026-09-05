from contextlib import AbstractContextManager
from typing import Protocol

from armaden.framework.protocols.database_query_builder_protocol import (
    DatabaseQueryBuilderProtocol,
)
from armaden.framework.protocols.database_schema_builder_protocol import (
    DatabaseSchemaBuilderProtocol,
)


class DatabaseResolverProtocol(Protocol):
    def begin_transaction(self, connection: str) -> object: ...

    def commit(self, connection: str) -> object: ...

    def get_connection_details(self) -> dict[str, object]: ...

    def get_query_builder(self, connection: str) -> DatabaseQueryBuilderProtocol: ...

    def get_schema_builder(self, connection: str) -> DatabaseSchemaBuilderProtocol: ...

    def rollback(self, connection: str) -> object: ...

    def statement(
        self,
        query: str,
        bindings: tuple[object, ...],
        connection: str,
    ) -> object: ...

    def transaction(self, connection: str) -> AbstractContextManager[object]: ...
