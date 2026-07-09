# Graph Report - armaden  (2026-07-09)

## Corpus Check
- 141 files · ~23,765 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1335 nodes · 2651 edges · 132 communities (44 shown, 88 thin omitted)
- Extraction: 90% EXTRACTED · 10% INFERRED · 0% AMBIGUOUS · INFERRED: 261 edges (avg confidence: 0.54)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `b54ad344`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- IoC Container Binding
- Supervisor Request Handling
- Arma Reforger Server Config
- Application Kernel Interface
- App Facade Container
- Executable Argument Builder
- Task Lifecycle Management
- Async Datagram Transport
- Bound Method Resolution
- Core Application Bootstrap
- BattleEye RCON Server
- Console Kernel Bootstrap
- Scaffold File Generator
- BattleEye RCON Client
- Arma Server Task Runtime
- Server Path Configuration
- BattleEye Packet Protocol
- Framework Service Providers
- Typed Environment Config
- Login Packet Processing
- Datagram Packet Parsing
- FastAPI Default Application
- Module Discovery Loader
- Request
- lifecycle_controller.py
- Command Request Packet
- Command Response Packet
- Server Message Packet
- Config Value Management
- Player Response Parsing
- Login Response Packet
- Server Message Response
- Type Discovery Provider
- App Lifecycle Callbacks
- Async Subprocess Dispatch
- Frontend Dependencies
- Steam Query Bind Address
- Server Addon Loader
- Addon Auto Repair Flag
- Server Auto Restart Flag
- Auto Shutdown Flag
- Local Backend Storage Flag
- Resource Database Regeneration
- Debugger Port Setting
- Force Session Load Flag
- Freeze Detection Timeout
- Freeze Behaviour Mode
- Crash File Retention Flag
- Log File Retention Limit
- Session Save Retention Flag
- Game Language Setting
- Server FPS Cap
- List Scenarios Flag
- Log Append Mode Flag
- Filesystem Logging Flag
- Log Verbosity Level
- .autoshutdown
- Error Dialog Suppression
- .backend_disable_storage
- .backend_local_storage
- .custom
- .debugger_port
- .disable_ai
- .disable_crash_reporter
- Global Streaming Budget
- .enable_night_grain
- Agent Guidelines Docs
- Arma Games Module
- Scaffold CLI Tool
- App Config File
- Environment Variables File
- ArmaDen Core Package
- ArmaDen Documentation
- Package Init Module
- Package Init Module
- Package Init Module
- .freeze_check
- .jobsys_long_worker_count
- .keep_crash_files
- .keep_session_save
- .log_voting
- .nds
- .no_backend
- .nwk_resolution
- .rpl_encode_as_long_jobs
- .rpl_timeout_ms
- .server_id
- .silent_crash_report
- .single_threaded_update
- .staggering_budget
- .streams_delta
- .vm_error_mode
- Any
- Config
- Self
- .resolve
- TaskRuntimeInterface
- __init__.py
- Result
- Kernel
- InstanceContainer
- Parameter
- Any
- ABC
- Bind
- Parameter
- Result
- RouteRegistrar
- __init__.py
- ServiceProvider
- JSONResponse
- HttpServiceProvider
- ModuleLoader
- Any
- C
- Self
- Result
- Any
- Result

## God Nodes (most connected - your core abstractions)
1. `InstanceContainer` - 113 edges
2. `ArmaReforgerServerExecutable` - 87 edges
3. `Request` - 45 edges
4. `CoreApplication` - 42 edges
5. `app()` - 39 edges
6. `BattleEyeRconClient` - 38 edges
7. `Packet` - 31 edges
8. `BattleEyeRconServer` - 30 edges
9. `RouteRegistrar` - 25 edges
10. `Supervisor` - 25 edges

## Surprising Connections (you probably didn't know these)
- `Build and Release Workflow` --references--> `armaden.framework.runtime`  [INFERRED]
  .github/workflows/build.yml → README.md
