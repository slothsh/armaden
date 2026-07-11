# Graph Report - armaden  (2026-07-11)

## Corpus Check
- 167 files · ~31,646 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1752 nodes · 3011 edges · 396 communities (58 shown, 338 thin omitted)
- Extraction: 83% EXTRACTED · 17% INFERRED · 0% AMBIGUOUS · INFERRED: 502 edges (avg confidence: 0.55)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `7c91a2b1`
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
- Application Health Status
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
- SupervisorRequestData
- Server Message Response
- packet.py
- App Lifecycle Callbacks
- Async Subprocess Dispatch
- Frontend Dependencies
- App Config Module
- Steam Query Bind Address
- Server Addon Loader
- Addon Auto Repair Flag
- KeepAlivePacket
- Auto Shutdown Flag
- Local Backend Storage Flag
- Resource Database Regeneration
- Debugger Port Setting
- Force Session Load Flag
- Freeze Detection Timeout
- Freeze Behaviour Mode
- Crash File Retention Flag
- .add_task
- Session Save Retention Flag
- Game Language Setting
- Server FPS Cap
- List Scenarios Flag
- Log Append Mode Flag
- Filesystem Logging Flag
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
- AbstractEventLoop
- AsyncStreamCallback
- Package Init Module
- Package Init Module
- Package Init Module
- Package Init Module
- Package Entry Point
- Package Init Module
- Package Init Module
- SupervisorRequestInterface
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
- TaskInterface
- ScheduleBuilder
- .server_id
- .single_threaded_update
- .staggering_budget
- .streams_delta
- SubprocessHandle
- Any
- Config
- Self
- ABC
- TaskRuntimeInterface
- __init__.py
- Result
- Kernel
- StrEnum
- InstanceContainer
- Parameter
- Any
- ABC
- Bind
- Parameter
- Result
- RouteRegistrar
- __init__.py
- RouteCompiler
- ServiceProvider
- __init__.py
- Task
- HttpServiceProvider
- AppServiceProvider
- ModuleLoader
- callable
- HealthStatus
- .dispatch_subprocess
- Any
- C
- Self
- __init__.py
- Result
- Route
- Result
- .bootstrap
- arma_reforger_server.py
- steamcmd_executable.py
- Any
- ApplicationInterface
- callable
- Path
- RouteDefinition
- Request
- Request
- Any
- Result
- SupervisorInterface
- Any
- Result
- Result
- Any
- Any
- Any
- Any
- Any
- Any
- FastAPI
- Any
- Any
- Any
- Any
- Any
- Any
- Result
- Result
- Result
- Any
- Path
- Result
- Result
- Any
- FastAPI
- Result
- AbstractEventLoop
- Any
- AsyncStreamCallback
- Path
- Result
- Self
- Any
- Parameter
- Any
- Any
- Config
- Path
- Result
- Any
- ArmaReforgerServerConfig
- Result
- Self
- Self
- Result
- Config
- Path
- PushValue
- Result
- AbstractEventLoop
- Any
- DatagramTransportFactory
- datetime
- Exception
- AbstractEventLoop
- DatagramTransportFactory
- datetime
- Exception
- Self
- AbstractEventLoop
- Any
- Exception
- Exception
- Any
- Result
- Result
- ArmaReforgerServerConfig
- .disable_navmesh_streaming
- ConsoleKernel
- .freeze_check_mode
- Kernel
- ApplicationInterface
- .list_scenarios
- __init__.py
- .log_scr_checksum
- Kernel
- Any
- .no_backend
- .no_sound
- CoreApplicationInterface
- config.py
- .rpl_encode_as_long_jobs
- AuthGuard
- Any
- .server_world
- Result
- DatagramTransportInterface
- StatusCallback
- __init__.py
- .addon_temp_dir
- Executable
- ApplicationInterface
- route_compiler.py
- ApplicationInterface
- .addons_verify
- RequestContext
- Result
- ServiceProvider
- Result
- Result
- .autoshutdown
- .backend_local_storage
- .cfg
- .create_db
- .custom
- .debugger
- .debugger_port
- .disable_crash_reporter
- .disable_shaders_build
- .jobsys_long_worker_count
- .limit_fps
- .log_rdb_checksum
- .logs_dir
- .minidump
- .nds
- .no_splash
- .no_throw
- .nwk_resolution
- .profile
- .scenario
- .script_authorize_all
- .server_id
- Any
- AsyncStreamCallback
- TaskThreadingPolicy
- Any
- Result
- Self
- SupervisorRequestInterface
- Self
- StatusCallback
- TaskCallback
- Any
- AsyncStreamCallback
- Path
- Result
- AbstractEventLoop
- Any
- Result
- Any
- AsyncStreamCallback
- Path
- Result
- Any
- Result
- Any
- Result
- Result
- Any
- Result
- AbstractEventLoop
- Any
- AsyncStreamCallback
- Path
- Result
- Self
- SupervisorRequestInterface
- Any
- Result
- Self
- Any
- Parameter
- Any
- Result
- TaskThreadingPolicy
- AbstractEventLoop
- Any
- AsyncStreamCallback
- Path
- Result
- Any
- Result
- Self
- Result
- Result
- Result
- Pipeline
- ProgressChannel
- RestartPolicy
- Any
- Any
- Result
- Self
- TaskThreadingPolicy
- Any
- Result
- SupervisorRequestInterface
- TaskInterface
- Self
- AsyncStreamCallback
- Path
- Result
- AbstractEventLoop
- Any
- InstanceContainer
- Result
- AsyncStreamCallback
- Path
- Result
- Result
- Any
- Result
- Result
- Any
- Result
- TaskRuntimeInterface
- Result
- Self
- Any
- Result
- Self
- Any
- Any
- Result
- AbstractEventLoop
- Any
- AsyncStreamCallback
- Path
- Result
- Any
- Result
- Self
- TaskRuntimeInterface
- SupervisorInterface
- Task
- TaskInterface
- Result
- Result
- Result
- ServiceProvider

