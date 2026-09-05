from __future__ import annotations

import base64
import json
import logging
import pickle
from collections.abc import Mapping
from typing import ClassVar, override

from armaden.framework.protocols.cache_serializer_protocol import (
    CacheSerializerProtocol,
)
from armaden.framework.runtime.cache.exceptions.cache_serializer_error import (
    CacheSerializerError,
)

logger = logging.getLogger(__name__)


class CacheSerializer(CacheSerializerProtocol):
    HEADER_PREFIX: ClassVar[str] = 'ARMADEN_CACHE::'
    FORMAT_JSON: ClassVar[str] = 'JSON'
    FORMAT_PICKLE: ClassVar[str] = 'PICKLE'

    def __init__(self, config: Mapping[str, object]) -> None:
        default_format = config.get('default', 'json')
        self._default_format: str = (
            default_format if isinstance(default_format, str) else 'json'
        )
        auto_detect_type = config.get('auto_detect_type', True)
        self._auto_detect_type: bool = (
            auto_detect_type if isinstance(auto_detect_type, bool) else True
        )
        version = config.get('version', 1)
        self._version: int = version if isinstance(version, int) else 1
        if self._default_format.lower() not in {
            self.FORMAT_JSON.lower(),
            self.FORMAT_PICKLE.lower(),
        }:
            raise CacheSerializerError(f"Unsupported default serializer format '{self._default_format}'. Supported formats: json, pickle")


    @override
    def deserialize(self, data: str | bytes) -> object:
        parsed = self._parse_header(data)
        if parsed is not None:
            _, format_name, payload = parsed
            if format_name == self.FORMAT_JSON:
                return self._deserialize_json_payload(payload)
            if format_name == self.FORMAT_PICKLE:
                return self._deserialize_pickle_payload(payload)
            raise CacheSerializerError(
                f"Unknown cache payload format '{format_name}'"
            )

        if isinstance(data, bytes):
            try:
                return pickle.loads(data)
            except Exception:
                try:
                    return json.loads(data.decode('utf-8'))
                except (UnicodeDecodeError, json.JSONDecodeError, TypeError) as exception:
                    raise CacheSerializerError(
                        'Unversioned cache payload could not be decoded'
                    ) from exception

        try:
            return json.loads(data)
        except (json.JSONDecodeError, TypeError):
            pass
        try:
            return pickle.loads(data.encode('utf-8'))
        except Exception:
            return data


    @override
    def serialize(self, value: object) -> str:
        default_format = self._default_format.lower()
        if default_format == self.FORMAT_JSON.lower():
            try:
                payload = json.dumps(value)
                return self._build_header(self.FORMAT_JSON) + payload
            except TypeError as exception:
                if not self._auto_detect_type:
                    raise CacheSerializerError(
                        'Value is not JSON-serializable and auto detection is disabled'
                    ) from exception
                return self._serialize_pickle(value)
        if default_format == self.FORMAT_PICKLE.lower():
            return self._serialize_pickle(value)
        raise CacheSerializerError(
            f"Unsupported default serializer format '{self._default_format}'"
        )


    def _build_header(self, format_name: str) -> str:
        return f'{self.HEADER_PREFIX}V{self._version}::{format_name}::'


    def _deserialize_json_payload(self, payload: str | bytes) -> object:
        if isinstance(payload, bytes):
            try:
                payload = payload.decode('utf-8')
            except UnicodeDecodeError as exception:
                raise CacheSerializerError(
                    'JSON cache payload was not valid UTF-8'
                ) from exception
        try:
            return json.loads(payload)
        except (json.JSONDecodeError, TypeError) as exception:
            raise CacheSerializerError(
                'Failed to JSON-deserialize cache payload'
            ) from exception


    def _deserialize_pickle_payload(self, payload: str | bytes) -> object:
        encoded = payload.encode('ascii') if isinstance(payload, str) else payload
        try:
            raw = base64.b64decode(encoded, validate=True)
            return pickle.loads(raw)
        except Exception as exception:
            raise CacheSerializerError(
                'Failed to deserialize pickle cache payload'
            ) from exception


    def _parse_header(self, data: str | bytes) -> tuple[int, str, str | bytes] | None:
        raw = data.encode('utf-8') if isinstance(data, str) else data
        prefix = self.HEADER_PREFIX.encode('utf-8')
        if not raw.startswith(prefix):
            return None
        remaining = raw[len(prefix):]
        first = remaining.find(b'::')
        if first == -1:
            return None
        version_part = remaining[:first]
        if version_part.startswith(b'V'):
            version_part = version_part[1:]
        try:
            version = int(version_part)
        except ValueError:
            return None
        rest = remaining[first + 2:]
        second = rest.find(b'::')
        if second == -1:
            return None
        try:
            format_name = rest[:second].decode('utf-8')
        except UnicodeDecodeError:
            return None
        payload_bytes = rest[second + 2:]
        if version != self._version:
            logger.warning(
                'Cache payload version mismatch: expected %s, found %s',
                self._version,
                version,
            )
        if isinstance(data, str):
            return version, format_name, payload_bytes.decode('utf-8')
        return version, format_name, payload_bytes


    def _serialize_pickle(self, value: object) -> str:
        try:
            raw = pickle.dumps(value)
            encoded = base64.b64encode(raw).decode('ascii')
            return self._build_header(self.FORMAT_PICKLE) + encoded
        except Exception as exception:
            raise CacheSerializerError('Failed to serialize pickle cache payload') from exception
