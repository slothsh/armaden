from __future__ import annotations

from enum import StrEnum


class PaperEnvironmentVariable(StrEnum):
    DEFAULT_CENTRAL_REPOSITORY = 'PAPER_DEFAULT_CENTRAL_REPOSITORY'
    MANAGEMENT_TLS_KEYSTORE_PASSWORD = 'MINECRAFT_MANAGEMENT_TLS_KEYSTORE_PASSWORD'
    VELOCITY_SECRET = 'PAPER_VELOCITY_SECRET'

    @classmethod
    def caution(cls) -> frozenset[PaperEnvironmentVariable]:
        return frozenset({
            cls.DEFAULT_CENTRAL_REPOSITORY,
            cls.MANAGEMENT_TLS_KEYSTORE_PASSWORD,
        })

    @classmethod
    def defaults(cls) -> dict[PaperEnvironmentVariable, str]:
        return {
            cls.DEFAULT_CENTRAL_REPOSITORY: 'https://maven-central.storage-download.googleapis.com/maven2',
        }

    @classmethod
    def unset_by_default(cls) -> frozenset[PaperEnvironmentVariable]:
        return frozenset({
            cls.MANAGEMENT_TLS_KEYSTORE_PASSWORD,
            cls.VELOCITY_SECRET,
        })
