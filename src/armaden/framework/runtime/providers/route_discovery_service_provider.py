import logging
import os
import sys
from importlib import import_module
from pathlib import Path
from typing import Any

from returns.result import Success

from armaden.framework.classes.service_provider import ServiceProvider
from armaden.framework.facades import App
from armaden.framework.protocols.application import ApplicationInterface
from armaden.framework.runtime.http.routing.route_group import RouteGroupStack
from armaden.framework.runtime.module_loader import ModuleLoader, ModuleLoaderError
from armaden.framework.errors.error import Error
from armaden.framework.utils.types import Result
from returns.pipeline import is_successful
from returns.result import Failure

logger = logging.getLogger(__name__)


class RouteDiscoveryServiceProvider(ServiceProvider):
    name = 'route_discovery'

    def register(self) -> Result[None]:
        app_dir = os.getenv('APP_DIR')
        if not app_dir:
            logger.debug("No APP_DIR set; skipping route discovery")
            return Success(None)

        routes_dir = Path(app_dir).absolute() / 'routes'
        if not routes_dir.is_dir():
            logger.debug("No routes/ directory found at %s", routes_dir)
            return Success(None)

        route_files = sorted(
            (f for f in routes_dir.rglob('*.py')
             if f.is_file() and not f.name.startswith(('.', '_'))),
            key=lambda f: str(f),
        )

        if not route_files:
            return Success(None)

        user_app = self._container.make(ApplicationInterface)
        route_groups = self._get_route_groups(user_app)
        base_dir = str(Path(app_dir).absolute())
        sys.path.insert(0, base_dir)

        try:
            for file in route_files:
                group_config = self._find_group_for_file(file, route_groups)
                if group_config:
                    RouteGroupStack.get_instance().push(**group_config)

                try:
                    relative = file.relative_to(base_dir).with_suffix('')
                    dotted = '.'.join(relative.parts)
                    import_module(dotted)
                    logger.debug("Loaded route file: %s", dotted)
                except Exception as exc:
                    logger.error("Failed to load route file %s: %s", file, exc)
                finally:
                    if group_config:
                        RouteGroupStack.get_instance().pop()
        finally:
            if base_dir in sys.path:
                sys.path.remove(base_dir)

        logger.info("Discovered %d route file(s) in routes/", len(route_files))
        return Success(None)

    def _get_route_groups(self, user_app: ApplicationInterface) -> dict[str, dict[str, Any]]:
        try:
            groups_method = getattr(user_app, 'route_groups', None)
            if callable(groups_method):
                return groups_method()
        except Exception as exc:
            logger.warning("Failed to read route_groups from Application: %s", exc)
        return {}

    def _find_group_for_file(
        self,
        file_path: Path,
        route_groups: dict[str, dict[str, Any]],
    ) -> dict[str, Any] | None:
        stem = file_path.stem
        if stem in route_groups:
            return route_groups[stem]
        for key, config in route_groups.items():
            if file_path.match(f'{key}.py'):
                return config
        return None
