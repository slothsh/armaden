# ArmaDen

Framework, game server integrations, and runtime for building dedicated game server applications.

## Packages

| Package | Import | Purpose |
|---------|--------|---------|
| `armaden` | `armaden.framework` | IoC container, task scheduling, service providers, and protocols |
| `armaden` | `armaden.games` | Executable wrappers and game-specific integrations |
| `armaden` | `armaden.framework.runtime` | Application bootstrap, HTTP API, and module loader |

## Install

```toml
[tool.poetry.dependencies]
armaden = { url = "https://github.com/OWNER/REPO/releases/download/v0.1.0/armaden-0.1.0-py3-none-any.whl" }
```

## Scaffold an Application

After adding `armaden` as a dependency, generate the required directory structure and starter files:

```bash
poetry add git+https://github.com/slothsh/armaden.git
poetry run armaden-scaffold
```

This creates:

```
.
├── bootstrap/
│   ├── application.py    # Entry-point Application class
│   └── providers.py      # providers() entry point
├── app/
│   └── providers/
│       └── app_service_provider.py
├── config/
│   └── app.py
└── .env
```

Set `APP_DIR` (already included in the generated `.env`) and run:

```bash
poetry run armaden
```

Options:

- `--name` – application name (default: "My Application")
- `--path` – target directory (default: current directory)
- `--force` – overwrite existing files

## Manual Application Setup

Implement `ApplicationInterface` and register a task via a service provider:

```python
# bootstrap/application.py
from returns.result import Success
from armaden.framework.application import Application as ApplicationBase
from armaden.framework.utils.types import Result


class Application(ApplicationBase):
    def boot(self) -> Result[None]:
        return Success(None)
```

```python
# bootstrap/providers.py
from typing import List
from armaden.framework.classes.service_provider import ServiceProvider
from app.providers.app_service_provider import AppServiceProvider


def providers() -> List[ServiceProvider]:
    return [AppServiceProvider]
```

```python
# app/providers/app_service_provider.py
from returns.result import Success
from armaden.framework.classes.service_provider import ServiceProvider
from armaden.framework.classes.task import TaskBuilder
from armaden.framework.facades import app
from armaden.framework.utils.types import Result


class AppServiceProvider(ServiceProvider):
    name = "my_game"

    def register(self) -> Result[None]:
        return Success(None)

    def boot(self) -> Result[None]:
        task = (
            TaskBuilder()
            .name("my_task")
            .on_initialize(self.initialize)
            .on_run(self.run)
            .build()
        )
        app().supervisor.add_task(task)
        return Success(None)
```

The runtime loads `bootstrap/application.py` and `bootstrap/providers.py` from the directory pointed to by `APP_DIR`.

## Run with Docker

```dockerfile
FROM ghcr.io/OWNER/armaden:latest

ENV APP_DIR=/app
COPY . /app
```

Or mount at runtime:

```bash
docker run -v .:/app -e APP_DIR=/app ghcr.io/OWNER/armaden:latest
```

If `APP_DIR` is not set or contains no `bootstrap/application.py`, the runtime falls back to a no-op default application.

## Build Locally

```bash
poetry install
poetry build
```

## CLI Entrypoints

```bash
poetry run armaden          # Start the runtime
poetry run armaden-scaffold # Scaffold a new application
```

Or as a module:

```bash
python -m armaden.framework.runtime
```
