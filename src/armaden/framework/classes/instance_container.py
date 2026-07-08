from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, List, Optional
import inspect
import logging

from .bound_method import BoundMethod
from ..utils.container import (
    array_wrap,
    get_class_for_callable,
    get_contextual_attribute_from_dependency,
    get_parameter_class_name,
    resolve_string_to_class,
    unwrap_if_closure,
)

logger = logging.getLogger(__name__)

_BUILTIN_DEFAULTS: Dict[type, Any] = {
    int: 0,
    float: 0.0,
    complex: 0j,
    str: '',
    bool: False,
    bytes: b'',
    bytearray: bytearray(),
    list: [],
    dict: {},
    tuple: (),
    set: set(),
    frozenset: frozenset(),
}

# -- Internal Types ------------------------------------------------------------

class SelfBuilding(ABC):
    pass


class ContextualAttribute(ABC):
    @staticmethod
    @abstractmethod
    def resolve(attribute: Any, container: 'InstanceContainer', parameter: inspect.Parameter) -> Any:
        raise NotImplementedError


class BindingResolutionException(Exception):
    pass


class CircularDependencyException(Exception):
    pass


class EntryNotFoundException(Exception):
    pass


class LogicException(Exception):
    pass


# -- ContextualBindingBuilder --------------------------------------------------

class ContextualBindingBuilder:
    def __init__(self, container: InstanceContainer, concrete: list):
        self.container = container
        self.concrete = array_wrap(concrete)
        self.abstract: Any = None

    def needs(self, abstract: Any) -> ContextualBindingBuilder:
        self.abstract = abstract
        return self

    def give(self, implementation: Any) -> ContextualBindingBuilder:
        for concrete in self.concrete:
            self.container.add_contextual_binding(concrete, self.abstract, implementation)
        return self

    def giveTagged(self, tag: str) -> ContextualBindingBuilder:
        for concrete in self.concrete:
            self.container.add_contextual_binding(
                concrete, self.abstract, {'__tagged__': tag}
            )
        return self

    def giveConfig(self, key: str) -> ContextualBindingBuilder:
        for concrete in self.concrete:
            self.container.add_contextual_binding(
                concrete, self.abstract, {'__config__': key}
            )
        return self


# -- InstanceContainer ---------------------------------------------------------

