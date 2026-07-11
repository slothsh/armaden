# Graph Report - armaden  (2026-07-11)

## Corpus Check
- 168 files · ~31,637 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1706 nodes · 2824 edges · 286 communities (58 shown, 228 thin omitted)
- Extraction: 90% EXTRACTED · 10% INFERRED · 0% AMBIGUOUS · INFERRED: 279 edges (avg confidence: 0.56)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `c41600e4`
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
- Self
- .server_id
- .single_threaded_update
- .staggering_budget
- .streams_delta
- Any
- Config
- Self
- TaskInjector
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
- __init__.py
- Any
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
- Result
- .freeze_check_mode
- TaskGraph
- TaskGraph
- .list_scenarios
- .log_scr_checksum
- Any
- Result
- .no_backend
- .no_sound
- CoreApplicationInterface
- config.py
- .rpl_encode_as_long_jobs
- Result
- TaskGraph
- .server_world
- TaskGraph
- DatagramTransportInterface
- Any
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
- Result
- Result

## God Nodes (most connected - your core abstractions)
1. `InstanceContainer` - 102 edges
2. `ArmaReforgerServerExecutable` - 85 edges
3. `Request` - 49 edges
4. `app()` - 40 edges
5. `Supervisor` - 37 edges
6. `BattleEyeRconClient` - 36 edges
7. `CoreApplication` - 34 edges
8. `BattleEyeRconServer` - 29 edges
9. `TaskBuilder` - 26 edges
10. `AuthManager` - 23 edges

## Surprising Connections (you probably didn't know these)
- `RestartRequestData` --uses--> `HealthStatus`  [INFERRED]
  user/app/http/dto/lifecycle_data.py → src/armaden/framework/enums/health_status.py
- `ServiceHealthData` --uses--> `HealthStatus`  [INFERRED]
  user/app/http/dto/lifecycle_data.py → src/armaden/framework/enums/health_status.py
- `ShutdownRequestData` --uses--> `HealthStatus`  [INFERRED]
  user/app/http/dto/lifecycle_data.py → src/armaden/framework/enums/health_status.py
- `LifecycleController` --uses--> `Controller`  [INFERRED]
  user/app/http/controllers/lifecycle_controller.py → src/armaden/framework/runtime/http/controller.py
- `_UnresolvedSentinel` --uses--> `Task`  [INFERRED]
  src/armaden/framework/runtime/task_injector.py → src/armaden/framework/runtime/task.py

## Import Cycles
- None detected.

## Communities (286 total, 228 thin omitted)

### Community 0 - "IoC Container Binding"
Cohesion: 0.13
Nodes (7): ArmaReforgerServerExecutable, Bind the server to specific addresses / ports.          Keyword Args:, Configure BattlEye / RCON remote console.          Keyword Args:             add, Force loading a session save even if version mismatched., Skip the initial load request and start a brand-new session., Limit the number of streams opened for a client (1..1000)., Threads for short jobs (capped to CPU count or 16).

### Community 1 - "Supervisor Request Handling"
Cohesion: 0.24
Nodes (5): GraphTaskRuntime, Semaphore, _result_error(), _run_shutdown(), TaskInjector

### Community 2 - "Arma Reforger Server Config"
Cohesion: 0.05
Nodes (6): Parameter, BindingResolutionException, ContextualAttribute, ContextualBindingBuilder, InstanceContainer, Any

### Community 3 - "Application Kernel Interface"
Cohesion: 0.06
Nodes (17): AppServiceProvider, ServiceProvider, Path, RestartPolicy, HttpServiceProvider, Result, _BuiltCallbacks, _BuiltTask (+9 more)

### Community 4 - "App Facade Container"
Cohesion: 0.11
Nodes (3): app(), Any, T

### Community 5 - "Executable Argument Builder"
Cohesion: 0.15
Nodes (9): ArmaReforgerServerConfig, AppServiceProvider, Result, ArmaReforgerServer, ArmaReforgerServerError, ArmaReforgerServerException, ExecutableContainer, PathContainer (+1 more)

### Community 6 - "Task Lifecycle Management"
Cohesion: 0.07
Nodes (16): BoundMethod, Error, ErrorKindInterface, Enforces that any error type object has a code string and message string., Accepts any Enum instance that implements a .message property., GenericError, ModuleLoader, ModuleLoaderError (+8 more)

### Community 7 - "Async Datagram Transport"
Cohesion: 0.10
Nodes (9): DatagramProtocol, DatagramTransport, Exception, entry(), main(), entry(), main(), AsyncDatagramTransport (+1 more)

### Community 10 - "Core Application Bootstrap"
Cohesion: 0.11
Nodes (9): set_application(), bootstrap_console(), bootstrap_http(), ConsoleKernel, HttpKernel, Kernel, RuntimeEntry, ConsoleServiceProvider (+1 more)

### Community 11 - "BattleEye RCON Server"
Cohesion: 0.15
Nodes (7): BattleEyeRconServer, Client, ClientState, ResponseMessage, LoginStatus, LoginResponsePacket, IntEnum

