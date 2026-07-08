"""Utility helpers shared between the container and bound-method resolution."""

import inspect
import types
import typing
from typing import Any, Optional, Union


def array_wrap(value: Any) -> list:
    if value is None:
        return []
    return list(value) if isinstance(value, (list, tuple, set)) else [value]


def unwrap_if_closure(value: Any, container: Any = None) -> Any:
    if isinstance(value, types.FunctionType):
        if container is not None:
            return value(container)
        return value()
    return value


def get_parameter_class_name(parameter: inspect.Parameter) -> Optional[type]:
    annotation = parameter.annotation
    if annotation is inspect.Parameter.empty:
        return None

    origin = typing.get_origin(annotation)
    args = typing.get_args(annotation)

    if origin is Union or getattr(origin, '__origin__', None) is Union:
        for arg in args:
            if arg is type(None):
                continue
            if isinstance(arg, type):
                return arg
        return None

    if isinstance(annotation, type):
        if getattr(annotation, '__module__', None) == 'builtins':
            return None
        return annotation

    if origin is not None and isinstance(origin, type):
        return origin

    return None


def is_parameter_required(parameter: inspect.Parameter) -> bool:
    return parameter.kind not in (
        inspect.Parameter.VAR_POSITIONAL,
        inspect.Parameter.VAR_KEYWORD,
    ) and parameter.default == inspect.Parameter.empty


def get_contextual_attribute_from_dependency(parameter: inspect.Parameter) -> Any:
    annotation = parameter.annotation
    if annotation is inspect.Parameter.empty:
        return None
    origin = typing.get_origin(annotation)
    if origin is typing.Annotated:
        args = typing.get_args(annotation)
        for arg in args[1:]:
            if hasattr(arg, 'resolve'):
                return arg
    return None


def resolve_string_to_class(name: str) -> type:
    import importlib
    if '.' in name:
        module_path, class_name = name.rsplit('.', 1)
        module = importlib.import_module(module_path)
        return getattr(module, class_name)
    raise ImportError(f"Cannot unambiguously resolve class '{name}'")


def get_class_for_callable(callback: Any) -> Any:
    """Determine the class name associated with a callable for build-stack tracking."""
    if not callable(callback):
        return False

    if isinstance(callback, str):
        if '::' in callback:
            return callback.split('::')[0]
        if '.' in callback:
            return callback.rsplit('.', 1)[0]
        return False

    if isinstance(callback, (list, tuple)) and len(callback) == 2:
        target = callback[0]
        if isinstance(target, type):
            return target.__name__
        if isinstance(target, str):
            return target
        return type(target).__name__

    if inspect.ismethod(callback):
        bound_to = callback.__self__
        if isinstance(bound_to, type):
            return bound_to.__name__
        return bound_to.__class__.__name__

    if inspect.isfunction(callback):
        qualname = getattr(callback, '__qualname__', '')
        if '.' in qualname and not qualname.endswith('<locals>'):
            parts = qualname.split('.')
            if len(parts) >= 2:
                return parts[-2]

    return False