class InstanceContainer:
    _instance: Optional[InstanceContainer] = None

    def __init__(self):
        self._bindings: Dict[Any, Any] = {}
        self._instances: Dict[Any, Any] = {}
        self._aliases: Dict[Any, Any] = {}
        self._abstract_aliases: Dict[Any, List[Any]] = {}
        self._resolved: Dict[Any, bool] = {}
        self._build_stack: List[Any] = []
        self._with: List[Dict[str, Any]] = []
        self._method_bindings: Dict[str, Any] = {}
        self._tags: Dict[str, List[Any]] = {}
        self._scoped_instances: List[Any] = []
        self._extenders: Dict[Any, List[Callable]] = {}
        self._rebound_callbacks: Dict[Any, List[Callable]] = {}
        self._contextual: Dict[Any, Dict[Any, Any]] = {}
        self._contextual_attributes: Dict[Any, Callable] = {}
        self._global_before_resolving_callbacks: List[Callable] = []
        self._global_resolving_callbacks: List[Callable] = []
        self._global_after_resolving_callbacks: List[Callable] = []
        self._before_resolving_callbacks: Dict[Any, List[Callable]] = {}
        self._resolving_callbacks: Dict[Any, List[Callable]] = {}
        self._after_resolving_callbacks: Dict[Any, List[Callable]] = {}
        self._after_resolving_attribute_callbacks: Dict[Any, List[Callable]] = {}
        self._checked_for_attribute_bindings: Dict[Any, bool] = {}
        self._checked_for_singleton_or_scoped_attributes: Dict[Any, Any] = {}
        self._environment_resolver: Optional[Callable] = None
        self._deferred_services: Dict[Any, type] = {}

    # -- Contextual -----------------------------------------------------------

    def when(self, concrete: Any) -> ContextualBindingBuilder:
        aliases = [self.get_alias(c) for c in array_wrap(concrete)]
        return ContextualBindingBuilder(self, aliases)

    def when_has_attribute(self, attribute: str, handler: Callable) -> None:
        self._contextual_attributes[attribute] = handler

    # -- Binding state --------------------------------------------------------

    def bound(self, abstract: Any) -> bool:
        return abstract in self._bindings or abstract in self._instances or self.is_alias(abstract)

    def has(self, id: str) -> bool:
        return self.bound(id)

    def resolved(self, abstract: Any) -> bool:
        abstract = self.get_alias(abstract)
        return abstract in self._resolved or abstract in self._instances

    def is_shared(self, abstract: Any) -> bool:
        if abstract in self._instances:
            return True
        if abstract in self._bindings and self._bindings[abstract].get('shared', False):
            return True
        return False

    def is_alias(self, name: Any) -> bool:
        return name in self._aliases

    # -- Registration ---------------------------------------------------------

    def bind(self, abstract: Any, concrete: Any = None, shared: bool = False) -> None:
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

    def bind_if(self, abstract: Any, concrete: Any = None, shared: bool = False) -> None:
        if not self.bound(abstract):
            self.bind(abstract, concrete, shared)

    def singleton(self, abstract: Any, concrete: Any = None) -> None:
        self.bind(abstract, concrete, True)

    def singleton_if(self, abstract: Any, concrete: Any = None) -> None:
        if not self.bound(abstract):
            self.singleton(abstract, concrete)

    def scoped(self, abstract: Any, concrete: Any = None) -> None:
        self._scoped_instances.append(abstract)
        self.singleton(abstract, concrete)

    def scoped_if(self, abstract: Any, concrete: Any = None) -> None:
        if not self.bound(abstract):
            self.scoped(abstract, concrete)

    def bind_based_on_closure_return_types(self, abstract: Callable, concrete: Any = None, shared: bool = False) -> None:
        abstracts = self.closure_return_types(abstract)
        concrete_fn = abstract
        for _name, typ in abstracts.items():
            self.bind(typ, concrete_fn, shared)

    def get_closure(self, abstract: Any, concrete: Any) -> Callable:
        def factory(container: InstanceContainer, parameters: Optional[Dict[str, Any]] = None) -> Any:
            if parameters is None:
                parameters = {}
            if abstract == concrete:
                return container.build(concrete)
            return container.resolve(concrete, parameters, raiseEvents=False)
        return factory

    def extend(self, abstract: Any, closure: Callable) -> None:
        abstract = self.get_alias(abstract)
        if abstract in self._instances:
            self._instances[abstract] = closure(self._instances[abstract], self)
            self.rebound(abstract)
        else:
            self._extenders.setdefault(abstract, []).append(closure)
            if self.resolved(abstract):
                self.rebound(abstract)

    def instance(self, abstract: Any, instance: Any) -> Any:
        self.remove_abstract_alias(abstract)
        is_bound = self.bound(abstract)
        self._aliases.pop(abstract, None)
        self._instances[abstract] = instance
        if is_bound:
            self.rebound(abstract)
        return instance

    def alias(self, abstract: Any, alias: Any) -> None:
        if alias == abstract:
            raise LogicException(f'[{abstract}] is aliased to itself.')

        self.remove_abstract_alias(alias)
        self._aliases[alias] = abstract
        self._abstract_aliases.setdefault(abstract, []).append(alias)

    def remove_abstract_alias(self, searched: Any) -> None:
        if searched not in self._aliases:
            return
        abstract = self._aliases[searched]
        if abstract in self._abstract_aliases and searched in self._abstract_aliases[abstract]:
            self._abstract_aliases[abstract].remove(searched)

    # -- Tagging --------------------------------------------------------------

    def tag(self, abstracts: Any, *tags: Any) -> None:
        for tag in tags:
            if tag not in self._tags:
                self._tags[tag] = []
            for abstract in array_wrap(abstracts):
                self._tags[tag].append(abstract)

    def tagged(self, tag: str) -> list:
        if tag not in self._tags:
            return []
        return [self.make(abstract) for abstract in self._tags[tag]]

    # -- Rebinding ------------------------------------------------------------

    def rebinding(self, abstract: Any, callback: Callable) -> Any:
        abstract = self.get_alias(abstract)
        self._rebound_callbacks.setdefault(abstract, []).append(callback)
        if self.bound(abstract):
            return self.make(abstract)

    def refresh(self, abstract: Any, target: Any, method: str) -> Any:
        return self.rebinding(abstract, lambda app, instance: getattr(target, method)(instance))

    def rebound(self, abstract: Any) -> None:
        callbacks = self.get_rebound_callbacks(abstract)
        if not callbacks:
            return
        instance = self.make(abstract)
        for callback in callbacks:
            callback(self, instance)

    def get_rebound_callbacks(self, abstract: Any) -> List[Callable]:
        return self._rebound_callbacks.get(abstract, [])

    # -- Calling / Factories --------------------------------------------------

    def wrap(self, callback: Callable, parameters: Optional[Dict[str, Any]] = None) -> Callable:
        if parameters is None:
            parameters = {}
        return lambda: self.call(callback, parameters)

    def call(self, callback: Any, parameters: Optional[Dict[str, Any]] = None, default_method: Optional[str] = None) -> Any:
        if parameters is None:
            parameters = {}

        pushed_to_build_stack = False
        class_name = get_class_for_callable(callback)

        if class_name and class_name not in self._build_stack:
            self._build_stack.append(class_name)
            pushed_to_build_stack = True

        result = BoundMethod.call(self, callback, parameters, default_method)

        if pushed_to_build_stack:
            self._build_stack.pop()

        return result

    def factory(self, abstract: Any) -> Callable:
        return lambda: self.make(abstract)

    def make_with(self, abstract: Any, parameters: Optional[Dict[str, Any]] = None) -> Any:
        if parameters is None:
            parameters = {}
        return self.make(abstract, parameters)

    def make(self, abstract: Any, parameters: Optional[Dict[str, Any]] = None) -> Any:
        if parameters is None:
            parameters = {}
        return self.resolve(abstract, parameters)

    def get(self, id: str) -> Any:
        try:
            return self.resolve(id)
        except Exception as e:
            if self.has(id) or isinstance(e, CircularDependencyException):
                raise
            raise EntryNotFoundException(f'Target binding [{id}] does not exist.') from e

    # -- Core Resolution ------------------------------------------------------

    def resolve(self, abstract: Any, parameters: Optional[Dict[str, Any]] = None, raiseEvents: bool = True) -> Any:
        abstract = self.get_alias(abstract)

        if raiseEvents:
            self.fire_before_resolving_callbacks(abstract, parameters)

        concrete = self.get_contextual_concrete(abstract)
        needs_contextual_build = bool(parameters) or concrete is not None

        if abstract in self._instances and not needs_contextual_build:
            return self._instances[abstract]

        if raiseEvents and abstract not in self._bindings and abstract not in self._instances:
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

        if raiseEvents:
            self.fire_resolving_callbacks(abstract, obj)
            self.fire_after_resolving_callbacks(abstract, obj)

        if not needs_contextual_build:
            self._resolved[abstract] = True

        self._with.pop()

        return obj

    # -- Concrete / contextual ------------------------------------------------

    def get_concrete(self, abstract: Any) -> Any:
        if abstract in self._bindings:
            return self._bindings[abstract]['concrete']

        if not isinstance(abstract, str):
            return abstract

        if self._checked_for_attribute_bindings.get(abstract, False):
            return abstract

        return self.get_concrete_binding_from_attributes(abstract)

    def get_concrete_binding_from_attributes(self, abstract: str) -> Any:
        self._checked_for_attribute_bindings[abstract] = True
        try:
            if inspect.isclass(abstract):
                reflected = abstract
            else:
                reflected = resolve_string_to_class(abstract)
        except (ImportError, Exception):
            return abstract

        return abstract

    def get_contextual_concrete(self, abstract: Any) -> Any:
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

    def find_in_contextual_bindings(self, abstract: Any) -> Any:
        if not self._build_stack:
            return None
        return self._contextual.get(self._build_stack[-1], {}).get(abstract)

    def add_contextual_binding(self, concrete: Any, abstract: Any, implementation: Any) -> None:
        self._contextual.setdefault(concrete, {})[self.get_alias(abstract)] = implementation

    def _resolve_contextual_marker(self, concrete: Any) -> Any:
        if not isinstance(concrete, dict):
            return concrete
        if '__tagged__' in concrete:
            return self.tagged(concrete['__tagged__'])
        if '__config__' in concrete:
            return self._resolve_config_value(concrete['__config__'])
        return concrete

    def _resolve_config_value(self, key: str) -> Any:
        if self.resolved('config'):
            return self.make('config').get(key)
        return self.make('app').config(key)

    def is_buildable(self, concrete: Any, abstract: Any) -> bool:
        return concrete == abstract or callable(concrete)

    # -- Building --------------------------------------------------------------

    def build(self, concrete: Any) -> Any:
        if self._is_container_type(concrete):
            return self

        if callable(concrete) and not inspect.isclass(concrete):
            self._build_stack.append(id(concrete))
            try:
                return concrete(self, self.get_last_parameter_override())
            finally:
                self._build_stack.pop()

        if not inspect.isclass(concrete):
            raise BindingResolutionException(f'Target class [{concrete}] does not exist.')

        if not callable(concrete):
            raise BindingResolutionException(f'Target class [{concrete}] cannot be instantiated.')

        if issubclass(concrete, SelfBuilding) and concrete not in self._build_stack:
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
            self._build_stack.pop()

    def build_self_building_instance(self, concrete: type) -> Any:
        if not hasattr(concrete, 'new_instance') or not callable(getattr(concrete, 'new_instance')):
            raise BindingResolutionException(f'No newInstance method exists for [{concrete}].')

        self._build_stack.append(concrete)
        try:
            instance = self.call((concrete, 'new_instance'))
            self.fire_after_resolving_attribute_callbacks([], instance)
            return instance
        finally:
            self._build_stack.pop()

    # -- Dependency resolution ------------------------------------------------

    def resolve_dependencies(self, dependencies: List[inspect.Parameter]) -> list:
        results: list = []

        for dependency in dependencies:
            if self.has_parameter_override(dependency):
                results.append(self.get_parameter_override(dependency))
                continue

            result = None
            attribute = get_contextual_attribute_from_dependency(dependency)
            if attribute is not None:
                result = self.resolve_from_attribute(attribute, dependency)

            if result is None:
                cls_name = get_parameter_class_name(dependency)
                if cls_name is None:
                    result = self.resolve_primitive(dependency)
                else:
                    result = self.resolve_class(dependency)

            self.fire_after_resolving_attribute_callbacks([], result)

            if dependency.kind == inspect.Parameter.VAR_POSITIONAL:
                if isinstance(result, (list, tuple)):
                    results.extend(result)
                else:
                    results.append(result)
            else:
                results.append(result)

        return results

    def has_parameter_override(self, dependency: inspect.Parameter) -> bool:
        return dependency.name in self.get_last_parameter_override()

    def get_parameter_override(self, dependency: inspect.Parameter) -> Any:
        return self.get_last_parameter_override()[dependency.name]

    def get_last_parameter_override(self) -> Dict[str, Any]:
        return self._with[-1] if self._with else {}

    def resolve_primitive(self, parameter: inspect.Parameter) -> Any:
        concrete = self.get_contextual_concrete(f'${parameter.name}')
        if concrete is not None:
            return unwrap_if_closure(concrete, self)

        if parameter.default != inspect.Parameter.empty:
            return parameter.default

        if parameter.kind == inspect.Parameter.VAR_POSITIONAL:
            return []
        if parameter.kind == inspect.Parameter.VAR_KEYWORD:
            return {}

        return self.resolve_builtin_default(parameter)

    def resolve_builtin_default(self, parameter: inspect.Parameter) -> Any:
        annotation = parameter.annotation
        building = self.currently_resolving()
        building_name = getattr(building, '__name__', str(building)) if building is not None else '<unknown>'

        if annotation is inspect.Parameter.empty or annotation not in _BUILTIN_DEFAULTS:
            value = None
        else:
            default = _BUILTIN_DEFAULTS[annotation]
            value = type(default)() if isinstance(default, (list, dict, set, bytearray)) else default

        logger.warning(
            "Resolving builtin dependency [%s] on [%s] to default value [%r]; "
            "contextual binding is required. Provide a value via "
            "container.when(%s).needs('$%s').give(<value>)",
            parameter.name,
            building_name,
            value,
            building_name,
            parameter.name,
        )

        return value

    def _is_container_type(self, cls_name: type) -> bool:
        if cls_name is None or not isinstance(cls_name, type):
            return False
        return cls_name is InstanceContainer or issubclass(cls_name, InstanceContainer)

    def resolve_class(self, parameter: inspect.Parameter) -> Any:
        cls_name = get_parameter_class_name(parameter)

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
                        self._with.pop()
                    return []
                raise
            raise

    def resolve_variadic_class(self, parameter: inspect.Parameter) -> list:
        cls_name = get_parameter_class_name(parameter)
        abstract = self.get_alias(cls_name)
        concrete = self.get_contextual_concrete(abstract)
        if isinstance(concrete, dict) and '__tagged__' in concrete:
            return self.tagged(concrete['__tagged__'])
        if not isinstance(concrete, (list, tuple)):
            return [self.make(cls_name)]
        return [self.resolve(item) for item in concrete]

    def resolve_from_attribute(self, attribute: Any, dependency: Optional[inspect.Parameter] = None) -> Any:
        handler = self._contextual_attributes.get(
            getattr(attribute, 'name', type(attribute).__name__)
        )
        instance = attribute

        if handler is None and hasattr(instance, 'resolve'):
            handler = instance.resolve

        if handler is None:
            raise BindingResolutionException(
                f'Contextual binding attribute [{type(attribute).__name__}] has no registered handler.'
            )

        if callable(handler):
            if dependency is not None and isinstance(instance, ContextualAttribute):
                return handler(instance, self, dependency)
            return handler(instance, self)

        raise BindingResolutionException('Attribute handler must be callable.')

    # -- Error helpers --------------------------------------------------------

    def not_instantiable(self, concrete: Any) -> None:
        if self._build_stack:
            previous = ', '.join(str(item) for item in self._build_stack)
            message = f'Target [{concrete}] is not instantiable while building [{previous}].'
        else:
            message = f'Target [{concrete}] is not instantiable.'
        raise BindingResolutionException(message)

    def unresolvable_primitive(self, parameter: inspect.Parameter) -> None:
        message = f'Unresolvable dependency resolving [{parameter.name}]'
        raise BindingResolutionException(message)

    # -- Method bindings ------------------------------------------------------

    def has_method_binding(self, method: str) -> bool:
        return method in self._method_bindings

    def bind_method(self, method: Any, callback: Callable) -> None:
        self._method_bindings[self._parse_bind_method(method)] = callback

    def _parse_bind_method(self, method: Any) -> str:
        if isinstance(method, (list, tuple)):
            return f'{method[0]}@{method[1]}'
        return str(method)

    def call_method_binding(self, method: str, instance: Any) -> Any:
        return self._method_bindings[method](instance, self)

    # -- Callbacks / events ---------------------------------------------------

    def before_resolving(self, abstract: Any, callback: Optional[Callable] = None) -> None:
        if callable(abstract) and callback is None:
            self._global_before_resolving_callbacks.append(abstract)
        else:
            abstract = self.get_alias(abstract)
            self._before_resolving_callbacks.setdefault(abstract, []).append(callback)

    def resolving(self, abstract: Any, callback: Optional[Callable] = None) -> None:
        if callable(abstract) and callback is None:
            self._global_resolving_callbacks.append(abstract)
        else:
            abstract = self.get_alias(abstract)
            self._resolving_callbacks.setdefault(abstract, []).append(callback)

    def after_resolving(self, abstract: Any, callback: Optional[Callable] = None) -> None:
        if callable(abstract) and callback is None:
            self._global_after_resolving_callbacks.append(abstract)
        else:
            abstract = self.get_alias(abstract)
            self._after_resolving_callbacks.setdefault(abstract, []).append(callback)

    def after_resolving_attribute(self, attribute: Any, callback: Callable) -> None:
        self._after_resolving_attribute_callbacks.setdefault(attribute, []).append(callback)

    def fire_before_resolving_callbacks(self, abstract: Any, parameters: Optional[Dict[str, Any]] = None) -> None:
        if parameters is None:
            parameters = {}
        self._fire_before_callback_array(abstract, parameters, self._global_before_resolving_callbacks)
        for typ, callbacks in self._before_resolving_callbacks.items():
            if typ == abstract:
                self._fire_before_callback_array(abstract, parameters, callbacks)
            elif isinstance(abstract, type) and isinstance(typ, type) and issubclass(abstract, typ):
                self._fire_before_callback_array(abstract, parameters, callbacks)

    def fire_resolving_callbacks(self, abstract: Any, obj: Any) -> None:
        self._fire_callback_array(obj, self._global_resolving_callbacks)
        self._fire_callback_array(obj, self._get_callbacks_for_type(abstract, obj, self._resolving_callbacks))
        self.fire_after_resolving_callbacks(abstract, obj)

    def fire_after_resolving_callbacks(self, abstract: Any, obj: Any) -> None:
        self._fire_callback_array(obj, self._global_after_resolving_callbacks)
        self._fire_callback_array(obj, self._get_callbacks_for_type(abstract, obj, self._after_resolving_callbacks))

    def fire_after_resolving_attribute_callbacks(self, attributes: list, obj: Any) -> None:
        for attribute in attributes:
            attr_name = attribute if isinstance(attribute, str) else getattr(attribute, '__name__', str(type(attribute)))
            for callbacks in self._after_resolving_attribute_callbacks.get(attr_name, []):
                callbacks(attribute, obj, self)

    def _get_callbacks_for_type(self, abstract: Any, obj: Any, callbacks_per_type: Dict[Any, List[Callable]]) -> List[Callable]:
        results: List[Callable] = []
        for typ, callbacks in callbacks_per_type.items():
            if typ == abstract or isinstance(obj, typ):
                results.extend(callbacks)
        return results

    def _fire_callback_array(self, obj: Any, callbacks: List[Callable]) -> None:
        for callback in callbacks:
            callback(obj, self)

    def _fire_before_callback_array(self, abstract: Any, parameters: Dict[str, Any], callbacks: List[Callable]) -> None:
        for callback in callbacks:
            callback(abstract, parameters, self)

    # -- Reflection helpers ---------------------------------------------------

    def closure_return_types(self, closure: Callable) -> Dict[str, type]:
        import typing
        try:
            hints = typing.get_type_hints(closure)
        except Exception:
            return {}
        return_type = hints.get('return')
        if return_type is None:
            return {}

        result: Dict[str, type] = {}
        origin = typing.get_origin(return_type)
        args = typing.get_args(return_type)

        if origin is typing.Union or getattr(origin, '__origin__', None) is typing.Union:
            for arg in args:
                if arg is type(None):
                    continue
                if isinstance(arg, type):
                    result[arg.__name__] = arg
        elif isinstance(return_type, type):
            result[return_type.__name__] = return_type

        return result

    # -- Misc -----------------------------------------------------------------

    def currently_resolving(self) -> Any:
        return self._build_stack[-1] if self._build_stack else None

    def get_bindings(self) -> Dict[Any, Any]:
        return self._bindings

    def get_alias(self, abstract: Any) -> Any:
        if abstract in self._aliases:
            return self.get_alias(self._aliases[abstract])
        return abstract

    def get_extenders(self, abstract: Any) -> List[Callable]:
        return self._extenders.get(self.get_alias(abstract), [])

    def forget_extenders(self, abstract: Any) -> None:
        alias = self.get_alias(abstract)
        self._extenders.pop(alias, None)

    def drop_stale_instances(self, abstract: Any) -> None:
        alias = self.get_alias(abstract)
        self._instances.pop(alias, None)
        self._aliases.pop(alias, None)

    def forget_instance(self, abstract: Any) -> None:
        self._instances.pop(abstract, None)

    def forget_instances(self) -> None:
        self._instances.clear()

    def forget_scoped_instances(self) -> None:
        for scoped in self._scoped_instances:
            if callable(scoped):
                continue
            self._instances.pop(scoped, None)

    def flush(self) -> None:
        self._aliases.clear()
        self._resolved.clear()
        self._bindings.clear()
        self._instances.clear()
        self._abstract_aliases.clear()
        self._scoped_instances.clear()
        self._checked_for_attribute_bindings.clear()
        self._checked_for_singleton_or_scoped_attributes.clear()
        self._rebound_callbacks.clear()
        self._extenders.clear()
        self._tags.clear()
        self._method_bindings.clear()
        self._global_before_resolving_callbacks.clear()
        self._global_resolving_callbacks.clear()
        self._global_after_resolving_callbacks.clear()
        self._before_resolving_callbacks.clear()
        self._resolving_callbacks.clear()
        self._after_resolving_callbacks.clear()
        self._after_resolving_attribute_callbacks.clear()
        self._contextual.clear()
        self._contextual_attributes.clear()
        self._with.clear()
        self._build_stack.clear()

    # -- Environment ----------------------------------------------------------

    def resolve_environment_using(self, callback: Optional[Callable]) -> None:
        self._environment_resolver = callback

    def current_environment_is(self, environments: Any) -> bool:
        if self._environment_resolver is None:
            return False
        return self._environment_resolver(environments)

    # -- Deferred Providers --------------------------------------------------

    def add_deferred_services(self, services: Dict[Any, type]) -> None:
        self._deferred_services.update(services)

    def _try_resolve_deferred(self, abstract: Any) -> None:
        if abstract not in self._deferred_services:
            return
        provider_class = self._deferred_services.pop(abstract)
        provider = provider_class(self)
        provider.register_bindings()
        provider.register()
        if hasattr(provider, 'boot'):
            provider.boot()

    # -- Singleton accessors --------------------------------------------------

    @staticmethod
    def get_instance() -> InstanceContainer:
        if InstanceContainer._instance is None:
            InstanceContainer._instance = InstanceContainer()
        return InstanceContainer._instance

    @staticmethod
    def set_instance(container: Optional[InstanceContainer] = None) -> Optional[InstanceContainer]:
        InstanceContainer._instance = container
        return container

    # -- Attribute-based binding discovery -----------------------------------

    def discover_attribute_bindings(self, classes: list[type]) -> None:
        for cls in classes:
            self._discover_bind_attributes(cls)
            self._discover_singleton_attribute(cls)
            self._discover_scoped_attribute(cls)

    def _discover_bind_attributes(self, cls: type) -> None:
        bindings = getattr(cls, '_armaden_bindings', [])
        for bind in bindings:
            if bind.environments:
                if not self._environment_matches(bind.environments):
                    continue
            self.bind(cls, bind.concrete, shared=False)

    def _discover_singleton_attribute(self, cls: type) -> None:
        if getattr(cls, '_armaden_singleton', False):
            self.singleton(cls, cls)

    def _discover_scoped_attribute(self, cls: type) -> None:
        if getattr(cls, '_armaden_scoped', False):
            self.scoped(cls, cls)

    def _environment_matches(self, environments: list[str]) -> bool:
        if self._environment_resolver is None:
            return False
        return self._environment_resolver() in environments

    # -- ArrayAccess / magic --------------------------------------------------

    def __contains__(self, key: Any) -> bool:
        return self.bound(key)

    def __getitem__(self, key: Any) -> Any:
        return self.make(key)

    def __setitem__(self, key: Any, value: Any) -> None:
        self.bind(key, value if callable(value) else lambda: value)

    def __delitem__(self, key: Any) -> None:
        self._bindings.pop(key, None)
        self._instances.pop(key, None)
        self._resolved.pop(key, None)

    def __getattr__(self, key: str) -> Any:
        return self.make(key)

    def __setattr__(self, key: str, value: Any) -> None:
        if key.startswith('_'):
            object.__setattr__(self, key, value)
        else:
            self.bind(key, value if callable(value) else lambda: value)
