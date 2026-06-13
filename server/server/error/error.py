from enum import StrEnum


class GenericError(StrEnum):
    UNKNOWN = 'an unknown error has occurred'
    EXCEPTION = 'a runtime exception occurred'
    APP_NOT_BOOTSTRAPPED = 'the application has not been properly bootstrapped, or has not been bootstrapped at all'
