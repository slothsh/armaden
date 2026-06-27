import inspect

from ..utils.container import (
    get_parameter_class_name,
    is_parameter_required,
    resolve_string_to_class,
    unwrap_if_closure,
)


class BoundMethod:
    @staticmethod
    def call(container, callback, parameters=None, default_method=None):
        if parameters is None:
            parameters = {}

        if isinstance(callback, str) and default_method is None:
            try:
                callback_cls = resolve_string_to_class(callback)
                if hasattr(callback_cls, '__call__'):
                    default_method = '__call__'
            except (ImportError, ModuleNotFoundError, AttributeError):
                pass

        if BoundMethod._is_callable_with_at_sign(callback) or default_method:
            return BoundMethod._call_class(container, callback, parameters, default_method)

        def _default():
            dependencies = BoundMethod._get_method_dependencies(container, callback, parameters)
            if isinstance(callback, str) and '::' in callback:
                parts = callback.split('::')
                target = resolve_string_to_class(parts[0])
                return getattr(target, parts[1])(*dependencies)
            if isinstance(callback, (list, tuple)) and len(callback) == 2:
                target, method_name = callback
                if isinstance(target, str):
                    try:
                        target = resolve_string_to_class(target)
                    except (ImportError, ModuleNotFoundError, AttributeError):
                        pass
                return getattr(target, method_name)(*dependencies)
            return callback(*dependencies)

        return BoundMethod._call_bound_method(container, callback, _default)

    @staticmethod
    def _is_callable_with_at_sign(callback):
        return isinstance(callback, str) and '@' in callback

    @staticmethod
    def _call_class(container, target, parameters, default_method=None):
        if not isinstance(target, str):
            raise ValueError("Target must be a string for class@method syntax")

        segments = target.split('@')
        method = segments[1] if len(segments) == 2 else default_method

        if method is None:
            raise ValueError("Method not provided.")

        cls_name = segments[0]
        try:
            cls = resolve_string_to_class(cls_name)
        except (ImportError, ModuleNotFoundError, AttributeError):
            cls = cls_name

        instance = container.make(cls, parameters)
        return BoundMethod.call(container, [instance, method], parameters)

    @staticmethod
    def _call_bound_method(container, callback, default):
        if not isinstance(callback, (list, tuple)) or len(callback) != 2:
            return unwrap_if_closure(default)

        method = BoundMethod._normalize_method(callback)
        if container.has_method_binding(method):
            return container.call_method_binding(method, callback[0])

        return unwrap_if_closure(default)

    @staticmethod
    def _normalize_method(callback):
        target = callback[0]
        method = callback[1]
        class_name = target if isinstance(target, str) else type(target).__name__
        return f"{class_name}@{method}"

    @staticmethod
    def _get_method_dependencies(container, callback, parameters):
        parameters = dict(parameters)
        dependencies = []

        reflector = BoundMethod._get_call_reflector(callback)
        for _, parameter in reflector.parameters.items():
            BoundMethod._add_dependency_for_call_parameter(
                container, parameter, parameters, dependencies
            )

        dependencies.extend(parameters.values())
        return dependencies

    @staticmethod
    def _get_call_reflector(callback):
        if isinstance(callback, str) and '::' in callback:
            callback = callback.split('::')
        elif callable(callback) and not (
            inspect.isfunction(callback)
            or inspect.ismethod(callback)
            or isinstance(callback, type)
        ):
            callback = (callback, '__call__')

        if isinstance(callback, (list, tuple)) and len(callback) == 2:
            target, method_name = callback
            if isinstance(target, str):
                try:
                    target = resolve_string_to_class(target)
                except (ImportError, ModuleNotFoundError, AttributeError):
                    pass

            if isinstance(target, type):
                unbound = getattr(target, method_name, None)
                if callable(unbound):
                    return inspect.signature(unbound)

            bound = getattr(target, method_name, None)
            if callable(bound):
                return inspect.signature(bound)

            raise ValueError(f"Method {method_name} not found on {target}")

        return inspect.signature(callback)

    @staticmethod
    def _add_dependency_for_call_parameter(container, parameter, parameters, dependencies):
        param_name = parameter.name
        pending_dependencies = []

        if param_name in parameters:
            pending_dependencies.append(parameters[param_name])
            del parameters[param_name]
        else:
            cls_hint = get_parameter_class_name(parameter)
            if cls_hint is not None:
                if cls_hint in parameters:
                    pending_dependencies.append(parameters[cls_hint])
                    del parameters[cls_hint]
                elif parameter.kind == inspect.Parameter.VAR_POSITIONAL:
                    resolved = container.make(cls_hint)
                    if isinstance(resolved, (list, tuple)):
                        pending_dependencies.extend(resolved)
                    else:
                        pending_dependencies.append(resolved)
                else:
                    pending_dependencies.append(container.make(cls_hint))
            elif parameter.default != inspect.Parameter.empty:
                pending_dependencies.append(parameter.default)
            elif is_parameter_required(parameter):
                raise Exception(f"Unable to resolve dependency [{param_name}]")

        dependencies.extend(pending_dependencies)
