from __future__ import annotations

from collections.abc import Callable
from typing import cast, override

from returns.result import Failure, Success

from armaden.framework.facades.exceptions.database_error import DatabaseError
from armaden.framework.facades.facade import Facade
from armaden.framework.protocols.database_query_builder_protocol import (
    DatabaseQueryBuilderProtocol,
)
from armaden.framework.protocols.database_resolver_protocol import (
    DatabaseResolverProtocol,
)
from armaden.framework.protocols.database_schema_builder_protocol import (
    DatabaseSchemaBuilderProtocol,
)
from armaden.framework.runtime.error.error import Error
from armaden.framework.types.database import DatabaseBindings
from armaden.framework.types.result import Result


class DatabaseFacade(Facade):
    @override
    @classmethod
    def get_facade_accessor(cls) -> object:
        return 'database.resolver'


    @classmethod
    def begin_transaction(cls, name: str | None = None) -> Result[None]:
        try:
            _ = cls._resolver().begin_transaction(name or cls._default_connection())
            return Success(None)
        except Exception as exception:
            return Failure(Error(DatabaseError.TRANSACTION_FAILED, details={
                'exception': exception,
            }))


    @classmethod
    def commit(cls, name: str | None = None) -> Result[None]:
        try:
            _ = cls._resolver().commit(name or cls._default_connection())
            return Success(None)
        except Exception as exception:
            return Failure(Error(DatabaseError.TRANSACTION_FAILED, details={
                'exception': exception,
            }))


    @classmethod
    def connection(cls, name: str | None = None) -> DatabaseResolverProtocol:
        _ = name
        return cls._resolver()


    @classmethod
    def delete(
        cls,
        query: str,
        bindings: DatabaseBindings = (),
    ) -> Result[int]:
        return cls.update(query, bindings)


    @classmethod
    def insert(
        cls,
        query: str,
        bindings: DatabaseBindings = (),
    ) -> Result[bool]:
        return cls.statement(query, bindings)


    @classmethod
    def raw(
        cls,
        query: str,
        bindings: DatabaseBindings = (),
    ) -> Result[object]:
        return cls.statement(query, bindings)


    @classmethod
    def rollback(cls, name: str | None = None) -> Result[None]:
        try:
            _ = cls._resolver().rollback(name or cls._default_connection())
            return Success(None)
        except Exception as exception:
            return Failure(Error(DatabaseError.TRANSACTION_FAILED, details={
                'exception': exception,
            }))


    @classmethod
    def schema(cls, connection: str | None = None) -> DatabaseSchemaBuilderProtocol:
        return cls._resolver().get_schema_builder(
            connection or cls._default_connection(),
        )


    @classmethod
    def select(
        cls,
        query: str,
        bindings: DatabaseBindings = (),
    ) -> Result[list[object]]:
        try:
            result = cls._resolver().statement(
                query,
                bindings,
                connection=cls._default_connection(),
            )
            if isinstance(result, list):
                return Success(cast(list[object], result))
            return Success([])
        except Exception as exception:
            return Failure(Error(DatabaseError.QUERY_FAILED, details={
                'exception': exception,
            }))


    @classmethod
    def statement(
        cls,
        query: str,
        bindings: DatabaseBindings = (),
    ) -> Result[bool]:
        try:
            _ = cls._resolver().statement(
                query,
                bindings,
                connection=cls._default_connection(),
            )
            return Success(True)
        except Exception as exception:
            return Failure(Error(DatabaseError.QUERY_FAILED, details={
                'exception': exception,
            }))


    @classmethod
    def table(
        cls,
        name: str,
        connection: str | None = None,
    ) -> DatabaseQueryBuilderProtocol:
        return cls._resolver().get_query_builder(
            connection or cls._default_connection(),
        ).table(name)


    @classmethod
    def transaction(
        cls,
        callback: Callable[[], object],
        name: str | None = None,
    ) -> Result[object]:
        try:
            with cls._resolver().transaction(name or cls._default_connection()):
                return Success(callback())
        except Exception as exception:
            return Failure(Error(DatabaseError.TRANSACTION_FAILED, details={
                'exception': exception,
            }))


    @classmethod
    def update(
        cls,
        query: str,
        bindings: DatabaseBindings = (),
    ) -> Result[int]:
        try:
            result = cls._resolver().statement(
                query,
                bindings,
                connection=cls._default_connection(),
            )
            return Success(result if isinstance(result, int) else 0)
        except Exception as exception:
            return Failure(Error(DatabaseError.QUERY_FAILED, details={
                'exception': exception,
            }))


    @classmethod
    def _default_connection(cls) -> str:
        application = cls.get_facade_application()
        if application is not None:
            configured = application.make('database.default')
            if isinstance(configured, str):
                return configured
        details = cls._resolver().get_connection_details()
        configured = details.get('default', 'default')
        return configured if isinstance(configured, str) else 'default'


    @classmethod
    def _resolver(cls) -> DatabaseResolverProtocol:
        return cast(DatabaseResolverProtocol, cls.get_facade_root())