## God Nodes (most connected - your core abstractions)
1. `InstanceContainer` - 119 edges
2. `ArmaReforgerServerExecutable` - 85 edges
3. `Request` - 49 edges
4. `Supervisor` - 47 edges
5. `app()` - 40 edges
6. `CoreApplication` - 39 edges
7. `BattleEyeRconClient` - 36 edges
8. `TaskGraph` - 33 edges
9. `Task` - 30 edges
10. `TaskGraphCompiler` - 29 edges

## Surprising Connections (you probably didn't know these)
- `AppServiceProvider` --uses--> `ServiceProvider`  [INFERRED]
  user/app/providers/app_service_provider.py → src/armaden/framework/classes/service_provider.py
- `TelemetryServiceProvider` --uses--> `ServiceProvider`  [INFERRED]
  user/app/providers/telemetry_service_provider.py → src/armaden/framework/classes/service_provider.py
- `CollectServerTelemetryTask` --uses--> `TaskRuntimeInterface`  [INFERRED]
  user/app/tasks/telemetry_tasks.py → src/armaden/framework/protocols/task_runtime.py
- `FormatTelemetryReportTask` --uses--> `TaskRuntimeInterface`  [INFERRED]
  user/app/tasks/telemetry_tasks.py → src/armaden/framework/protocols/task_runtime.py
- `TelemetryAlertTask` --uses--> `TaskRuntimeInterface`  [INFERRED]
  user/app/tasks/telemetry_tasks.py → src/armaden/framework/protocols/task_runtime.py

## Import Cycles
- None detected.

## Communities (396 total, 338 thin omitted)

### Community 0 - "IoC Container Binding"
Cohesion: 0.13
Nodes (7): ArmaReforgerServerExecutable, Bind the server to specific addresses / ports.          Keyword Args:, Configure BattlEye / RCON remote console.          Keyword Args:             add, Force loading a session save even if version mismatched., Skip the initial load request and start a brand-new session., Limit the number of streams opened for a client (1..1000)., Threads for short jobs (capped to CPU count or 16).

