from __future__ import annotations

import inspect
import types
import typing
from collections.abc import Sequence
from typing import TypeGuard, cast


type CallbackReference = Sequence[object]


class Reflection:
    @staticmethod
    def get_class_for_callable(callback: object) -> str | bool:
        if not callable(callback):
            return False

        if isinstance(callback, str):
            if '::' in callback:
                return callback.split('::')[0]
            if '.' in callback:
                return callback.rsplit('.', 1)[0]
            return False

        if isinstance(callback, (list, tuple)):
            callback_items = cast(list[object] | tuple[object, ...], callback)
            if len(callback_items) != 2:
                return False
            target = callback_items[0]
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


    @staticmethod
    def get_contextual_attribute_from_dependency(
        parameter: inspect.Parameter,
    ) -> object | None:
        annotation = parameter.annotation
        if annotation is inspect.Parameter.empty:
            return None
        if typing.get_origin(annotation) is typing.Annotated:
            args = typing.get_args(annotation)
            for argument in args[1:]:
                if hasattr(argument, 'resolve'):
                    return argument
        return None


    @staticmethod
    def get_parameter_class_name(parameter: inspect.Parameter) -> type[object] | None:
        annotation = parameter.annotation
        if annotation is inspect.Parameter.empty:
            return None

        origin = typing.get_origin(annotation)
        args = typing.get_args(annotation)

        if origin is types.UnionType:
            for argument in args:
                if argument is type(None):
                    continue
                if isinstance(argument, type):
                    return argument
            return None

        if isinstance(annotation, type):
            if annotation.__module__ == 'builtins':
                return None
            return annotation

        if origin is not None and isinstance(origin, type):
            return origin

        return None


    @staticmethod
    def is_callback_reference(value: object) -> TypeGuard[CallbackReference]:
        if not isinstance(value, (list, tuple)):
            return False
        candidate = cast(Sequence[object], value)
        return len(candidate) == 2


    @staticmethod
    def is_object_sequence(value: object) -> TypeGuard[Sequence[object]]:
        return isinstance(value, (list, tuple))


    @staticmethod
    def is_parameter_required(parameter: inspect.Parameter) -> bool:
        return parameter.kind not in (
            inspect.Parameter.VAR_POSITIONAL,
            inspect.Parameter.VAR_KEYWORD,
        ) and parameter.default == inspect.Parameter.empty


    @staticmethod
    def resolve_string_to_class(name: str) -> type[object]:
        import importlib

        if '.' in name:
            module_path, class_name = name.rsplit('.', 1)
            module = importlib.import_module(module_path)
            return getattr(module, class_name)
        raise ImportError(f"Cannot unambiguously resolve class '{name}'")


    @staticmethod
    def unwrap_if_closure(
        value: object,
        container: object | None = None,
    ) -> object:
        if isinstance(value, types.FunctionType):
            if container is not None:
                return value(container)
            return value()
        return value
