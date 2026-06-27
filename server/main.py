#!/usr/bin/env python3
"""Example demonstrating the IoC container (InstanceContainer) ported from Laravel."""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

# ---------------------------------------------------------------------------
# The framework package pulls in heavy dependencies on init, so we load the
# container module directly to keep this example self-contained.
# ---------------------------------------------------------------------------
import importlib.util
import types

# Stub out the framework package hierarchy so relative imports inside the
# container succeed without triggering the full framework __init__ chain.
framework_pkg = types.ModuleType("framework")
framework_pkg.__path__ = [str(PROJECT_ROOT / "framework")]  # type: ignore[attr-defined]
sys.modules["framework"] = framework_pkg

framework_classes = types.ModuleType("framework.classes")
framework_classes.__path__ = [str(PROJECT_ROOT / "framework" / "classes")]  # type: ignore[attr-defined]
sys.modules["framework.classes"] = framework_classes

framework_utils = types.ModuleType("framework.utils")
framework_utils.__path__ = [str(PROJECT_ROOT / "framework" / "utils")]  # type: ignore[attr-defined]
sys.modules["framework.utils"] = framework_utils

# Load utils.container
_util_spec = importlib.util.spec_from_file_location(
    "framework.utils.container",
    PROJECT_ROOT / "framework" / "utils" / "container.py",
)
_util_mod = importlib.util.module_from_spec(_util_spec)
sys.modules[_util_spec.name] = _util_mod
_util_spec.loader.exec_module(_util_mod)  # type: ignore[union-attr]
setattr(framework_utils, "container", _util_mod)

# Load classes.bound_method
_bound_spec = importlib.util.spec_from_file_location(
    "framework.classes.bound_method",
    PROJECT_ROOT / "framework" / "classes" / "bound_method.py",
)
_bound_mod = importlib.util.module_from_spec(_bound_spec)
sys.modules[_bound_spec.name] = _bound_mod
_bound_spec.loader.exec_module(_bound_mod)  # type: ignore[union-attr]
setattr(framework_classes, "bound_method", _bound_mod)

# Load classes.instance_container
_container_spec = importlib.util.spec_from_file_location(
    "framework.classes.instance_container",
    PROJECT_ROOT / "framework" / "classes" / "instance_container.py",
)
_container_mod = importlib.util.module_from_spec(_container_spec)
sys.modules[_container_spec.name] = _container_mod
_container_spec.loader.exec_module(_container_mod)  # type: ignore[union-attr]
setattr(framework_classes, "instance_container", _container_mod)

InstanceContainer = _container_mod.InstanceContainer


# -- Example domain classes ----------------------------------------------------

class DatabaseConnection:
    """A simple DB connection with one primitive parameter."""
    def __init__(self, driver: str = "sqlite"):
        self.driver = driver

    def query(self):
        return f"Querying via {self.driver}"


class Logger:
    """A simple logger with one primitive parameter."""
    def __init__(self, prefix: str = "APP"):
        self.prefix = prefix

    def log(self, message: str):
        print(f"[{self.prefix}] {message}")


class Mailer:
    """Depends on Logger – will be auto-injected."""
    def __init__(self, logger: Logger):
        self.logger = logger

    def send(self, to: str, subject: str):
        self.logger.log(f"Sending mail to {to}: {subject}")
        return f"Sent '{subject}' to {to}"


class Repository:
    """Depends on DatabaseConnection – will be auto-injected."""
    def __init__(self, db: DatabaseConnection):
        self.db = db

    def all(self):
        return self.db.query()


class RedisBackend:
    def get(self, key: str):
        return f"redis:{key}"


class MemcachedBackend:
    def get(self, key: str):
        return f"memcached:{key}"


class Cache:
    """Constructor takes a primitive 'backend' – resolved via contextual binding."""
    def __init__(self, backend):
        self.backend = backend


# -- main ---------------------------------------------------------------------