- `providers()` --references--> `ServiceProvider`  [EXTRACTED]
  user/bootstrap/providers.py → src/armaden/framework/classes/service_provider.py
- `HttpKernel` --uses--> `ApplicationInterface`  [INFERRED]
  src/armaden/framework/runtime/http/middleware/kernel.py → src/armaden/framework/protocols/application.py
- `HttpServiceProvider` --uses--> `HttpKernel`  [INFERRED]
  src/armaden/framework/runtime/providers/http_service_provider.py → src/armaden/framework/runtime/http/middleware/kernel.py
- `Bind` --uses--> `InstanceContainer`  [INFERRED]
  src/armaden/framework/attributes/__init__.py → src/armaden/framework/classes/instance_container.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Application Bootstrap Entry-Point Flow** — armaden_framework_runtime, bootstrap_application, bootstrap_providers, app_providers_app_service_provider [EXTRACTED 0.95]
- **Task Registration Flow via ServiceProvider** — app_providers_app_service_provider, armaden_framework_classes_task, armaden_framework_facades, armaden_framework_classes_service_provider [EXTRACTED 0.90]

## Communities (132 total, 88 thin omitted)

### Community 1 - "Supervisor Request Handling"
Cohesion: 0.10
Nodes (21): Future, SupervisorRequestArgs, SupervisorRequestData, SupervisorRequestKind, Any, StrEnum, SupervisorRequestInterface, ProcessInfoData (+13 more)

### Community 2 - "Arma Reforger Server Config"
Cohesion: 0.07
Nodes (14): ArmaReforgerServerExecutable, Bind the server to specific addresses / ports.          Keyword Args:, Configure BattlEye / RCON remote console.          Keyword Args:             add, Cap the server frame rate., Load a server-side addon (mod) by ID.          May be called multiple times to l, Server region tag (used by the server browser)., Skip the initial load request and start a brand-new session., Maximum players per faction (``FactionKey:Number`` pairs). (+6 more)

### Community 3 - "Application Kernel Interface"
Cohesion: 0.16
Nodes (16): Exception, BoundMethod, CircularDependencyException, EntryNotFoundException, LogicException, array_wrap(), get_class_for_callable(), get_contextual_attribute_from_dependency() (+8 more)

### Community 4 - "App Facade Container"
Cohesion: 0.11
Nodes (6): app(), Any, config(), Any, get_application(), T

### Community 5 - "Executable Argument Builder"
Cohesion: 0.06
Nodes (23): APIRouter, FastAPI, HttpKernel, RouteDefinition, HealthStatus, AsyncStreamCallback, Path, Result (+15 more)

### Community 6 - "Task Lifecycle Management"
Cohesion: 0.12
Nodes (6): Self, StatusCallback, TaskCallback, Task, TaskBuilder, TaskThreadingPolicy

### Community 7 - "Async Datagram Transport"
Cohesion: 0.13
Nodes (10): DatagramProtocol, DatagramTransport, entry(), main(), entry(), main(), AsyncDatagramTransport, Any (+2 more)

### Community 8 - "Bound Method Resolution"
Cohesion: 0.13
Nodes (4): AbstractEventLoop, DatagramTransportInterface, Exception, WrapperTransportInterface

### Community 10 - "Core Application Bootstrap"
Cohesion: 0.06
Nodes (23): AbstractEventLoop, Any, ApplicationInterface, callable, InstanceContainer, Path, ApplicationInterface, ApplicationError (+15 more)

### Community 11 - "BattleEye RCON Server"
Cohesion: 0.10
Nodes (13): IntEnum, BattleEyeRconServer, Client, ClientState, AbstractEventLoop, DatagramTransportFactory, datetime, Exception (+5 more)

### Community 12 - "Console Kernel Bootstrap"
Cohesion: 0.07
Nodes (18): ABC, Configurable, _resolve_config_type(), SelfBuilding, DeferrableProvider, Any, Result, ServiceProvider (+10 more)

