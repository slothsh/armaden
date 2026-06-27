from typing import TypedDict


class Config(TypedDict):
    executable: str | None


DEFAULT_CONFIG: Config = {
    'executable': None,
}