if __name__ == "__main__":
    container = InstanceContainer()

    # Ensure the container can inject itself for SelfBuilding or other type-hints
    container.instance(InstanceContainer, container)

    print("=" * 60)
    print("1. Simple value binding")
    print("=" * 60)
    container.bind("app.name", lambda c, params=None: "MyApplication")
    print("app.name =>", container.make("app.name"))

    print("\n" + "=" * 60)
    print("2. Class binding (transient)")
    print("=" * 60)
    # Bind a factory that returns a new DatabaseConnection each time
    container.bind(DatabaseConnection, lambda c, params=None: DatabaseConnection("postgres"))
    db1 = container.make(DatabaseConnection)
    db2 = container.make(DatabaseConnection)
    print("db1.driver:", db1.driver)
    print("db2.driver:", db2.driver)
    print("Same instance?", db1 is db2)  # False (transient)

    print("\n" + "=" * 60)
    print("3. Singleton binding")
    print("=" * 60)
    # Register before we ever resolve it so the callback fires on first creation
    container.resolving(Logger, lambda instance, c: instance.log("Created!"))
    container.singleton(Logger)
    logger1 = container.make(Logger)
    logger2 = container.make(Logger)
    print("Same instance?", logger1 is logger2)  # True

    print("\n" + "=" * 60)
    print("4. Alias")
    print("=" * 60)
    container.alias(DatabaseConnection, "db")
    print("Resolving alias 'db' gives DatabaseConnection?", isinstance(container.make("db"), DatabaseConnection))

    print("\n" + "=" * 60)
    print("5. Automatic constructor injection")
    print("=" * 60)
    container.bind(DatabaseConnection, lambda c, params=None: DatabaseConnection("mysql"))
    repo = container.make(Repository)
    print("Repository.db.driver:", repo.db.driver)

    print("\n" + "=" * 60)
    print("6. call() – inject dependencies into a function")
    print("=" * 60)
    def send_welcome_email(mailer: Mailer, name: str):
        return mailer.send(name, "Welcome aboard!")

    result = container.call(send_welcome_email, {"name": "alice@example.com"})
    print(result)

    print("\n" + "=" * 60)
    print("7. call() – inject dependencies into a [obj, 'method'] pair")
    print("=" * 60)
    result = container.call((repo, "all"))
    print(result)

    print("\n" + "=" * 60)
    print("8. Instance binding")
    print("=" * 60)
    shared_logger = Logger(prefix="SHARED")
    container.instance("shared.logger", shared_logger)
    print("Same logger object?", container.make("shared.logger") is shared_logger)

    print("\n" + "=" * 60)
    print("9. Method binding")
    print("=" * 60)
    def custom_handler(instance, c):
        return f"Custom handler on {type(instance).__name__}"

    container.bind_method("Logger@handle", custom_handler)
    print(container.call([logger1, "handle"]))

    print("\n" + "=" * 60)
    print("10. Contextual binding (primitive override)")
    print("=" * 60)
    # Bind the primitive '$backend' specifically when building Cache
    container.when(Cache).needs("$backend").give(MemcachedBackend())
    cache = container.make(Cache)
    print("Cache backend type:", type(cache.backend).__name__)

    print("\n" + "=" * 60)
    print("11. Tagging")
    print("=" * 60)
    container.tag([DatabaseConnection, Logger, Mailer], "services")
    tagged = container.tagged("services")
    print("Tagged services:", [type(s).__name__ for s in tagged])

    print("\n" + "=" * 60)
    print("12. Extending a resolved instance")
    print("=" * 60)
    container.extend(DatabaseConnection, lambda instance, c: setattr(instance, "extended", True) or instance)
    db3 = container.make(DatabaseConnection)
    print("Has 'extended' attr?", hasattr(db3, "extended"))

    print("\n" + "=" * 60)
    print("13. Global singleton access")
    print("=" * 60)
    InstanceContainer.set_instance(container)
    print("Global container present?", InstanceContainer.get_instance() is container)

    print("\n" + "=" * 60)
    print("14. ArrayAccess-style usage")
    print("=" * 60)
    container["magic_key"] = lambda c, params=None: "magic_value"
    print("container['magic_key'] =>", container["magic_key"])
    print("'magic_key' in container?", "magic_key" in container)

    print("\n" + "=" * 60)
    print("Example complete!")
    print("=" * 60)
