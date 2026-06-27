from typing import TypedDict


class Config(TypedDict):
    executable: str | None
    install_directory: str | None


DEFAULT_CONFIG: Config = {
    'executable': None,
    'install_directory': None,
}
