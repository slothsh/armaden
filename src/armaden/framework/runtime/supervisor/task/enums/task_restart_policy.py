from enum import StrEnum


class TaskRestartPolicy(StrEnum):
    ALWAYS = 'always'
    NEVER = 'never'
    ON_FAILURE = 'on_failure'