### Community 12 - "Console Kernel Bootstrap"
Cohesion: 0.14
Nodes (5): AbstractEventLoop, Future, InstanceContainer, Supervisor, TaskStateData

### Community 13 - "Scaffold File Generator"
Cohesion: 0.14
Nodes (10): Generator, GeneratorResult, _detect_poetry_package_path(), _fmt_list(), main(), _print_result(), # TODO: Register bindings on the service container., # TODO: Build and register tasks with the supervisor. (+2 more)

### Community 14 - "BattleEye RCON Client"
Cohesion: 0.13
Nodes (5): BattleEyeRconClient, ClientStatus, # TODO: handle stateful messages (responses to sequenced messages), # TODO: implement event system, # TODO: handle stateful messages (responses to sequences)

### Community 16 - "Server Path Configuration"
Cohesion: 0.05
Nodes (21): Executable, Dictionary, ArmaReforgerRconClient, A2SConfig, Config, GameConfig, GamePropertiesConfig, GamePropertiesPersistence (+13 more)

### Community 17 - "BattleEye Packet Protocol"
Cohesion: 0.18
Nodes (3): Message, Packet, UnknownPacket

### Community 18 - "Framework Service Providers"
Cohesion: 0.05
Nodes (23): ABC, Application, ApplicationBase, Application (ApplicationBase), Application, Configurable, _resolve_config_type(), ApplicationInterface (+15 more)

### Community 19 - "Typed Environment Config"
Cohesion: 0.13
Nodes (11): _ExclusiveWorker, RequestInfoData, _SharedWorker, SupervisorError, TaskRecord, ThreadInfoData, _WorkerBase, WorkerPool (+3 more)

### Community 21 - "Datagram Packet Parsing"
Cohesion: 0.18
Nodes (3): Config, Give, Tag

### Community 22 - "FastAPI Default Application"
Cohesion: 0.31
Nodes (4): TaskInjector, _UnresolvedSentinel, Task, TaskGraph

### Community 23 - "Module Discovery Loader"
Cohesion: 0.22
Nodes (3): AsyncStreamCallback, ProcessInfoData, TaskRuntime

### Community 24 - "Request"
Cohesion: 0.06
Nodes (20): HttpKernel, Middleware, MiddlewarePipeline, json_response(), JSONResponse, response(), ResponseFactory, ApiUser (+12 more)

### Community 25 - "lifecycle_controller.py"
Cohesion: 0.24
Nodes (7): Lifecycle, Pipeline, CollectServerTelemetryTask, FormatTelemetryReportTask, Result, TelemetryAlertTask, TelemetryReadinessProbeTask

### Community 28 - "Server Message Packet"
Cohesion: 0.20
Nodes (3): CommandHeader, CommandResponsePacket, BattleEyeInvalidPacketException

### Community 29 - "Config Value Management"
Cohesion: 0.05
Nodes (17): __getattr__(), _LegacyTask, Self, TaskThreadingPolicy, TaskBuilder, Lifecycle, Pipeline, Self (+9 more)

### Community 30 - "Player Response Parsing"
Cohesion: 0.06
Nodes (18): TaskThreadingPolicy, ArmaReforgerExecutableFlag, ArmaReforgerExecutableFlagError, Arma Reforger CLI startup flags., SteamCMD CLI command flags (prefixed with ``+``)., SteamCmdExecutableFlag, ServiceProvider, RestartPolicy (+10 more)

### Community 31 - "SupervisorRequestData"
Cohesion: 0.26
Nodes (6): FastAPI, DefaultApi, DefaultApiError, Any, Result, TaskRuntimeInterface

### Community 32 - "Server Message Response"
Cohesion: 0.21
Nodes (3): RequestMessage, KeepAlivePacket, LoginRequestPacket

### Community 35 - "Async Subprocess Dispatch"
Cohesion: 0.14
Nodes (5): config(), env(), Facade for reading typed environment variables from the application., config(), config()

### Community 37 - "App Config Module"
Cohesion: 0.09
Nodes (8): ProcessBuilder, _ProcessTask, Any, AsyncStreamCallback, Path, Result, SubprocessHandle, ProcessFacade

### Community 38 - "Steam Query Bind Address"
Cohesion: 0.19
Nodes (4): ErrorInterface, Result, SupervisorRequestInterface, SupervisorInterface

### Community 40 - "Addon Auto Repair Flag"
Cohesion: 0.15
Nodes (5): APIRouter, Controller, RouteCompiler, RouteParameter, HttpKernel

### Community 45 - "Debugger Port Setting"
Cohesion: 0.25
Nodes (3): Bind, Scoped, Singleton

### Community 49 - "Crash File Retention Flag"
Cohesion: 0.18
Nodes (5): Any, Task, TaskPolicy, MultiImplementation, TaskThreadingPolicy

### Community 52 - "Game Language Setting"
Cohesion: 0.08
Nodes (8): route(), URL, RequestContext, RouteNotFoundException, RouteParameterMissingException, UrlGenerator, auth(), request()