### Community 1 - "Supervisor Request Handling"
Cohesion: 0.07
Nodes (19): app() facade, SupervisorRequestArgs, SupervisorRequestData, HealthStatus, SupervisorRequestKind, GetAppStatus, RestartAppService, ShutdownAppService (+11 more)

### Community 2 - "Arma Reforger Server Config"
Cohesion: 0.14
Nodes (6): BindingResolutionException, CircularDependencyException, ContextualAttribute, EntryNotFoundException, SelfBuilding, Parameter

### Community 3 - "Application Kernel Interface"
Cohesion: 0.13
Nodes (3): AsyncStreamCallback, ProcessBuilder, Path

### Community 4 - "App Facade Container"
Cohesion: 0.11
Nodes (3): Any, app(), T

### Community 5 - "Executable Argument Builder"
Cohesion: 0.24
Nodes (5): ArmaReforgerServerConfig, TaskRuntimeInterface, ArmaReforgerServerError, ArmaReforgerServerException, ExecutableContainer

### Community 6 - "Task Lifecycle Management"
Cohesion: 0.07
Nodes (16): BoundMethod, Error, ErrorKindInterface, Enforces that any error type object has a code string and message string., Accepts any Enum instance that implements a .message property., GenericError, ModuleLoader, ModuleLoaderError (+8 more)

### Community 7 - "Async Datagram Transport"
Cohesion: 0.10
Nodes (9): DatagramProtocol, DatagramTransport, Exception, entry(), main(), entry(), main(), AsyncDatagramTransport (+1 more)

### Community 10 - "Core Application Bootstrap"
Cohesion: 0.24
Nodes (6): set_application(), bootstrap_console(), bootstrap_http(), HttpKernel, RuntimeEntry, TypedResult

### Community 11 - "BattleEye RCON Server"
Cohesion: 0.15
Nodes (7): BattleEyeRconServer, Client, ClientState, ResponseMessage, LoginStatus, LoginResponsePacket, IntEnum

### Community 12 - "Console Kernel Bootstrap"
Cohesion: 0.10
Nodes (3): AbstractEventLoop, CoreApplication, InstanceContainer

### Community 13 - "Scaffold File Generator"
Cohesion: 0.14
Nodes (10): Generator, GeneratorResult, _detect_poetry_package_path(), _fmt_list(), main(), _print_result(), # TODO: Register bindings on the service container., # TODO: Build and register tasks with the supervisor. (+2 more)

### Community 14 - "BattleEye RCON Client"
Cohesion: 0.13
Nodes (5): BattleEyeRconClient, ClientStatus, # TODO: handle stateful messages (responses to sequenced messages), # TODO: implement event system, # TODO: handle stateful messages (responses to sequences)

### Community 15 - "Arma Server Task Runtime"
Cohesion: 0.19
Nodes (16): TaskError, ConcurrencyFacade, ProcessFacade, ScheduleFacade, PolicyEngine, _ExclusiveWorker, ProcessInfoData, RequestInfoData (+8 more)

### Community 16 - "Server Path Configuration"
Cohesion: 0.05
Nodes (21): Executable, Dictionary, ArmaReforgerRconClient, A2SConfig, Config, GameConfig, GamePropertiesConfig, GamePropertiesPersistence (+13 more)

### Community 17 - "BattleEye Packet Protocol"
Cohesion: 0.18
Nodes (3): Message, Packet, UnknownPacket

### Community 18 - "Framework Service Providers"
Cohesion: 0.16
Nodes (8): Lifecycle, Pipeline, DuplicateTaskNameError, TaskGraphCycleError, UnresolvedDependencyError, TaskGraph, TaskGraphCompiler, _UnresolvedSentinel

### Community 19 - "Typed Environment Config"
Cohesion: 0.16
Nodes (6): GraphTaskRuntime, _result_error(), _run_shutdown(), WorkerPool, Semaphore, TaskInjector

### Community 21 - "Datagram Packet Parsing"
Cohesion: 0.18
Nodes (3): Config, Give, Tag

