from __future__ import annotations

import inspect
import logging
import types
from collections.abc import Callable
from typing import ClassVar, cast, override

from armaden.framework.protocols.configuration_protocol import ConfigurationProtocol
from armaden.framework.protocols.container_instance_protocol import (
    ContainerInstanceProtocol,
)
from armaden.framework.protocols.container_protocol import ContainerProtocol
from armaden.framework.runtime.container.bound_method import BoundMethod
from armaden.framework.runtime.container.contextual_attribute import ContextualAttribute
from armaden.framework.runtime.container.contextual_binding_builder import (
    ContextualBindingBuilder,
)
from armaden.framework.runtime.container.exceptions import (
    BindingResolutionException,
    CircularDependencyException,
    EntryNotFoundException,
    LogicException,
)
from armaden.framework.support.array import Array
from armaden.framework.support.reflection import Reflection
from armaden.framework.runtime.container.tags import SelfBuildingTag

logger = logging.getLogger(__name__)

type Binding = dict[str, object]
type Callback = Callable[..., object]


class Container(ContainerProtocol, ContainerInstanceProtocol):
    _instance: ContainerProtocol | None = None
    _TYPE_DEFAULTS: ClassVar[dict[type, object]] = {
        int: 0,
        float: 0.0,
        complex: 0j,
        str: '',
        bool: False,
        bytes: b'',
        bytearray: bytearray(),
        list: list[object](),
        dict: dict[object, object](),
        tuple: (),
        set: set[object](),
        frozenset: frozenset(),
    }

    @override
    def __contains__(self, key: object) -> bool:
        return self.bound(key)


    @override
    def __delitem__(self, key: object) -> None:
        _ = self._bindings.pop(key, None)
        _ = self._instances.pop(key, None)
        _ = self._resolved.pop(key, None)


    @override
    def __getattr__(self, key: str) -> object:
        return self.make(key)


    @override
    def __getitem__(self, key: object) -> object:
        return self.make(key)


    @override
    def __init__(self):
        self._abstract_aliases: dict[object, list[object]] = {}
        self._after_resolving_attribute_callbacks: dict[object, list[Callable[..., object]]] = {}
        self._after_resolving_callbacks: dict[object, list[Callable[..., object]]] = {}
        self._aliases: dict[object, object] = {}
        self._before_resolving_callbacks: dict[object, list[Callable[..., object]]] = {}
        self._bindings: dict[object, Binding] = {}
        self._build_stack: list[object] = []
        self._checked_for_attribute_bindings: dict[object, bool] = {}
        self._checked_for_singleton_or_scoped_attributes: dict[object, object] = {}
        self._contextual: dict[object, dict[object, object]] = {}
        self._contextual_attributes: dict[object, Callback] = {}
        self._deferred_services: dict[object, type] = {}
        self._environment_resolver: Callable[..., object] | None = None
        self._extenders: dict[object, list[Callable[..., object]]] = {}
        self._global_after_resolving_callbacks: list[Callable[..., object]] = []
        self._global_before_resolving_callbacks: list[Callable[..., object]] = []
        self._global_resolving_callbacks: list[Callable[..., object]] = []
        self._instances: dict[object, object] = {}
        self._method_bindings: dict[str, Callback] = {}
        self._rebound_callbacks: dict[object, list[Callable[..., object]]] = {}
        self._resolved: dict[object, bool] = {}
        self._resolving_callbacks: dict[object, list[Callable[..., object]]] = {}
        self._scoped_instances: list[object] = []
        self._tags: dict[str, list[object]] = {}
        self._with: list[dict[object, object]] = []


    @override
    def __setattr__(self, key: str, value: object) -> None:
        if key.startswith('_'):
            object.__setattr__(self, key, value)
        else:
            self.bind(key, value if callable(value) else lambda: value)


    @override
    def __setitem__(self, key: object, value: object) -> None:
        self.bind(key, value if callable(value) else lambda: value)


    def _discover_bind_attributes(self, cls: type) -> None:
        bindings = getattr(cls, '_armaden_bindings', [])
        for bind in bindings:
            if bind.environments:
                if not self._environment_matches(bind.environments):
                    continue
            self.bind(cls, bind.concrete, shared=False)


    def _discover_scoped_attribute(self, cls: type) -> None:
        if getattr(cls, '_armaden_scoped', False):
            self.scoped(cls, cls)


    def _discover_singleton_attribute(self, cls: type) -> None:
        if getattr(cls, '_armaden_singleton', False):
            self.singleton(cls, cls)


    def _environment_matches(self, environments: list[str]) -> bool:
        if self._environment_resolver is None:
            return False
        return self._environment_resolver() in environments


    def _fire_before_callback_array(self, abstract: object, parameters: dict[object, object], callbacks: list[Callable[..., object]]) -> None:
        for callback in callbacks:
            _ = callback(abstract, parameters, self)


    def _fire_callback_array(self, obj: object, callbacks: list[Callable[..., object]]) -> None:
        for callback in callbacks:
            _ = callback(obj, self)


    def _get_callbacks_for_type(self, abstract: object, obj: object, callbacks_per_type: dict[object, list[Callable[..., object]]]) -> list[Callable[..., object]]:
        results: list[Callable[..., object]] = []
        for typ, callbacks in callbacks_per_type.items():
            if typ == abstract or (isinstance(typ, type) and isinstance(obj, typ)):
                results.extend(callbacks)
        return results


    def _is_container_type(self, cls_name: object) -> bool:
        if not isinstance(cls_name, type):
            return False
        return cls_name is Container or issubclass(cls_name, Container)


    def _parse_bind_method(self, method: object) -> str:
        if isinstance(method, (list, tuple)):
            return f'{method[0]}@{method[1]}'
        return str(method)


    def _resolve_config_value(self, key: str) -> object:
        try:
            configuration = self.make(ConfigurationProtocol)
        except BindingResolutionException:
            configuration = None
        if configuration is not None:
            getter = getattr(configuration, 'get', None)
            if callable(getter):
                return getter(key)
        if self.resolved('config'):
            config = self.make('config')
            getter = getattr(config, 'get', None)
            if callable(getter):
                return getter(key)
        app = self.make('app')
        config = getattr(app, 'config', None)
        if callable(config):
            return config(key)
        raise AttributeError('The application does not provide a config method.')


    def _resolve_contextual_marker(self, concrete: object) -> object:
        if not isinstance(concrete, dict):
            return concrete
        marker = cast(dict[str, object], concrete)
        tagged = marker.get('__tagged__')
        if isinstance(tagged, str):
            return self.tagged(tagged)
        config = marker.get('__config__')
        if isinstance(config, str):
            return self._resolve_config_value(config)
        return marker


    def _try_resolve_deferred(self, abstract: object) -> None:
        if abstract not in self._deferred_services:
            return
        provider_class = self._deferred_services.pop(abstract)
        provider = provider_class(self)
        provider.register_bindings()
        provider.register()
        if hasattr(provider, 'boot'):
            provider.boot()


    @override
    def add_contextual_binding(self, concrete: object, abstract: object, implementation: object) -> None:
        self._contextual.setdefault(concrete, {})[self.get_alias(abstract)] = implementation


    @override
    def add_deferred_services(self, services: dict[object, type]) -> None:
        self._deferred_services.update(services)


    @override
    def after_resolving(self, abstract: object, callback: Callable[..., object] | None = None) -> None:
        if callable(abstract) and callback is None:
            self._global_after_resolving_callbacks.append(abstract)
        else:
            if callback is None:
                raise TypeError('A callback is required for a bound abstract.')
            abstract = self.get_alias(abstract)
            self._after_resolving_callbacks.setdefault(abstract, []).append(callback)


    @override
    def after_resolving_attribute(self, attribute: object, callback: Callable[..., object]) -> None:
        self._after_resolving_attribute_callbacks.setdefault(attribute, []).append(callback)


    @override
    def alias(self, abstract: object, alias: object) -> None:
        if alias == abstract:
            raise LogicException(f'[{abstract}] is aliased to itself.')

        self.remove_abstract_alias(alias)
        self._aliases[alias] = abstract
        self._abstract_aliases.setdefault(abstract, []).append(alias)


    @override
    def before_resolving(self, abstract: object, callback: Callable[..., object] | None = None) -> None:
        if callable(abstract) and callback is None:
            self._global_before_resolving_callbacks.append(abstract)
        else:
            if callback is None:
                raise TypeError('A callback is required for a bound abstract.')
            abstract = self.get_alias(abstract)
            self._before_resolving_callbacks.setdefault(abstract, []).append(callback)


    @override
    def bind(self, abstract: object, concrete: object | None = None, shared: bool = False) -> None:
        if callable(abstract) and not inspect.isclass(abstract):
            return self.bind_based_on_closure_return_types(abstract, concrete, shared)

        self.drop_stale_instances(abstract)

        if concrete is None:
            concrete = abstract

        if isinstance(concrete, str):
            concrete = self.get_closure(abstract, concrete)
        elif not callable(concrete):
            raise TypeError(f'Concrete must be a string or callable, got {type(concrete)}')

        self._bindings[abstract] = {'concrete': concrete, 'shared': shared}

        if self.resolved(abstract):
            self.rebound(abstract)


    @override
    def bind_based_on_closure_return_types(self, abstract: Callable[..., object], concrete: object | None = None, shared: bool = False) -> None:
        abstracts = self.closure_return_types(abstract)
        concrete_fn = abstract
        for _name, typ in abstracts.items():
            self.bind(typ, concrete_fn, shared)


    @override
    def bind_if(self, abstract: object, concrete: object | None = None, shared: bool = False) -> None:
        if not self.bound(abstract):
            self.bind(abstract, concrete, shared)


    @override
    def bind_method(self, method: object, callback: Callable[..., object]) -> None:
        self._method_bindings[self._parse_bind_method(method)] = callback


    @override
    def bound(self, abstract: object) -> bool:
        return abstract in self._bindings or abstract in self._instances or self.is_alias(abstract)


    @override
    def build(self, concrete: object) -> object:
        if self._is_container_type(concrete):
            return self

        if callable(concrete) and not inspect.isclass(concrete):
            self._build_stack.append(id(concrete))
            try:
                return concrete(self, self.get_last_parameter_override())
            finally:
                _ = self._build_stack.pop()

        if not inspect.isclass(concrete):
            raise BindingResolutionException(f'Target class [{concrete}] does not exist.')

        if issubclass(concrete, SelfBuildingTag) and concrete not in self._build_stack:
            return self.build_self_building_instance(concrete)

        self._build_stack.append(concrete)
        try:
            constructor = inspect.signature(concrete.__init__)
            params = list(constructor.parameters.values())[1:]

            if concrete.__init__ is object.__init__:
                params = []

            if not params:
                instance = concrete()
                self.fire_after_resolving_attribute_callbacks([], instance)
                return instance

            dependencies = self.resolve_dependencies(params)
            instance = concrete(*dependencies)
            self.fire_after_resolving_attribute_callbacks([], instance)
            return instance
        finally:
            _ = self._build_stack.pop()


    @override
    def build_self_building_instance(self, concrete: type) -> object:
        if not hasattr(concrete, 'new_instance') or not callable(getattr(concrete, 'new_instance')):
            raise BindingResolutionException(f'No newInstance method exists for [{concrete}].')

        self._build_stack.append(concrete)
        try:
            instance = self.call((concrete, 'new_instance'))
            self.fire_after_resolving_attribute_callbacks([], instance)
            return instance
        finally:
            _ = self._build_stack.pop()


    @override
    def call(self, callback: object, parameters: dict[object, object] | None = None, default_method: str | None = None) -> object:
        if parameters is None:
            parameters = {}

        pushed_to_build_stack = False
        class_name = Reflection.get_class_for_callable(callback)

        if class_name and class_name not in self._build_stack:
            self._build_stack.append(class_name)
            pushed_to_build_stack = True

        result = BoundMethod.call(self, callback, parameters, default_method)

        if pushed_to_build_stack:
            _ = self._build_stack.pop()

        return result


    @override
    def call_method_binding(self, method: str, instance: object) -> object:
        return self._method_bindings[method](instance, self)


    @override
    def closure_return_types(self, closure: Callable[..., object]) -> dict[str, type]:
        import typing
        try:
            hints = typing.get_type_hints(closure)
        except Exception:
            return {}
        return_type = hints.get('return')
        if return_type is None:
            return {}

        result: dict[str, type] = {}
        origin = typing.get_origin(return_type)
        args = typing.get_args(return_type)

        if origin is types.UnionType:
            for arg in args:
                if arg is type(None):
                    continue
                if isinstance(arg, type):
                    result[arg.__name__] = arg
        elif isinstance(return_type, type):
            result[return_type.__name__] = return_type

        return result


    @override
    def current_environment_is(self, environments: object) -> bool:
        if self._environment_resolver is None:
            return False
        return bool(self._environment_resolver(environments))


    @override
    def currently_resolving(self) -> object:
        return self._build_stack[-1] if self._build_stack else None


    @override
    def discover_attribute_bindings(self, classes: list[type]) -> None:
        for cls in classes:
            self._discover_bind_attributes(cls)
            self._discover_singleton_attribute(cls)
            self._discover_scoped_attribute(cls)


    @override
    def drop_stale_instances(self, abstract: object) -> None:
        alias = self.get_alias(abstract)
        _ = self._instances.pop(alias, None)
        _ = self._aliases.pop(alias, None)


    @override
    def extend(self, abstract: object, closure: Callable[..., object]) -> None:
        abstract = self.get_alias(abstract)
        if abstract in self._instances:
            self._instances[abstract] = closure(self._instances[abstract], self)
            self.rebound(abstract)
        else:
            self._extenders.setdefault(abstract, []).append(closure)
            if self.resolved(abstract):
                self.rebound(abstract)


    @override
    def factory(self, abstract: object) -> Callable[..., object]:
        return lambda: self.make(abstract)


    @override
    def find_in_contextual_bindings(self, abstract: object) -> object:
        if not self._build_stack:
            return None
        return self._contextual.get(self._build_stack[-1], {}).get(abstract)


    @override
    def fire_after_resolving_attribute_callbacks(self, attributes: list[object], obj: object) -> None:
        for attribute in attributes:
            attr_name = attribute if isinstance(attribute, str) else getattr(attribute, '__name__', str(type(attribute)))
            for callbacks in self._after_resolving_attribute_callbacks.get(attr_name, []):
                _ = callbacks(attribute, obj, self)


    @override
    def fire_after_resolving_callbacks(self, abstract: object, obj: object) -> None:
        self._fire_callback_array(obj, self._global_after_resolving_callbacks)
        self._fire_callback_array(obj, self._get_callbacks_for_type(abstract, obj, self._after_resolving_callbacks))


    @override
    def fire_before_resolving_callbacks(self, abstract: object, parameters: dict[object, object] | None = None) -> None:
        if parameters is None:
            parameters = {}
        self._fire_before_callback_array(abstract, parameters, self._global_before_resolving_callbacks)
        for typ, callbacks in self._before_resolving_callbacks.items():
            if typ == abstract:
                self._fire_before_callback_array(abstract, parameters, callbacks)
            elif isinstance(abstract, type) and isinstance(typ, type) and issubclass(abstract, typ):
                self._fire_before_callback_array(abstract, parameters, callbacks)


    @override
    def fire_resolving_callbacks(self, abstract: object, obj: object) -> None:
        self._fire_callback_array(obj, self._global_resolving_callbacks)
        self._fire_callback_array(obj, self._get_callbacks_for_type(abstract, obj, self._resolving_callbacks))
        self.fire_after_resolving_callbacks(abstract, obj)


    @override
    def flush(self) -> None:
        self._abstract_aliases.clear()
        self._after_resolving_attribute_callbacks.clear()
        self._after_resolving_callbacks.clear()
        self._aliases.clear()
        self._before_resolving_callbacks.clear()
        self._bindings.clear()
        self._build_stack.clear()
        self._checked_for_attribute_bindings.clear()
        self._checked_for_singleton_or_scoped_attributes.clear()
        self._contextual.clear()
        self._contextual_attributes.clear()
        self._extenders.clear()
        self._global_after_resolving_callbacks.clear()
        self._global_before_resolving_callbacks.clear()
        self._global_resolving_callbacks.clear()
        self._instances.clear()
        self._method_bindings.clear()
        self._rebound_callbacks.clear()
        self._resolved.clear()
        self._resolving_callbacks.clear()
        self._scoped_instances.clear()
        self._tags.clear()
        self._with.clear()


    @override
    def forget_extenders(self, abstract: object) -> None:
        alias = self.get_alias(abstract)
        _ = self._extenders.pop(alias, None)


    @override
    def forget_instance(self, abstract: object) -> None:
        _ = self._instances.pop(abstract, None)


    @override
    def forget_instances(self) -> None:
        self._instances.clear()


    @override
    def forget_scoped_instances(self) -> None:
        for scoped in self._scoped_instances:
            if callable(scoped):
                continue
            _ = self._instances.pop(scoped, None)


    @override
    def get(self, id: str) -> object:
        try:
            return self.resolve(id)
        except Exception as e:
            if self.has(id) or isinstance(e, CircularDependencyException):
                raise
            raise EntryNotFoundException(f'Target binding [{id}] does not exist.') from e


    @override
    def get_alias(self, abstract: object) -> object:
        if abstract in self._aliases:
            return self.get_alias(self._aliases[abstract])
        return abstract


    @override
    def get_bindings(self) -> dict[object, object]:
        return cast(dict[object, object], self._bindings)


    @override
    def get_closure(self, abstract: object, concrete: object) -> Callable[..., object]:
        def factory(container: ContainerProtocol, parameters: dict[object, object] | None = None) -> object:
            if parameters is None:
                parameters = {}
            if abstract == concrete:
                return container.build(concrete)
            return container.resolve(concrete, parameters, raise_events=False)
        return factory


    @override
    def get_concrete(self, abstract: object) -> object:
        if abstract in self._bindings:
            return self._bindings[abstract]['concrete']

        if not isinstance(abstract, str):
            return abstract

        if self._checked_for_attribute_bindings.get(abstract, False):
            return abstract

        return self.get_concrete_binding_from_attributes(abstract)


    @override
    def get_concrete_binding_from_attributes(self, abstract: str) -> object:
        self._checked_for_attribute_bindings[abstract] = True
        try:
            if not inspect.isclass(abstract):
                _ = Reflection.resolve_string_to_class(abstract)
        except (ImportError, Exception):
            return abstract

        return abstract


    @override
    def get_contextual_concrete(self, abstract: object) -> object:
        binding = self.find_in_contextual_bindings(abstract)
        if binding is not None:
            return binding

        if abstract not in self._abstract_aliases:
            return None

        for alias in self._abstract_aliases[abstract]:
            binding = self.find_in_contextual_bindings(alias)
            if binding is not None:
                return binding

        return None


    @override
    def get_extenders(self, abstract: object) -> list[Callable[..., object]]:
        return self._extenders.get(self.get_alias(abstract), [])


    @staticmethod
    @override
    def get_instance() -> ContainerProtocol:
        if Container._instance is None:
            Container._instance = Container()
        return Container._instance


    @override
    def get_last_parameter_override(self) -> dict[object, object]:
        return self._with[-1] if self._with else {}


    @override
    def get_parameter_override(self, dependency: inspect.Parameter) -> object:
        return self.get_last_parameter_override()[dependency.name]


    @override
    def get_rebound_callbacks(self, abstract: object) -> list[Callable[..., object]]:
        return self._rebound_callbacks.get(abstract, [])


    @override
    def has(self, id: str) -> bool:
        return self.bound(id)


    @override
    def has_method_binding(self, method: str) -> bool:
        return method in self._method_bindings


    @override
    def has_parameter_override(self, dependency: inspect.Parameter) -> bool:
        return dependency.name in self.get_last_parameter_override()


    @override
    def instance(self, abstract: object, instance: object) -> object:
        self.remove_abstract_alias(abstract)
        is_bound = self.bound(abstract)
        _ = self._aliases.pop(abstract, None)
        self._instances[abstract] = instance
        if is_bound:
            self.rebound(abstract)
        return instance


    @override
    def is_alias(self, name: object) -> bool:
        return name in self._aliases


    @override
    def is_buildable(self, concrete: object, abstract: object) -> bool:
        return concrete == abstract or callable(concrete)


    @override
    def is_shared(self, abstract: object) -> bool:
        if abstract in self._instances:
            return True
        if abstract in self._bindings and self._bindings[abstract].get('shared', False):
            return True
        return False


    @override
    def make(self, abstract: object, parameters: dict[object, object] | None = None) -> object:
        if parameters is None:
            parameters = {}
        return self.resolve(abstract, parameters)


    @override
    def make_with(self, abstract: object, parameters: dict[object, object] | None = None) -> object:
        if parameters is None:
            parameters = {}
        return self.make(abstract, parameters)


    @override
    def not_instantiable(self, concrete: object) -> None:
        if self._build_stack:
            previous = ', '.join(str(item) for item in self._build_stack)
            message = f'Target [{concrete}] is not instantiable while building [{previous}].'
        else:
            message = f'Target [{concrete}] is not instantiable.'
        raise BindingResolutionException(message)


    @override
    def rebinding(self, abstract: object, callback: Callable[..., object]) -> object:
        abstract = self.get_alias(abstract)
        self._rebound_callbacks.setdefault(abstract, []).append(callback)
        if self.bound(abstract):
            return self.make(abstract)


    @override
    def rebound(self, abstract: object) -> None:
        callbacks = self.get_rebound_callbacks(abstract)
        if not callbacks:
            return
        instance = self.make(abstract)
        for callback in callbacks:
            _ = callback(self, instance)


    @override
    def refresh(self, abstract: object, target: object, method: str) -> object:
        def refresh_instance(_app: ContainerProtocol, instance: object) -> object:
            target_method = cast(Callable[[object], object], getattr(target, method))
            return target_method(instance)

        return self.rebinding(abstract, refresh_instance)


    @override
    def remove_abstract_alias(self, searched: object) -> None:
        if searched not in self._aliases:
            return
        abstract = self._aliases[searched]
        if abstract in self._abstract_aliases and searched in self._abstract_aliases[abstract]:
            self._abstract_aliases[abstract].remove(searched)


    @override
    def resolve(self, abstract: object, parameters: dict[object, object] | None = None, raise_events: bool = True) -> object:
        abstract = self.get_alias(abstract)

        if raise_events:
            self.fire_before_resolving_callbacks(abstract, parameters)

        concrete = self.get_contextual_concrete(abstract)
        needs_contextual_build = bool(parameters) or concrete is not None

        if abstract in self._instances and not needs_contextual_build:
            return self._instances[abstract]

        if raise_events and abstract not in self._bindings and abstract not in self._instances:
            self._try_resolve_deferred(abstract)

        self._with.append(parameters or {})

        if concrete is None:
            concrete = self.get_concrete(abstract)

        concrete = self._resolve_contextual_marker(concrete)

        if self.is_buildable(concrete, abstract):
            obj = self.build(concrete)
        else:
            obj = self.make(concrete)

        for extender in self.get_extenders(abstract):
            obj = extender(obj, self)

        if self.is_shared(abstract) and not needs_contextual_build:
            self._instances[abstract] = obj

        if raise_events:
            self.fire_resolving_callbacks(abstract, obj)
            self.fire_after_resolving_callbacks(abstract, obj)

        if not needs_contextual_build:
            self._resolved[abstract] = True

        _ = self._with.pop()

        return obj


    @override
    def resolve_builtin_default(self, parameter: inspect.Parameter) -> object:
        annotation = parameter.annotation
        building = self.currently_resolving()
        building_name = getattr(building, '__name__', str(building)) if building is not None else '<unknown>'

        if annotation is inspect.Parameter.empty or annotation not in Container._TYPE_DEFAULTS:
            value = None
        else:
            default = Container._TYPE_DEFAULTS[annotation]
            if isinstance(default, (list, dict, set, bytearray)):
                copyable = cast(
                    list[object] | dict[object, object] | set[object] | bytearray,
                    default,
                )
                value: object = copyable.copy()
            else:
                value = default

        logger.warning(
            "Resolving builtin dependency [%s] on [%s] to default value [%r]; contextual binding is required. Provide a value via container.when(%s).needs('$%s').give(<value>)",
            parameter.name,
            building_name,
            value,
            building_name,
            parameter.name,
        )

        return value


    @override
    def resolve_class(self, parameter: inspect.Parameter) -> object:
        cls_name = Reflection.get_parameter_class_name(parameter)

        if cls_name is not None and self._is_container_type(cls_name):
            return self

        if (parameter.default != inspect.Parameter.empty and
                not self.bound(cls_name) and
                self.find_in_contextual_bindings(cls_name) is None):
            return parameter.default

        try:
            if parameter.kind == inspect.Parameter.VAR_POSITIONAL:
                return self.resolve_variadic_class(parameter)
            return self.make(cls_name)
        except Exception as e:
            if isinstance(e, BindingResolutionException):
                if parameter.kind == inspect.Parameter.VAR_POSITIONAL:
                    if self._with:
                        _ = self._with.pop()
                    return []
                raise
            raise


    @override
    def resolve_dependencies(self, dependencies: list[inspect.Parameter]) -> list[object]:
        results: list[object] = []

        for dependency in dependencies:
            if self.has_parameter_override(dependency):
                results.append(self.get_parameter_override(dependency))
                continue

            result = None
            attribute = Reflection.get_contextual_attribute_from_dependency(dependency)
            if attribute is not None:
                result = self.resolve_from_attribute(attribute, dependency)

            if result is None:
                cls_name = Reflection.get_parameter_class_name(dependency)
                if cls_name is None:
                    result = self.resolve_primitive(dependency)
                else:
                    result = self.resolve_class(dependency)

            self.fire_after_resolving_attribute_callbacks([], result)

            if dependency.kind == inspect.Parameter.VAR_POSITIONAL:
                if Reflection.is_object_sequence(result):
                    results.extend(result)
                else:
                    results.append(result)
            else:
                results.append(result)

        return results


    @override
    def resolve_environment_using(self, callback: Callable[..., object] | None) -> None:
        self._environment_resolver = callback


    @override
    def resolve_from_attribute(self, attribute: object, dependency: inspect.Parameter | None = None) -> object:
        handler = self._contextual_attributes.get(
            getattr(attribute, 'name', type(attribute).__name__)
        )
        instance = attribute

        if handler is None:
            attribute_resolver = getattr(instance, 'resolve', None)
            if callable(attribute_resolver):
                handler = attribute_resolver

        if handler is None:
            raise BindingResolutionException(
                f'Contextual binding attribute [{type(attribute).__name__}] has no registered handler.'
            )

        if callable(handler):
            if dependency is not None and isinstance(instance, ContextualAttribute):
                return handler(instance, self, dependency)
            return handler(instance, self)

        raise BindingResolutionException('Attribute handler must be callable.')


    @override
    def resolve_primitive(self, parameter: inspect.Parameter) -> object:
        concrete = self.get_contextual_concrete(f'${parameter.name}')
        if concrete is not None:
            return Reflection.unwrap_if_closure(concrete, self)

        if parameter.default != inspect.Parameter.empty:
            return parameter.default

        if parameter.kind == inspect.Parameter.VAR_POSITIONAL:
            return []
        if parameter.kind == inspect.Parameter.VAR_KEYWORD:
            return {}

        return self.resolve_builtin_default(parameter)


    @override
    def resolve_variadic_class(self, parameter: inspect.Parameter) -> list[object]:
        cls_name = Reflection.get_parameter_class_name(parameter)
        abstract = self.get_alias(cls_name)
        concrete = self.get_contextual_concrete(abstract)
        if isinstance(concrete, dict):
            marker = cast(dict[str, object], concrete)
            tagged = marker.get('__tagged__')
            if isinstance(tagged, str):
                return self.tagged(tagged)
        sequence = cast(object, concrete)
        if not Reflection.is_object_sequence(sequence):
            return [self.make(cls_name)]
        return [self.resolve(item) for item in sequence]


    @override
    def resolved(self, abstract: object) -> bool:
        abstract = self.get_alias(abstract)
        return abstract in self._resolved or abstract in self._instances


    @override
    def resolving(self, abstract: object, callback: Callable[..., object] | None = None) -> None:
        if callable(abstract) and callback is None:
            self._global_resolving_callbacks.append(abstract)
        else:
            if callback is None:
                raise TypeError('A callback is required for a bound abstract.')
            abstract = self.get_alias(abstract)
            self._resolving_callbacks.setdefault(abstract, []).append(callback)


    @override
    def scoped(self, abstract: object, concrete: object | None = None) -> None:
        self._scoped_instances.append(abstract)
        self.singleton(abstract, concrete)


    @override
    def scoped_if(self, abstract: object, concrete: object | None = None) -> None:
        if not self.bound(abstract):
            self.scoped(abstract, concrete)


    @staticmethod
    @override
    def set_instance(
        container: ContainerProtocol | None = None,
    ) -> ContainerProtocol | None:
        Container._instance = container
        return container


    @override
    def singleton(self, abstract: object, concrete: object | None = None) -> None:
        self.bind(abstract, concrete, True)


    @override
    def singleton_if(self, abstract: object, concrete: object | None = None) -> None:
        if not self.bound(abstract):
            self.singleton(abstract, concrete)


    @override
    def tag(self, abstracts: object, *tags: object) -> None:
        for tag in tags:
            if not isinstance(tag, str):
                raise TypeError(f'Tag must be a string, got {tag!r}')
            if tag not in self._tags:
                self._tags[tag] = []
            for abstract in Array.array_wrap(abstracts):
                self._tags[tag].append(abstract)


    @override
    def tagged(self, tag: str) -> list[object]:
        if tag not in self._tags:
            return []
        return [self.make(abstract) for abstract in self._tags[tag]]


    @override
    def unresolvable_primitive(self, parameter: inspect.Parameter) -> None:
        message = f'Unresolvable dependency resolving [{parameter.name}]'
        raise BindingResolutionException(message)


    @override
    def when(self, concrete: object) -> ContextualBindingBuilder:
        aliases = [self.get_alias(c) for c in Array.array_wrap(concrete)]
        return ContextualBindingBuilder(self, aliases)


    @override
    def when_has_attribute(self, attribute: str, handler: Callable[..., object]) -> None:
        self._contextual_attributes[attribute] = handler


    @override
    def wrap(self, callback: Callable[..., object], parameters: dict[object, object] | None = None) -> Callable[..., object]:
        if parameters is None:
            parameters = {}
        return lambda: self.call(callback, parameters)
