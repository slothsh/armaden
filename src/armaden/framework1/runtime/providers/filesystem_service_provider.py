from __future__ import annotations

import logging

from returns.result import Success

from armaden.framework.classes.service_provider import ServiceProvider
from armaden.framework.filesystem import create_filesystem
from armaden.framework.protocols.filesystem import Filesystem
from armaden.framework.utils.types import Result

logger = logging.getLogger(__name__)


class FilesystemServiceProvider(ServiceProvider):
    name = 'filesystem'

    def register(self) -> Result[None]:
        application = self._container.make('app')
        config = application.config('filesystems', {}) or {}
        disks_config = config.get('disks', {}) or {}
        default_name = config.get('default')

        if not disks_config:
            disks_config = {
                'local': {
                    'driver': 'local',
                    'root': 'storage/app',
                    'url': '/storage',
                    'visibility': 'public',
                }
            }
            default_name = 'local'
            logger.info("No filesystem disks configured; falling back to default 'local' disk")

        disk_map: dict[str, Filesystem] = {}
        default_disk: Filesystem | None = None
        default_disk_name: str | None = default_name

        for disk_name, raw_config in disks_config.items():
            try:
                disk_config = {**(raw_config or {})}
                filesystem = create_filesystem(disk_config)
            except Exception as exception:
                logger.warning(
                    "Failed to create filesystem disk '%s': %s",
                    disk_name, exception,
                )
                continue

            disk_map[disk_name] = filesystem
            self._container.instance(f'filesystem.disk.{disk_name}', filesystem)

            if disk_name == default_name:
                default_disk = filesystem

        if default_disk is None and disk_map:
            default_disk_name = next(iter(disk_map))
            default_disk = disk_map[default_disk_name]

        if default_disk is not None and default_disk_name is not None:
            self._container.instance('filesystem.disk.default', default_disk)
            self._container.instance('filesystem.default', default_disk_name)
            self._container.instance(Filesystem, default_disk)
        else:
            logger.warning("No filesystem disks were registered")

        self._container.instance('filesystem.disks', disk_map)

        logger.info(
            "Registered filesystem disks: %s (default: %s)",
            ', '.join(disk_map) or 'none',
            default_disk_name if default_disk else 'none',
        )

        return Success(None)

    def boot(self) -> Result[None]:
        return Success(None)