### Community 22 - "FastAPI Default Application"
Cohesion: 0.17
Nodes (3): ConcurrencyBuilder, TaskInjector, TaskGraph

### Community 23 - "Module Discovery Loader"
Cohesion: 0.14
Nodes (6): DefaultApi, ArmaReforgerServer, PathContainer, AppServiceProvider, Result, TaskRuntimeInterface

### Community 24 - "Request"
Cohesion: 0.06
Nodes (20): HttpKernel, Middleware, MiddlewarePipeline, json_response(), JSONResponse, response(), ResponseFactory, ApiUser (+12 more)

### Community 28 - "Server Message Packet"
Cohesion: 0.20
Nodes (3): CommandHeader, CommandResponsePacket, BattleEyeInvalidPacketException

### Community 29 - "Config Value Management"
Cohesion: 0.05
Nodes (8): __getattr__(), _LegacyTask, TaskBuilder, TaskBuilderInterface, TaskInterface, StatusCallback, TaskCallback, TaskThreadingPolicy

### Community 32 - "Server Message Response"
Cohesion: 0.21
Nodes (3): RequestMessage, KeepAlivePacket, LoginRequestPacket

### Community 35 - "Async Subprocess Dispatch"
Cohesion: 0.14
Nodes (5): config(), env(), Facade for reading typed environment variables from the application., config(), config()

### Community 38 - "Steam Query Bind Address"
Cohesion: 0.19
Nodes (3): ErrorInterface, SupervisorInterface, SupervisorRequestInterface

### Community 40 - "Addon Auto Repair Flag"
Cohesion: 0.25
Nodes (4): APIRouter, RouteCompiler, RouteParameter, HttpKernel

### Community 41 - "KeepAlivePacket"
Cohesion: 0.20
Nodes (7): RestartPolicy, _emit_banner(), TelemetryServiceProvider, CollectServerTelemetryTask, FormatTelemetryReportTask, TelemetryAlertTask, TelemetryReadinessProbeTask

### Community 42 - "Auto Shutdown Flag"
Cohesion: 0.12
Nodes (12): AppServiceProvider, ServiceProvider, TaskThreadingPolicy, ArmaReforgerExecutableFlag, ArmaReforgerExecutableFlagError, Arma Reforger CLI startup flags., ApplicationError, ApplicationException (+4 more)

### Community 45 - "Debugger Port Setting"
Cohesion: 0.25
Nodes (3): Bind, Scoped, Singleton

### Community 48 - "Freeze Behaviour Mode"
Cohesion: 0.15
Nodes (6): Application, ApplicationBase, Application (ApplicationBase), Application, DefaultApplication, Application

### Community 52 - "Game Language Setting"
Cohesion: 0.08
Nodes (8): route(), URL, RequestContext, RouteNotFoundException, RouteParameterMissingException, UrlGenerator, auth(), request()

### Community 53 - "Server FPS Cap"
Cohesion: 0.33
Nodes (3): PlayerResponseData, Parse a single data row from ``players`` output.          Returns ``None``  if t, A connected player returned by the ``players`` command.

### Community 74 - "ArmaDen Documentation"
Cohesion: 0.16
Nodes (3): SupervisorRequestInterface, GroupState, RouteGroupStack

### Community 79 - "Package Init Module"
Cohesion: 0.16
Nodes (4): Event, ProgressChannel, ProgressUpdate, TaskRuntime

### Community 100 - ".single_threaded_update"
Cohesion: 0.12
Nodes (3): Future, Supervisor, SupervisorRequestData

### Community 107 - "ABC"
Cohesion: 0.23
Nodes (4): ABC, Configurable, _resolve_config_type(), Controller

### Community 161 - "Any"
Cohesion: 0.22
Nodes (8): ArmaDen, Build Locally, CLI Entrypoints, Install, Manual Application Setup, Packages, Run with Docker, Scaffold an Application

### Community 175 - "Result"
Cohesion: 0.33
Nodes (5): MANDATORY: Code Comment Conventions, MANDATORY: Git Rules, MANDATORY: Local Code Search/Traversal, MANDATORY: Use td for Task Management, MANDATORY: Worktree Management

