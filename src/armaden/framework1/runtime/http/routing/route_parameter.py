import re

_PARAM_PATTERN = re.compile(r'\{(\w+)(?::(\w+))?\}')

_CONSTRAINT_MAP: dict[str, type] = {
    'int': int,
    'str': str,
    'float': float,
    'uuid': str,
    'path': str,
}

_CONSTRAINT_FASTAPI: dict[str, str] = {
    'int': ':int',
    'str': '',
    'float': ':float',
    'uuid': ':uuid',
    'path': ':path',
}


class RouteParameter:
    @classmethod
    def parse(cls, path: str) -> tuple[str, dict[str, type]]:
        parameters: dict[str, type] = {}

        def _replace(match: re.Match) -> str:
            name = match.group(1)
            constraint = match.group(2) or 'str'
            if constraint not in _CONSTRAINT_MAP:
                constraint = 'str'
            parameters[name] = _CONSTRAINT_MAP[constraint]
            suffix = _CONSTRAINT_FASTAPI[constraint]
            return f'{{{name}{suffix}}}'

        fastapi_path = _PARAM_PATTERN.sub(_replace, path)
        return fastapi_path, parameters
