from __future__ import annotations

import re
from typing import ClassVar, override

from armaden.framework.protocols.route_parameter_protocol import RouteParameterProtocol


class RouteParameter(RouteParameterProtocol):
    _CONSTRAINT_FASTAPI: ClassVar[dict[str, str]] = {
        'float': ':float',
        'int': ':int',
        'path': ':path',
        'str': '',
        'uuid': ':uuid',
    }
    _CONSTRAINT_TYPES: ClassVar[dict[str, type[object]]] = {
        'float': float,
        'int': int,
        'path': str,
        'str': str,
        'uuid': str,
    }
    _PARAMETER_PATTERN: ClassVar[re.Pattern[str]] = re.compile(
        r'\{(\w+)(?::(\w+))?\}',
    )

    @override
    @classmethod
    def parse(cls, path: str) -> tuple[str, dict[str, type[object]]]:
        parameters: dict[str, type[object]] = {}

        def replace(match: re.Match[str]) -> str:
            name = match.group(1)
            constraint = match.group(2) or 'str'
            if constraint not in cls._CONSTRAINT_TYPES:
                constraint = 'str'
            parameters[name] = cls._CONSTRAINT_TYPES[constraint]
            return f'{{{name}{cls._CONSTRAINT_FASTAPI[constraint]}}}'

        return cls._PARAMETER_PATTERN.sub(replace, path), parameters