### Community 236 - "__init__.py"
Cohesion: 0.48
Nodes (3): MultiImplementation, TypeDiscoveryError, TypeDiscoveryServiceProvider

### Community 242 - "CoreApplicationInterface"
Cohesion: 0.06
Nodes (7): ErrorInterface, CoreApplicationInterface, KernelInterface, RconPacketInterface, DatagramTransportInterface, WrapperTransportInterface, Protocol

## Knowledge Gaps
- **26 isolated node(s):** `armaden`, `ApiResponseData`, `MANDATORY: Local Code Search/Traversal`, `MANDATORY: Use td for Task Management`, `MANDATORY: Worktree Management` (+21 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **338 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ArmaReforgerServerExecutable` connect `IoC Container Binding` to `.addons_verify`, `Result`, `.autoshutdown`, `.backend_local_storage`, `.cfg`, `.create_db`, `.custom`, `.debugger`, `.debugger_port`, `.disable_crash_reporter`, `.disable_shaders_build`, `Server Path Configuration`, `.jobsys_long_worker_count`, `.limit_fps`, `.log_rdb_checksum`, `.logs_dir`, `.minidump`, `.nds`, `.no_splash`, `.no_throw`, `.nwk_resolution`, `.profile`, `.scenario`, `.script_authorize_all`, `.server_id`, `Local Backend Storage Flag`, `Freeze Detection Timeout`, `List Scenarios Flag`, `Log Append Mode Flag`, `.autoshutdown`, `Error Dialog Suppression`, `.backend_disable_storage`, `.backend_local_storage`, `.debugger_port`, `.disable_ai`, `Global Streaming Budget`, `Package Init Module`, `Package Init Module`, `Package Entry Point`, `Package Init Module`, `Package Init Module`, `Package Init Module`, `Package Init Module`, `Package Init Module`, `.freeze_check`, `.jobsys_long_worker_count`, `.keep_crash_files`, `.keep_session_save`, `.log_voting`, `.nds`, `.no_backend`, `.nwk_resolution`, `.server_id`, `.staggering_budget`, `.disable_navmesh_streaming`, `.streams_delta`, `.freeze_check_mode`, `Any`, `Config`, `.list_scenarios`, `Self`, `.log_scr_checksum`, `TaskRuntimeInterface`, `__init__.py`, `.no_backend`, `.no_sound`, `Result`, `.rpl_encode_as_long_jobs`, `.server_world`, `.addon_temp_dir`?**
  _High betweenness centrality (0.169) - this node is a cross-community bridge._
- **Why does `Executable` connect `Server Path Configuration` to `IoC Container Binding`, `ABC`?**
  _High betweenness centrality (0.141) - this node is a cross-community bridge._
- **Why does `InstanceContainer` connect `Bound Method Resolution` to `Arma Reforger Server Config`, `.silent_crash_report`, `Agent Guidelines Docs`, `App Lifecycle Callbacks`, `.single_threaded_update`, `Auto Shutdown Flag`, `Console Kernel Bootstrap`, `Arma Server Task Runtime`, `StrEnum`, `Typed Environment Config`?**
  _High betweenness centrality (0.082) - this node is a cross-community bridge._
- **Are the 21 inferred relationships involving `InstanceContainer` (e.g. with `._is_container_type()` and `DeferrableProvider`) actually correct?**
  _`InstanceContainer` has 21 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `ArmaReforgerServerExecutable` (e.g. with `Executable` and `Dictionary`) actually correct?**
  _`ArmaReforgerServerExecutable` has 4 INFERRED edges - model-reasoned connections that need verification._
- **What connects `armaden`, `Accepts any Enum instance that implements a .message property.`, `Enforces that any error type object has a code string and message string.` to the rest of the system?**
  _120 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `IoC Container Binding` be split into smaller, more focused modules?**
  _Cohesion score 0.1323529411764706 - nodes in this community are weakly interconnected._