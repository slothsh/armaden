from __future__ import annotations

from enum import StrEnum
from typing import TYPE_CHECKING, Any, Callable

from returns.result import Failure, Result, Success

from armaden.framework.errors import Error
from ._registry import get_application

if TYPE_CHECKING:
    from masoniteorm.connections import ConnectionResolver
    from masoniteorm.query import QueryBuilder
    from masoniteorm.schema import Schema as SchemaBuilder


class DatabaseError(StrEnum):
    RESOLVER_NOT_REGISTERED = "the database resolver is not registered in the container"
    QUERY_FAILED = "a database query failed to execute"
    TRANSACTION_FAILED = "a database transaction operation failed"
    CONNECTION_FAILED = "a database connection could not be established"


class DB:

    @classmethod
    def _resolver(cls) -> 'ConnectionResolver':
        container = get_application().container
        if not container.has('database.resolver'):
            raise RuntimeError("database.resolver is not registered")
        return container.get('database.resolver')

    @classmethod
    def _default_connection(cls) -> str:
        container = get_application().container
        if container.has('database.default'):
            return container.get('database.default')
        return cls._resolver().get_connection_details().get('default', 'default')

    @classmethod
    def connection(cls, name: str | None = None) -> 'ConnectionResolver':
        return cls._resolver()

    @classmethod
    def table(cls, name: str, connection: str | None = None) -> 'QueryBuilder':
        resolver = cls._resolver()
        return resolver.get_query_builder(connection or cls._default_connection()).table(name)

    @classmethod
    def select(cls, query: str, bindings: tuple = ()) -> Result[list]:
        try:
            resolver = cls._resolver()
            result = resolver.statement(query, bindings, connection=cls._default_connection())
            return Success(result if isinstance(result, list) else (result or []))
        except Exception as exception:
            return Failure(Error(DatabaseError.QUERY_FAILED, details={'exception': exception}))

    @classmethod
    def statement(cls, query: str, bindings: tuple = ()) -> Result[bool]:
        try:
            cls._resolver().statement(query, bindings, connection=cls._default_connection())
            return Success(True)
        except Exception as exception:
            return Failure(Error(DatabaseError.QUERY_FAILED, details={'exception': exception}))

    @classmethod
    def insert(cls, query: str, bindings: tuple = ()) -> Result[bool]:
        return cls.statement(query, bindings)

    @classmethod
    def update(cls, query: str, bindings: tuple = ()) -> Result[int]:
        try:
            result = cls._resolver().statement(
                query, bindings, connection=cls._default_connection()
            )
            return Success(result if isinstance(result, int) else 0)
        except Exception as exception:
            return Failure(Error(DatabaseError.QUERY_FAILED, details={'exception': exception}))

    @classmethod
    def delete(cls, query: str, bindings: tuple = ()) -> Result[int]:
        return cls.update(query, bindings)

    @classmethod
    def raw(cls, query: str, bindings: tuple = ()) -> Result[Any]:
        return cls.statement(query, bindings)

    @classmethod
    def begin_transaction(cls, name: str | None = None) -> Result[None]:
        try:
            cls._resolver().begin_transaction(name or cls._default_connection())
            return Success(None)
        except Exception as exception:
            return Failure(Error(DatabaseError.TRANSACTION_FAILED, details={'exception': exception}))

    @classmethod
    def commit(cls, name: str | None = None) -> Result[None]:
        try:
            cls._resolver().commit(name or cls._default_connection())
            return Success(None)
        except Exception as exception:
            return Failure(Error(DatabaseError.TRANSACTION_FAILED, details={'exception': exception}))

    @classmethod
    def rollback(cls, name: str | None = None) -> Result[None]:
        try:
            cls._resolver().rollback(name or cls._default_connection())
            return Success(None)
        except Exception as exception:
            return Failure(Error(DatabaseError.TRANSACTION_FAILED, details={'exception': exception}))

    @classmethod
    def transaction(cls, callback: Callable, name: str | None = None) -> Result[Any]:
        resolver = cls._resolver()
        connection = name or cls._default_connection()
        try:
            with resolver.transaction(connection):
                return Success(callback())
        except Exception as exception:
            return Failure(Error(DatabaseError.TRANSACTION_FAILED, details={'exception': exception}))

    @classmethod
    def schema(cls, connection: str | None = None) -> 'SchemaBuilder':
        resolver = cls._resolver()
        return resolver.get_schema_builder(connection or cls._default_connection())
