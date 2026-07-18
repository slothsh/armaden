from __future__ import annotations

import json
import pickle
import logging
from typing import Any

logger = logging.getLogger(__name__)


class CacheSerializationError(Exception):
    pass


_HEADER_PREFIX = 'ARMADEN_CACHE::'
_FORMAT_JSON = 'JSON'
_FORMAT_PICKLE = 'PICKLE'


class CacheSerializer:

    def __init__(self, config: dict) -> None:
        self._default_format = config.get('default', 'json')
        self._auto_detect_type = config.get('auto_detect_type', True)
        self._version = config.get('version', 1)

        if self._default_format not in (_FORMAT_JSON.lower(), _FORMAT_PICKLE.lower()):
            raise CacheSerializationError(
                f"Unsupported default serializer format '{self._default_format}'. "
                f"Supported formats: json, pickle"
            )

    def _build_header(self, format_name: str) -> str:
        return f'{_HEADER_PREFIX}V{self._version}::{format_name}::'

    def _parse_header(self, data: str | bytes) -> tuple[int, str, str | bytes] | None:
        # Parse at the byte level: pickle payloads contain non-UTF-8 bytes,
        # so a full decode-then-split would fail on those.
        if isinstance(data, str):
            raw = data.encode('utf-8')
            payload_is_str = True
        else:
            raw = data
            payload_is_str = False

        prefix = _HEADER_PREFIX.encode('utf-8')
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
                "Cache payload version mismatch: expected %s, found %s; "
                "attempting deserialization anyway",
                self._version, version,
            )

        if payload_is_str:
            return version, format_name, payload_bytes.decode('utf-8')
        return version, format_name, payload_bytes

    def serialize(self, value: Any) -> str | bytes:
        default = self._default_format.lower()

        if default == 'json':
            try:
                payload = json.dumps(value)
                return self._build_header(_FORMAT_JSON) + payload
            except TypeError as exception:
                if self._auto_detect_type:
                    try:
                        payload = pickle.dumps(value)
                    except Exception as pickling_error:
                        raise CacheSerializationError(
                            f"Failed to pickle value after JSON serialization failed: {pickling_error}"
                        ) from pickling_error
                    return self._build_header(_FORMAT_PICKLE).encode('utf-8') + payload
                raise CacheSerializationError(
                    f"Value is not JSON-serializable and auto_detect_type is disabled: {exception}"
                ) from exception

        if default == 'pickle':
            try:
                payload = pickle.dumps(value)
            except Exception as pickling_error:
                raise CacheSerializationError(
                    f"Failed to pickle value: {pickling_error}"
                ) from pickling_error
            return self._build_header(_FORMAT_PICKLE).encode('utf-8') + payload

        raise CacheSerializationError(
            f"Unsupported default serializer format '{self._default_format}'"
        )

    def deserialize(self, data: str | bytes) -> Any:
        if data is None:
            raise CacheSerializationError("Cannot deserialize None")

        parsed = self._parse_header(data)
        if parsed is not None:
            _, format_name, payload = parsed
            if format_name == _FORMAT_JSON:
                if isinstance(payload, bytes):
                    try:
                        payload = payload.decode('utf-8')
                    except UnicodeDecodeError as exception:
                        raise CacheSerializationError(
                            f"JSON cache payload was not valid UTF-8: {exception}"
                        ) from exception
                try:
                    return json.loads(payload)
                except (json.JSONDecodeError, TypeError) as exception:
                    raise CacheSerializationError(
                        f"Failed to JSON-deserialize cache payload: {exception}"
                    ) from exception
            if format_name == _FORMAT_PICKLE:
                if isinstance(payload, str):
                    payload = payload.encode('utf-8')
                try:
                    return pickle.loads(payload)
                except Exception as exception:
                    raise CacheSerializationError(
                        f"Failed to pickle-deserialize cache payload: {exception}"
                    ) from exception
            raise CacheSerializationError(
                f"Unknown cache payload format '{format_name}'"
            )

        if isinstance(data, bytes):
            try:
                text = data.decode('utf-8')
            except UnicodeDecodeError:
                try:
                    return pickle.loads(data)
                except Exception:
                    raise CacheSerializationError(
                        "Unversioned cache payload could not be decoded as UTF-8 or unpickled"
                    )
            candidate = text
        else:
            candidate = data

        try:
            return json.loads(candidate)
        except (json.JSONDecodeError, TypeError):
            pass

        try:
            return pickle.loads(candidate.encode('utf-8'))
        except Exception:
            pass

        return candidate
