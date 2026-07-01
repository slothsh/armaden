from typing import TypedDict


class Config(TypedDict):
    executable: str | None
    installDirectory: str | None


DEFAULT_CONFIG: Config = {
    'executable': None,
    'installDirectory': None,
}
