from __future__ import annotations

import inspect
import logging
from enum import Enum
from types import ModuleType
from typing import cast, override

from returns.pipeline import is_successful
from returns.result import Success

from armaden.framework.protocols.class_discovery_protocol import (
    ClassDiscoveryProtocol,
)
from armaden.framework.runtime.application.module_loader import (
    ModuleLoader,
    ModuleLoaderError,
)
from armaden.framework.runtime.error.error import Error
from armaden.framework.types.result import Result

logger = logging.getLogger(__name__)


class ClassDiscovery(ClassDiscoveryProtocol):
    def __init__(self) -> None:
        pass


    @override
    def discover(self, paths: list[str]) -> Result[list[type[object]]]:
        discovered: list[type[object]] = []
        seen: set[type[object]] = set()
        for path in paths:
            result = ModuleLoader.try_discover_user_modules(path)
            if not is_successful(result):
                failure = cast(Error, result.failure())
                kind = cast(ModuleLoaderError, failure.kind)
                if kind == ModuleLoaderError.USER_DISCOVERY_INVALID_PATH:
                    logger.warning(
                        "Discovery path '%s' is unavailable, skipping",
                        path,
                    )
                    continue
                return result.map(lambda _: discovered)
            for module in result.unwrap():
                self._collect_declared_classes(module, discovered, seen)
        return Success(discovered)


    def _collect_declared_classes(
        self,
        module: ModuleType,
        discovered: list[type[object]],
        seen: set[type[object]],
    ) -> None:
        for _, value in inspect.getmembers(module, inspect.isclass):
            if value.__module__ != module.__name__:
                continue
            if inspect.isabstract(value):
                continue
            if issubclass(value, Enum):
                continue
            if value in seen:
                continue
            seen.add(value)
            discovered.append(value)
