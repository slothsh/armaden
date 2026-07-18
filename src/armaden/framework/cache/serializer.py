from __future__ import annotations

import base64
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

    def serialize(self, value: Any) -> str:
        default = self._default_format.lower()

        if default == 'json':
            try:
                payload = json.dumps(value)
                return self._build_header(_FORMAT_JSON) + payload
            except TypeError as exception:
                if not self._auto_detect_type:
                    raise CacheSerializationError(
                        f"Value is not JSON-serializable and auto_detect_type is disabled: {exception}"
                    ) from exception
                try:
                    raw = pickle.dumps(value)
                except Exception as pickling_error:
                    raise CacheSerializationError(
                        f"Failed to pickle value after JSON serialization failed: {pickling_error}"
                    ) from pickling_error
                encoded = base64.b64encode(raw).decode('ascii')
                return self._build_header(_FORMAT_PICKLE) + encoded

        if default == 'pickle':
            try:
                raw = pickle.dumps(value)
            except Exception as pickling_error:
                raise CacheSerializationError(
                    f"Failed to pickle value: {pickling_error}"
                ) from pickling_error
            encoded = base64.b64encode(raw).decode('ascii')
            return self._build_header(_FORMAT_PICKLE) + encoded

        raise CacheSerializationError(
            f"Unsupported default serializer format '{self._default_format}'"
        )

    def _deserialize_pickle_payload(self, payload: str | bytes) -> Any:
        if isinstance(payload, str):
            payload = payload.encode('ascii')
        try:
            raw = base64.b64decode(payload, validate=True)
        except Exception as exception:
            raise CacheSerializationError(
                f"Failed to base64-decode pickle cache payload: {exception}"
            ) from exception
        try:
            return pickle.loads(raw)
        except Exception as exception:
            raise CacheSerializationError(
                f"Failed to pickle-deserialize cache payload: {exception}"
            ) from exception

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
                return self._deserialize_pickle_payload(payload)
            raise CacheSerializationError(
                f"Unknown cache payload format '{format_name}'"
            )

        if isinstance(data, bytes):
            try:
                return pickle.loads(data)
            except Exception:
                try:
                    return json.loads(data.decode('utf-8'))
                except (UnicodeDecodeError, json.JSONDecodeError, TypeError):
                    raise CacheSerializationError(
                        "Unversioned cache payload could not be decoded as UTF-8 or unpickled"
                    )

        try:
            return json.loads(data)
        except (json.JSONDecodeError, TypeError):
            pass

        try:
            return pickle.loads(data.encode('utf-8'))
        except Exception:
            pass

        return data
