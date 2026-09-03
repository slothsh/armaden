from abc import ABC


class Controller(ABC):
    middleware: dict[str, dict] = {}

    @classmethod
    def get_middleware(cls) -> dict[str, dict]:
        return dict(cls.middleware)

    @classmethod
    def get_middleware_for_method(cls, method_name: str) -> list[str]:
        applicable: list[str] = []
        for alias, config in cls.middleware.items():
            only = config.get('only')
            exclude = config.get('except')
            if only is not None and method_name not in only:
                continue
            if exclude is not None and method_name in exclude:
                continue
            applicable.append(alias)
        return applicable
