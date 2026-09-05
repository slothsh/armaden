from __future__ import annotations

import logging
from collections.abc import Mapping
from typing import cast, override

from returns.result import Success

from armaden.framework.protocols.container_protocol import ContainerProtocol
from armaden.framework.protocols.core_application_protocol import CoreApplicationProtocol
from armaden.framework.protocols.filesystem_protocol import FilesystemProtocol
from armaden.framework.runtime.filesystem.filesystem_factory import create_filesystem
from armaden.framework.runtime.service_provider.service_provider import ServiceProvider
from armaden.framework.runtime.supervisor.task.dto.task_graph_data import TaskGraphData
from armaden.framework.types.result import Result

logger = logging.getLogger(__name__)


class FilesystemServiceProvider(ServiceProvider):
    name: str = 'filesystem'

    def __init__(self, container: ContainerProtocol) -> None:
        super().__init__(container)
        self._registered: bool = False


    @override
    def boot(self) -> Result[None]:
        if not self._registered:
            self._build_disks()
            self._registered = True
        return Success(None)


    @override
    def register(self) -> Result[None]:
        return Success(None)


    def _build_disks(self) -> None:
        application = cast(
            CoreApplicationProtocol[TaskGraphData],
            self._container.make('app'),
        )
        configured = application.config('filesystems')
        user_configuration: Mapping[str, object] = (
            cast(Mapping[str, object], configured)
            if isinstance(configured, Mapping)
            else {}
        )
        configuration = user_configuration
        disks = configuration.get('disks')
        disk_configuration: Mapping[str, object] = (
            cast(Mapping[str, object], disks)
            if isinstance(disks, Mapping)
            else {}
        )
        default_name = configuration.get('default')
        configured_default = (
            default_name if isinstance(default_name, str) else 'local'
        )

        disk_map: dict[str, FilesystemProtocol] = {}
        for disk_name, raw_config in disk_configuration.items():
            if not isinstance(raw_config, Mapping):
                continue
            try:
                filesystem = create_filesystem(cast(Mapping[str, object], raw_config))
            except Exception as exception:
                logger.warning(
                    "Failed to create filesystem disk '%s': %s",
                    disk_name,
                    exception,
                )
                continue
            disk_map[disk_name] = filesystem
            _ = self._container.instance(
                f'filesystem.disk.{disk_name}',
                filesystem,
            )

        default_disk = disk_map.get(configured_default)
        default_disk_name = configured_default
        if default_disk is None and disk_map:
            default_disk_name, default_disk = next(iter(disk_map.items()))

        if default_disk is not None:
            _ = self._container.instance('filesystem.disk.default', default_disk)
            _ = self._container.instance('filesystem.default', default_disk_name)
            _ = self._container.instance(FilesystemProtocol, default_disk)
        else:
            logger.warning('No filesystem disks were registered')

        _ = self._container.instance('filesystem.disks', disk_map)
        logger.info(
            'Registered filesystem disks: %s (default: %s)',
            ', '.join(disk_map) or 'none',
            default_disk_name if default_disk is not None else 'none',
        )
