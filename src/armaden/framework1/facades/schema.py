from __future__ import annotations

from enum import StrEnum
from typing import TYPE_CHECKING, Callable

from returns.result import Failure, Result, Success

from armaden.framework.errors import Error
from ._registry import get_application
from .db import DB

if TYPE_CHECKING:
    from masoniteorm.blueprint import Blueprint
    from masoniteorm.schema import Schema as SchemaBuilder


class SchemaError(StrEnum):
    OPERATION_FAILED = "a schema operation failed to execute"


class Schema:

    @classmethod
    def _schema(cls, connection: str | None = None) -> 'SchemaBuilder':
        return DB.schema(connection)

    @classmethod
    def create(
        cls,
        table: str,
        callback: Callable[['Blueprint'], None],
        connection: str | None = None,
    ) -> Result[None]:
        try:
            schema = cls._schema(connection)
            with schema.create(table) as blueprint:
                callback(blueprint)
            return Success(None)
        except Exception as exception:
            return Failure(Error(SchemaError.OPERATION_FAILED, details={'exception': exception}))

    @classmethod
    def table(
        cls,
        table: str,
        callback: Callable[['Blueprint'], None],
        connection: str | None = None,
    ) -> Result[None]:
        try:
            schema = cls._schema(connection)
            with schema.table(table) as blueprint:
                callback(blueprint)
            return Success(None)
        except Exception as exception:
            return Failure(Error(SchemaError.OPERATION_FAILED, details={'exception': exception}))

    @classmethod
    def drop(cls, table: str, connection: str | None = None) -> Result[None]:
        try:
            cls._schema(connection).drop(table)
            return Success(None)
        except Exception as exception:
            return Failure(Error(SchemaError.OPERATION_FAILED, details={'exception': exception}))

    @classmethod
    def drop_if_exists(cls, table: str, connection: str | None = None) -> Result[None]:
        try:
            cls._schema(connection).drop_table_if_exists(table)
            return Success(None)
        except Exception as exception:
            return Failure(Error(SchemaError.OPERATION_FAILED, details={'exception': exception}))

    @classmethod
    def rename(
        cls,
        from_table: str,
        to_table: str,
        connection: str | None = None,
    ) -> Result[None]:
        try:
            cls._schema(connection).rename(from_table, to_table)
            return Success(None)
        except Exception as exception:
            return Failure(Error(SchemaError.OPERATION_FAILED, details={'exception': exception}))

    @classmethod
    def has_table(cls, table: str, connection: str | None = None) -> Result[bool]:
        try:
            return Success(bool(cls._schema(connection).has_table(table)))
        except Exception as exception:
            return Failure(Error(SchemaError.OPERATION_FAILED, details={'exception': exception}))

    @classmethod
    def has_column(
        cls,
        table: str,
        column: str,
        connection: str | None = None,
    ) -> Result[bool]:
        try:
            return Success(bool(cls._schema(connection).has_column(table, column)))
        except Exception as exception:
            return Failure(Error(SchemaError.OPERATION_FAILED, details={'exception': exception}))
