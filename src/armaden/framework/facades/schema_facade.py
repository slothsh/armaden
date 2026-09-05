from __future__ import annotations

from collections.abc import Callable
from typing import override

from returns.result import Failure, Success

from armaden.framework.facades.database_facade import DatabaseFacade
from armaden.framework.facades.exceptions.schema_error import SchemaError
from armaden.framework.facades.facade import Facade
from armaden.framework.protocols.database_schema_builder_protocol import (
    DatabaseSchemaBuilderProtocol,
)
from armaden.framework.runtime.error.error import Error
from armaden.framework.types.result import Result


class SchemaFacade(Facade):
    @override
    @classmethod
    def get_facade_accessor(cls) -> object:
        return 'database.resolver'


    @classmethod
    def create(
        cls,
        table: str,
        callback: Callable[[object], None],
        connection: str | None = None,
    ) -> Result[None]:
        try:
            with cls._schema(connection).create(table) as blueprint:
                callback(blueprint)
            return Success(None)
        except Exception as exception:
            return Failure(Error(SchemaError.OPERATION_FAILED, details={
                'exception': exception,
            }))


    @classmethod
    def drop(cls, table: str, connection: str | None = None) -> Result[None]:
        try:
            _ = cls._schema(connection).drop(table)
            return Success(None)
        except Exception as exception:
            return Failure(Error(SchemaError.OPERATION_FAILED, details={
                'exception': exception,
            }))


    @classmethod
    def drop_if_exists(
        cls,
        table: str,
        connection: str | None = None,
    ) -> Result[None]:
        try:
            _ = cls._schema(connection).drop_table_if_exists(table)
            return Success(None)
        except Exception as exception:
            return Failure(Error(SchemaError.OPERATION_FAILED, details={
                'exception': exception,
            }))


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
            return Failure(Error(SchemaError.OPERATION_FAILED, details={
                'exception': exception,
            }))


    @classmethod
    def has_table(cls, table: str, connection: str | None = None) -> Result[bool]:
        try:
            return Success(bool(cls._schema(connection).has_table(table)))
        except Exception as exception:
            return Failure(Error(SchemaError.OPERATION_FAILED, details={
                'exception': exception,
            }))


    @classmethod
    def rename(
        cls,
        from_table: str,
        to_table: str,
        connection: str | None = None,
    ) -> Result[None]:
        try:
            _ = cls._schema(connection).rename(from_table, to_table)
            return Success(None)
        except Exception as exception:
            return Failure(Error(SchemaError.OPERATION_FAILED, details={
                'exception': exception,
            }))


    @classmethod
    def table(
        cls,
        table: str,
        callback: Callable[[object], None],
        connection: str | None = None,
    ) -> Result[None]:
        try:
            with cls._schema(connection).table(table) as blueprint:
                callback(blueprint)
            return Success(None)
        except Exception as exception:
            return Failure(Error(SchemaError.OPERATION_FAILED, details={
                'exception': exception,
            }))


    @classmethod
    def _schema(cls, connection: str | None) -> DatabaseSchemaBuilderProtocol:
        return DatabaseFacade.schema(connection)