### Community 13 - "Scaffold File Generator"
Cohesion: 0.14
Nodes (12): Generator, GeneratorResult, Path, _detect_poetry_package_path(), _fmt_list(), main(), _print_result(), Path (+4 more)

### Community 14 - "BattleEye RCON Client"
Cohesion: 0.11
Nodes (8): BattleEyeRconClient, Message, Any, datetime, Exception, # TODO: handle stateful messages (responses to sequenced messages), # TODO: implement event system, Self

### Community 15 - "Arma Server Task Runtime"
Cohesion: 0.06
Nodes (16): Protocol, Application, ErrorInterface, CoreApplicationInterface, KernelInterface, Any, Result, Result (+8 more)

### Community 16 - "Server Path Configuration"
Cohesion: 0.09
Nodes (12): Path, Result, Path to a server configuration JSON file., Directory for profiles (saves, logs, settings).          The directory is create, Redirect log output to the given directory., Path to a session save to load on startup., Additional directories to search for mods.          Multiple directories can be, Directory where addons are downloaded. (+4 more)

### Community 17 - "BattleEye Packet Protocol"
Cohesion: 0.15
Nodes (4): CommandHeader, CommandResponsePacket, BattleEyeInvalidPacketException, Packet

### Community 18 - "Framework Service Providers"
Cohesion: 0.12
Nodes (10): Middleware, NextCallable, AsgiMiddlewareAdapter, HttpKernel, Middleware, Any, Request, MiddlewarePipeline (+2 more)

### Community 19 - "Typed Environment Config"
Cohesion: 0.18
Nodes (15): ArmaReforgerRconClient, A2SConfig, Config, GameConfig, GamePropertiesConfig, GamePropertiesPersistence, JoinQueueConfig, OperatingConfig (+7 more)

### Community 20 - "Login Packet Processing"
Cohesion: 0.20
Nodes (4): ClientStatus, AbstractEventLoop, DatagramTransportFactory, KeepAlivePacket

### Community 22 - "FastAPI Default Application"
Cohesion: 0.20
Nodes (6): Config, Give, Any, Parameter, Tag, ContextualAttribute

### Community 23 - "Module Discovery Loader"
Cohesion: 0.15
Nodes (6): ArmaReforgerServerConfig, config(), env(), Any, Facade for reading typed environment variables from the application., config()

### Community 24 - "Request"
Cohesion: 0.08
Nodes (3): Any, Request, StarletteRequest

### Community 30 - "Player Response Parsing"
Cohesion: 0.33
Nodes (4): PlayerResponseData, Self, Parse a single data row from ``players`` output.          Returns ``None``  if t, A connected player returned by the ``players`` command.

### Community 77 - "Package Init Module"
Cohesion: 0.40
Nodes (4): MANDATORY: Code Comment Conventions, MANDATORY: Git Rules, MANDATORY: Local Code Search/Traversal, MANDATORY: Use td for Task Management

### Community 78 - "Package Init Module"
Cohesion: 0.09
Nodes (9): Any, route(), URL, request(), RequestContext, Any, RouteNotFoundException, RouteParameterMissingException (+1 more)

### Community 79 - "Package Init Module"
Cohesion: 0.12
Nodes (16): app() facade, Controller, GetAppStatus, RestartAppService, ShutdownAppService, Api, Controllers for API routes, LifecycleController (+8 more)

### Community 107 - ".resolve"
Cohesion: 0.05
Nodes (29): AppServiceProvider, Application, ApplicationBase, armaden.framework, Application (ApplicationBase), ServiceProvider, TaskBuilder, armaden.framework.runtime (+21 more)

### Community 109 - "__init__.py"
Cohesion: 0.06
Nodes (22): ModuleType, Executable, Path, PushValue, Result, Self, Error, ErrorKindInterface (+14 more)

### Community 117 - "Bind"
Cohesion: 0.25
Nodes (3): Bind, Scoped, Singleton

