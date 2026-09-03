from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import List

from armaden.framework.installer.templates import Templates


@dataclass
class GeneratorResult:
    created_dirs: List[Path] = field(default_factory=list)
    created_files: List[Path] = field(default_factory=list)
    skipped_files: List[Path] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors


class Generator:
    def __init__(self, root: Path | str | None = None, force: bool = False) -> None:
        self._root = Path(root).resolve() if root else Path.cwd().resolve()
        self._force = force

    def generate(self, name: str = "My Application") -> GeneratorResult:
        result = GeneratorResult()

        self._ensure_dir(self._root / "bootstrap", result)
        self._ensure_dir(self._root / "app" / "providers", result)
        self._ensure_dir(self._root / "config", result)

        self._write_file(
            self._root / "bootstrap" / "application.py",
            Templates.bootstrap_application(),
            result,
        )

        self._write_file(
            self._root / "bootstrap" / "providers.py",
            Templates.bootstrap_providers(),
            result,
        )

        self._write_file(
            self._root / "app" / "__init__.py",
            "",
            result,
        )

        self._write_file(
            self._root / "app" / "providers" / "__init__.py",
            "",
            result,
        )

        self._write_file(
            self._root / "app" / "providers" / "app_service_provider.py",
            Templates.app_service_provider(),
            result,
        )

        self._write_file(
            self._root / "config" / "app.py",
            Templates.config_app(name),
            result,
        )

        env_path = self._root / ".env"
        if env_path.exists() and not self._force:
            result.skipped_files.append(env_path)
        else:
            self._write_file(env_path, Templates.env(name), result)

        return result

    def _ensure_dir(self, path: Path, result: GeneratorResult) -> None:
        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)
            result.created_dirs.append(path)

    def _write_file(self, path: Path, content: str, result: GeneratorResult) -> None:
        try:
            if path.exists() and not self._force:
                result.skipped_files.append(path)
                return

            with open(path, "w", encoding="utf-8") as fh:
                fh.write(content)

            normalized = path.relative_to(self._root) if path.is_relative_to(self._root) else path
            result.created_files.append(normalized)
        except OSError as exc:
            result.errors.append(f"Failed to write {path}: {exc}")