### Community 53 - "Server FPS Cap"
Cohesion: 0.33
Nodes (3): PlayerResponseData, Parse a single data row from ``players`` output.          Returns ``None``  if t, A connected player returned by the ``players`` command.

### Community 62 - ".custom"
Cohesion: 0.07
Nodes (11): ConcurrencyBuilder, Any, Result, ScheduleBuilder, _ScheduledTask, ConcurrencyFacade, ScheduleFacade, Any (+3 more)

### Community 68 - "Agent Guidelines Docs"
Cohesion: 0.07
Nodes (19): app() facade, SupervisorRequestArgs, SupervisorRequestData, HealthStatus, SupervisorRequestKind, GetAppStatus, RestartAppService, ShutdownAppService (+11 more)

### Community 74 - "ArmaDen Documentation"
Cohesion: 0.16
Nodes (3): SupervisorRequestInterface, GroupState, RouteGroupStack

### Community 79 - "Package Init Module"
Cohesion: 0.15
Nodes (8): Event, ProgressChannel, AbstractEventLoop, Any, AsyncStreamCallback, Path, Result, TaskRuntime

### Community 107 - "TaskInjector"
Cohesion: 0.18
Nodes (6): DuplicateTaskNameError, TaskError, TaskGraphCycleError, UnresolvedDependencyError, PolicyEngine, Any

### Community 161 - "Any"
Cohesion: 0.22
Nodes (8): ArmaDen, Build Locally, CLI Entrypoints, Install, Manual Application Setup, Packages, Run with Docker, Scaffold an Application

### Community 175 - "Result"
Cohesion: 0.33
Nodes (5): MANDATORY: Code Comment Conventions, MANDATORY: Git Rules, MANDATORY: Local Code Search/Traversal, MANDATORY: Use td for Task Management, MANDATORY: Worktree Management

### Community 249 - "DatagramTransportInterface"
Cohesion: 0.22
Nodes (3): RconPacketInterface, DatagramTransportInterface, Protocol

## Knowledge Gaps
- **27 isolated node(s):** `TaskGraphState`, `armaden`, `ApiResponseData`, `MANDATORY: Local Code Search/Traversal`, `MANDATORY: Use td for Task Management` (+22 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **228 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ArmaReforgerServerExecutable` connect `IoC Container Binding` to `.addons_verify`, `Result`, `.autoshutdown`, `.backend_local_storage`, `.cfg`, `.create_db`, `.custom`, `.debugger`, `.debugger_port`, `.disable_crash_reporter`, `.disable_shaders_build`, `Server Path Configuration`, `.jobsys_long_worker_count`, `.limit_fps`, `.log_rdb_checksum`, `.logs_dir`, `.minidump`, `.nds`, `.no_splash`, `.no_throw`, `.nwk_resolution`, `.profile`, `.scenario`, `.script_authorize_all`, `.server_id`, `Local Backend Storage Flag`, `Freeze Detection Timeout`, `List Scenarios Flag`, `Log Append Mode Flag`, `.autoshutdown`, `Error Dialog Suppression`, `.backend_disable_storage`, `.backend_local_storage`, `.debugger_port`, `.disable_ai`, `Global Streaming Budget`, `Package Init Module`, `Package Init Module`, `Package Entry Point`, `Package Init Module`, `Package Init Module`, `Package Init Module`, `Package Init Module`, `Package Init Module`, `.freeze_check`, `.jobsys_long_worker_count`, `.keep_crash_files`, `.keep_session_save`, `.log_voting`, `.nds`, `.no_backend`, `.nwk_resolution`, `.server_id`, `.staggering_budget`, `.disable_navmesh_streaming`, `.streams_delta`, `.freeze_check_mode`, `Any`, `Config`, `.list_scenarios`, `Self`, `.log_scr_checksum`, `TaskRuntimeInterface`, `__init__.py`, `.no_backend`, `.no_sound`, `Result`, `.rpl_encode_as_long_jobs`, `.server_world`, `.addon_temp_dir`?**
  _High betweenness centrality (0.171) - this node is a cross-community bridge._
- **Why does `Executable` connect `Server Path Configuration` to `IoC Container Binding`, `Framework Service Providers`?**
  _High betweenness centrality (0.139) - this node is a cross-community bridge._
- **Why does `SupervisorInterface` connect `Steam Query Bind Address` to `DatagramTransportInterface`, `.add_task`, `.custom`?**
  _High betweenness centrality (0.100) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `InstanceContainer` (e.g. with `._is_container_type()` and `DeferrableProvider`) actually correct?**
  _`InstanceContainer` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `ArmaReforgerServerExecutable` (e.g. with `Executable` and `Dictionary`) actually correct?**
  _`ArmaReforgerServerExecutable` has 4 INFERRED edges - model-reasoned connections that need verification._
- **What connects `TaskGraphState`, `armaden`, `Accepts any Enum instance that implements a .message property.` to the rest of the system?**
  _121 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `IoC Container Binding` be split into smaller, more focused modules?**
  _Cohesion score 0.1323529411764706 - nodes in this community are weakly interconnected._