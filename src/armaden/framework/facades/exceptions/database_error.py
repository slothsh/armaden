from enum import StrEnum


class DatabaseError(StrEnum):
    CONNECTION_FAILED = 'database connection could not be established'
    QUERY_FAILED = 'database query failed to execute'
    TRANSACTION_FAILED = 'database transaction operation failed'
