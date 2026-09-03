from enum import StrEnum


class RestartPolicy(StrEnum):
    NEVER = 'never'
    ALWAYS = 'always'
    ON_FAILURE = 'on_failure'
