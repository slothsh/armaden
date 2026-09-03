from __future__ import annotations
from armaden.framework.protocols.bound_method_protocol import BoundMethodProtocol
from armaden.framework.protocols.container_protocol import ContainerProtocol
from collections.abc import Callable, Sequence
from typing import override
import inspect
from armaden.framework.support.reflection import Reflection


type Parameters = dict[object, object]


class BoundMethod(BoundMethodProtocol):
    @staticmethod
    def _add_dependency_for_call_parameter(
        container: ContainerProtocol,
        parameter: inspect.Parameter,
        parameters: Parameters,
        dependencies: list[object],
    ) -> None:
        param_name = parameter.name
        pending_dependencies: list[object] = []

        if param_name in parameters:
            pending_dependencies.append(parameters[param_name])
            del parameters[param_name]
        else:
            cls_hint = Reflection.get_parameter_class_name(parameter)
            if cls_hint is not None:
                if cls_hint in parameters:
                    pending_dependencies.append(parameters[cls_hint])
                    del parameters[cls_hint]
                elif parameter.kind == inspect.Parameter.VAR_POSITIONAL:
                    resolved = container.make(cls_hint)
                    if Reflection.is_object_sequence(resolved):
                        pending_dependencies.extend(resolved)
                    else:
                        pending_dependencies.append(resolved)
                else:
                    pending_dependencies.append(container.make(cls_hint))
            elif parameter.default != inspect.Parameter.empty:
                pending_dependencies.append(parameter.default)
            elif Reflection.is_parameter_required(parameter):
                raise Exception(f"Unable to resolve dependency [{param_name}]")

        dependencies.extend(pending_dependencies)


    @staticmethod
    def _call_bound_method(
        container: ContainerProtocol,
        callback: object,
        default: Callable[..., object],
    ) -> object:
        if not Reflection.is_callback_reference(callback):
            return Reflection.unwrap_if_closure(default)

        method = BoundMethod._normalize_method(callback)
        if container.has_method_binding(method):
            return container.call_method_binding(method, callback[0])

        return Reflection.unwrap_if_closure(default)


    @staticmethod
    def _call_class(
        container: ContainerProtocol,
        target: object,
        parameters: Parameters,
        default_method: str | None = None,
    ) -> object:
        if not isinstance(target, str):
            raise ValueError('Target must be a string for class@method syntax')

        segments = target.split('@')
        method = segments[1] if len(segments) == 2 else default_method

        if method is None:
            raise ValueError('Method not provided.')

        cls_name = segments[0]
        try:
            cls = Reflection.resolve_string_to_class(cls_name)
        except (ImportError, ModuleNotFoundError, AttributeError):
            cls = cls_name

        instance = container.make(cls, parameters)
        return BoundMethod.call(container, [instance, method], parameters)


    @staticmethod
    def _get_call_reflector(callback: object) -> inspect.Signature:
        if isinstance(callback, str) and '::' in callback:
            callback = callback.split('::')
        elif callable(callback) and not (
            inspect.isfunction(callback)
            or inspect.ismethod(callback)
            or isinstance(callback, type)
        ):
            callback = (callback, '__call__')

        if Reflection.is_callback_reference(callback):
            target, method_name = callback
            if not isinstance(method_name, str):
                raise ValueError(f'Method name must be a string, got {method_name!r}')
            if isinstance(target, str):
                try:
                    target = Reflection.resolve_string_to_class(target)
                except (ImportError, ModuleNotFoundError, AttributeError):
                    pass

            if isinstance(target, type):
                unbound = getattr(target, method_name, None)
                if callable(unbound):
                    return inspect.signature(unbound)

            bound = getattr(target, method_name, None)
            if callable(bound):
                return inspect.signature(bound)

            raise ValueError(f'Method {method_name} not found on {target}')

        if not callable(callback):
            raise TypeError(f'Callback must be callable, got {callback!r}')
        return inspect.signature(callback)


    @staticmethod
    def _get_method_dependencies(
        container: ContainerProtocol,
        callback: object,
        parameters: Parameters,
    ) -> list[object]:
        remaining_parameters = dict(parameters)
        dependencies: list[object] = []

        reflector = BoundMethod._get_call_reflector(callback)
        for parameter in reflector.parameters.values():
            BoundMethod._add_dependency_for_call_parameter(
                container,
                parameter,
                remaining_parameters,
                dependencies,
            )

        dependencies.extend(remaining_parameters.values())
        return dependencies


    @staticmethod
    def _is_callable_with_at_sign(callback: object) -> bool:
        return isinstance(callback, str) and '@' in callback


    @staticmethod
    def _normalize_method(callback: Sequence[object]) -> str:
        target = callback[0]
        method = callback[1]
        class_name = target if isinstance(target, str) else type(target).__name__
        return f'{class_name}@{method}'


    @staticmethod
    @override
    def call(
        container: ContainerProtocol,
        callback: object,
        parameters: Parameters | None = None,
        default_method: str | None = None,
    ) -> object:
        resolved_parameters = parameters if parameters is not None else {}

        if isinstance(callback, str) and default_method is None:
            try:
                callback_cls = Reflection.resolve_string_to_class(callback)
                if hasattr(callback_cls, '__call__'):
                    default_method = '__call__'
            except (ImportError, ModuleNotFoundError, AttributeError):
                pass

        if BoundMethod._is_callable_with_at_sign(callback) or default_method:
            return BoundMethod._call_class(
                container,
                callback,
                resolved_parameters,
                default_method,
            )

        def default() -> object:
            dependencies = BoundMethod._get_method_dependencies(
                container,
                callback,
                resolved_parameters,
            )
            if isinstance(callback, str) and '::' in callback:
                parts = callback.split('::')
                target = Reflection.resolve_string_to_class(parts[0])
                return getattr(target, parts[1])(*dependencies)
            if Reflection.is_callback_reference(callback):
                target, method_name = callback
                if not isinstance(method_name, str):
                    raise ValueError(f'Method name must be a string, got {method_name!r}')
                if isinstance(target, str):
                    try:
                        target = Reflection.resolve_string_to_class(target)
                    except (ImportError, ModuleNotFoundError, AttributeError):
                        pass
                return getattr(target, method_name)(*dependencies)
            if not callable(callback):
                raise TypeError(f'Callback must be callable, got {callback!r}')
            return callback(*dependencies)

        return BoundMethod._call_bound_method(container, callback, default)