### Community 120 - "RouteRegistrar"
Cohesion: 0.07
Nodes (10): Any, RouteFacade, GroupState, Any, RouteGroup, RouteGroupStack, RouteParameter, Any (+2 more)

### Community 126 - "JSONResponse"
Cohesion: 0.36
Nodes (6): json_response(), JSONResponse, Any, response(), ResponseFactory, StarletteJSONResponse

## Knowledge Gaps
- **13 isolated node(s):** `MANDATORY: Local Code Search/Traversal`, `MANDATORY: Use td for Task Management`, `MANDATORY: Code Comment Conventions`, `MANDATORY: Git Rules`, `ServiceHealthData` (+8 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **88 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `InstanceContainer` connect `IoC Container Binding` to `Application Kernel Interface`, `Application Health Status`, `Console Kernel Bootstrap`, `Kernel`, `Arma Server Task Runtime`, `Parameter`, `Any`, `Bind`, `FastAPI Default Application`?**
  _High betweenness centrality (0.165) - this node is a cross-community bridge._
- **Why does `ArmaReforgerServerExecutable` connect `Arma Reforger Server Config` to `Executable Argument Builder`, `Server Path Configuration`, `Typed Environment Config`, `Command Response Packet`, `Config Value Management`, `Server Message Response`, `Type Discovery Provider`, `App Lifecycle Callbacks`, `Async Subprocess Dispatch`, `Frontend Dependencies`, `Steam Query Bind Address`, `Server Addon Loader`, `Addon Auto Repair Flag`, `Server Auto Restart Flag`, `Auto Shutdown Flag`, `Local Backend Storage Flag`, `Resource Database Regeneration`, `Debugger Port Setting`, `Force Session Load Flag`, `Freeze Detection Timeout`, `Freeze Behaviour Mode`, `Crash File Retention Flag`, `Log File Retention Limit`, `Game Language Setting`, `Server FPS Cap`, `List Scenarios Flag`, `Log Append Mode Flag`, `Filesystem Logging Flag`, `Log Verbosity Level`, `.autoshutdown`, `Error Dialog Suppression`, `.backend_disable_storage`, `.backend_local_storage`, `.custom`, `.debugger_port`, `.disable_ai`, `.disable_crash_reporter`, `Global Streaming Budget`, `.enable_night_grain`, `.freeze_check`, `.jobsys_long_worker_count`, `.keep_crash_files`, `.keep_session_save`, `.log_voting`, `.nds`, `.no_backend`, `.nwk_resolution`, `.rpl_encode_as_long_jobs`, `.rpl_timeout_ms`, `.server_id`, `.silent_crash_report`, `.single_threaded_update`, `.staggering_budget`, `.streams_delta`, `.vm_error_mode`, `__init__.py`?**
  _High betweenness centrality (0.160) - this node is a cross-community bridge._
- **Why does `Executable` connect `__init__.py` to `Arma Reforger Server Config`, `Typed Environment Config`, `Console Kernel Bootstrap`, `Executable Argument Builder`?**
  _High betweenness centrality (0.119) - this node is a cross-community bridge._
- **Are the 10 inferred relationships involving `InstanceContainer` (e.g. with `Application` and `Config`) actually correct?**
  _`InstanceContainer` has 10 INFERRED edges - model-reasoned connections that need verification._
- **Are the 5 inferred relationships involving `ArmaReforgerServerExecutable` (e.g. with `Executable` and `TaskRuntimeInterface`) actually correct?**
  _`ArmaReforgerServerExecutable` has 5 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `CoreApplication` (e.g. with `ApplicationInterface` and `HttpServiceProvider`) actually correct?**
  _`CoreApplication` has 3 INFERRED edges - model-reasoned connections that need verification._
- **What connects `MANDATORY: Local Code Search/Traversal`, `MANDATORY: Use td for Task Management`, `MANDATORY: Code Comment Conventions` to the rest of the system?**
  _105 weakly-connected nodes found - possible documentation gaps or missing edges._