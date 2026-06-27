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

## Build an Application

Implement `ApplicationInterface` and register a task via a service provider:

```python
# app/application.py
from armaden.framework.application import Application
from armaden.framework.utils.types import Result
from returns.result import Success

class MyApplication(Application):
    def boot(self) -> Result[None]:
        return Success(None)
```

```python
# app/providers/app_service_provider.py
from armaden.framework.classes.service_provider import ServiceProvider
from armaden.framework.classes.task import TaskBuilder
from armaden.framework.facades import app
from armaden.framework.utils.types import Result
from returns.result import Success

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

The runtime discovers service providers at `app.providers`.

## Run with Docker

```dockerfile
FROM ghcr.io/OWNER/armaden:latest

ENV APP_DIR=/app
COPY app /app
```

Or mount at runtime:

```bash
docker run -v ./app:/app -e APP_DIR=/app ghcr.io/OWNER/armaden:latest
```

If `APP_DIR` is not set or contains no `application.py`, the runtime falls back to a no-op default application.

## Build Locally

```bash
poetry install
poetry build
```

## CLI Entrypoint

```bash
poetry run armaden
```

Or as a module:

```bash
python -m armaden.framework.runtime
```
