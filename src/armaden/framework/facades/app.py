from typing import TYPE_CHECKING, Any, Callable, Dict, Optional, overload
from ._registry import get_application

if TYPE_CHECKING:
    from returns.result import Result
    from armaden.framework.protocols.kernel import CoreApplicationInterface
    from armaden.framework.protocols.supervisor import SupervisorInterface
    from armaden.framework.classes.instance_container import ContextualBindingBuilder


def app() -> 'CoreApplicationInterface':
    return get_application()


class App:
    @classmethod
    def application(cls) -> 'CoreApplicationInterface':
        return get_application()

    @classmethod
    def container(cls) -> Any:
        return get_application().container

    @classmethod
    def supervisor(cls) -> 'SupervisorInterface':
        return get_application().supervisor

    @classmethod
    def process(cls):
        return get_application().supervisor.process()

    @classmethod
    def schedule(cls):
        return get_application().supervisor.schedule()

    @classmethod
    def concurrency(cls):
        return get_application().supervisor.concurrency()

    @classmethod
    def config(cls, key: str, default: Any | None = None) -> Any:
        return get_application().config(key, default)

    @classmethod
    def version(cls) -> str:
        return get_application().version()

    @classmethod
    def register(cls, provider: Any) -> 'Result[None]':
        return get_application().register(provider)

    @classmethod
    def boot(cls) -> 'Result[None]':
        return get_application().boot()

    @classmethod
    async def status(cls) -> 'Result[Any]':
        return await get_application().status()

    @classmethod
    def bind(cls, abstract: Any, concrete: Any = None, shared: bool = False) -> None:
        cls.container().bind(abstract, concrete, shared)

    @classmethod
    def bind_if(cls, abstract: Any, concrete: Any = None, shared: bool = False) -> None:
        cls.container().bind_if(abstract, concrete, shared)

    @classmethod
    def singleton(cls, abstract: Any, concrete: Any = None) -> None:
        cls.container().singleton(abstract, concrete)

    @classmethod
    def singleton_if(cls, abstract: Any, concrete: Any = None) -> None:
        cls.container().singleton_if(abstract, concrete)

    @classmethod
    def scoped(cls, abstract: Any, concrete: Any = None) -> None:
        cls.container().scoped(abstract, concrete)

    @classmethod
    def scoped_if(cls, abstract: Any, concrete: Any = None) -> None:
        cls.container().scoped_if(abstract, concrete)

    @classmethod
    def instance[T](cls, abstract: Any, instance: T) -> T:
        return cls.container().instance(abstract, instance)

    @classmethod
    def extend(cls, abstract: Any, closure: Callable) -> None:
        cls.container().extend(abstract, closure)

    @classmethod
    def alias(cls, abstract: Any, alias: Any) -> None:
        cls.container().alias(abstract, alias)

    @classmethod
    def when(cls, concrete: Any) -> 'ContextualBindingBuilder':
        return cls.container().when(concrete)

    @classmethod
    def tag(cls, abstracts: Any, *tags: Any) -> None:
        cls.container().tag(abstracts, *tags)

    @classmethod
    def tagged(cls, tag: str) -> list:
        return cls.container().tagged(tag)

    @overload
    @classmethod
    def make[T](cls, abstract: type[T], parameters: Optional[Dict[str, Any]] = None) -> T: ...
    @overload
    @classmethod
    def make(cls, abstract: Any, parameters: Optional[Dict[str, Any]] = None) -> Any: ...
    @classmethod
    def make(cls, abstract: Any, parameters: Optional[Dict[str, Any]] = None) -> Any:
        return cls.container().make(abstract, parameters)

    @overload
    @classmethod
    def make_with[T](cls, abstract: type[T], parameters: Optional[Dict[str, Any]] = None) -> T: ...

    @overload
    @classmethod
    def make_with(cls, abstract: Any, parameters: Optional[Dict[str, Any]] = None) -> Any: ...

    @classmethod
    def make_with(cls, abstract: Any, parameters: Optional[Dict[str, Any]] = None) -> Any:
        return cls.container().make_with(abstract, parameters)

    @classmethod
    def call(cls, callback: Any, parameters: Optional[Dict[str, Any]] = None, default_method: Optional[str] = None) -> Any:
        return cls.container().call(callback, parameters, default_method)

    @classmethod
    def factory(cls, abstract: Any) -> Callable:
        return cls.container().factory(abstract)

    @classmethod
    def wrap(cls, callback: Callable, parameters: Optional[Dict[str, Any]] = None) -> Callable:
        return cls.container().wrap(callback, parameters)

    @classmethod
    def get(cls, id: str) -> Any:
        return cls.container().get(id)

    @classmethod
    def bound(cls, abstract: Any) -> bool:
        return cls.container().bound(abstract)

    @classmethod
    def has(cls, id: str) -> bool:
        return cls.container().has(id)

    @classmethod
    def resolved(cls, abstract: Any) -> bool:
        return cls.container().resolved(abstract)

    @classmethod
    def is_shared(cls, abstract: Any) -> bool:
        return cls.container().is_shared(abstract)

    @classmethod
    def is_alias(cls, name: Any) -> bool:
        return cls.container().is_alias(name)

    @classmethod
    def rebinding(cls, abstract: Any, callback: Callable) -> Any:
        return cls.container().rebinding(abstract, callback)

    @classmethod
    def flush(cls) -> None:
        cls.container().flush()

    @classmethod
    def forget_instance(cls, abstract: Any) -> None:
        cls.container().forget_instance(abstract)

    @classmethod
    def forget_instances(cls) -> None:
        cls.container().forget_instances()

    @classmethod
    def forget_scoped_instances(cls) -> None:
        cls.container().forget_scoped_instances()
