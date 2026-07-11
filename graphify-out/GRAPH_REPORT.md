# Graph Report - feature-supervisor-task-refactor-worktree  (2026-07-11)

## Corpus Check
- 167 files · ~31,037 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1683 nodes · 2844 edges · 289 communities (63 shown, 226 thin omitted)
- Extraction: 87% EXTRACTED · 13% INFERRED · 0% AMBIGUOUS · INFERRED: 377 edges (avg confidence: 0.55)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `3f91b6d3`
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
- Typed Environment Config
- Login Packet Processing
- Datagram Packet Parsing
- FastAPI Default Application
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
- App Config Module
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
- Package Init Module
- Package Init Module
- Package Init Module
- Package Entry Point
- Package Init Module
- Package Init Module
- Package Init Module
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
- __init__.py
- JSONResponse
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
- Executable
- .freeze_check_mode
- Kernel
- types.py
- .list_scenarios
- .log_scr_checksum
- app() facade
- .no_backend
- .no_sound
- CoreApplicationInterface
- config.py
- .rpl_encode_as_long_jobs
- AuthGuard
- ArmaReforgerExecutableError
- .server_world
- SteamCmdExecutableError
- DatagramTransportInterface
- __init__.py
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
- Path
- Result

## God Nodes (most connected - your core abstractions)
1. `InstanceContainer` - 109 edges
2. `ArmaReforgerServerExecutable` - 85 edges
3. `Supervisor` - 49 edges
4. `Request` - 49 edges
5. `TaskGraph` - 44 edges
6. `app()` - 40 edges
7. `BattleEyeRconClient` - 36 edges
8. `CoreApplication` - 35 edges
9. `BattleEyeRconServer` - 29 edges
10. `TaskGraphCompiler` - 26 edges

## Surprising Connections (you probably didn't know these)
- `RestartRequestData` --uses--> `HealthStatus`  [INFERRED]
  user/app/http/dto/lifecycle_data.py → src/armaden/framework/enums/health_status.py
- `ServiceHealthData` --uses--> `HealthStatus`  [INFERRED]
  user/app/http/dto/lifecycle_data.py → src/armaden/framework/enums/health_status.py
- `ShutdownRequestData` --uses--> `HealthStatus`  [INFERRED]
  user/app/http/dto/lifecycle_data.py → src/armaden/framework/enums/health_status.py
- `LifecycleController` --uses--> `Controller`  [INFERRED]
  user/app/http/controllers/lifecycle_controller.py → src/armaden/framework/runtime/http/controller.py
- `Application` --uses--> `Application`  [INFERRED]
  user/bootstrap/application.py → src/armaden/framework/application.py

## Import Cycles
- None detected.

## Communities (289 total, 226 thin omitted)

### Community 0 - "IoC Container Binding"
Cohesion: 0.13
Nodes (7): ArmaReforgerServerExecutable, Bind the server to specific addresses / ports.          Keyword Args:, Configure BattlEye / RCON remote console.          Keyword Args:             add, Force loading a session save even if version mismatched., Skip the initial load request and start a brand-new session., Limit the number of streams opened for a client (1..1000)., Threads for short jobs (capped to CPU count or 16).

### Community 1 - "Supervisor Request Handling"
Cohesion: 0.33
Nodes (5): SupervisorRequestArgs, SupervisorRequestData, SupervisorRequestKind, RestartAppService, ShutdownAppService

### Community 3 - "Application Kernel Interface"
Cohesion: 0.07
Nodes (15): FastAPI, RestartPolicy, HttpServiceProvider, Result, DefaultApi, DefaultApiError, Any, Result (+7 more)

### Community 4 - "App Facade Container"
Cohesion: 0.11
Nodes (3): app(), Any, T

### Community 5 - "Executable Argument Builder"
Cohesion: 0.17
Nodes (10): ArmaReforgerServerConfig, ArmaReforgerServer, ArmaReforgerServerError, ArmaReforgerServerException, ExecutableContainer, PathContainer, Any, Result (+2 more)

### Community 6 - "Task Lifecycle Management"
Cohesion: 0.13
Nodes (13): BoundMethod, CircularDependencyException, EntryNotFoundException, LogicException, SelfBuilding, get_class_for_callable(), get_contextual_attribute_from_dependency(), get_parameter_class_name() (+5 more)

### Community 7 - "Async Datagram Transport"
Cohesion: 0.10
Nodes (10): DatagramProtocol, DatagramTransport, Exception, entry(), main(), entry(), main(), AsyncDatagramTransport (+2 more)

### Community 10 - "Core Application Bootstrap"
Cohesion: 0.11
Nodes (9): set_application(), bootstrap_console(), bootstrap_http(), ConsoleKernel, HttpKernel, Kernel, RuntimeEntry, ConsoleServiceProvider (+1 more)

### Community 11 - "BattleEye RCON Server"
Cohesion: 0.15
Nodes (7): BattleEyeRconServer, Client, ClientState, ResponseMessage, LoginStatus, LoginResponsePacket, IntEnum

### Community 12 - "Console Kernel Bootstrap"
Cohesion: 0.12
Nodes (7): InstanceContainer, AbstractEventLoop, Self, SupervisorRequestInterface, TaskInterface, Supervisor, SupervisorRequestData

### Community 13 - "Scaffold File Generator"
Cohesion: 0.14
Nodes (10): Generator, GeneratorResult, _detect_poetry_package_path(), _fmt_list(), main(), _print_result(), # TODO: Register bindings on the service container., # TODO: Build and register tasks with the supervisor. (+2 more)

### Community 16 - "Server Path Configuration"
Cohesion: 0.05
Nodes (21): Executable, Dictionary, ArmaReforgerRconClient, A2SConfig, Config, GameConfig, GamePropertiesConfig, GamePropertiesPersistence (+13 more)

### Community 19 - "Typed Environment Config"
Cohesion: 0.18
Nodes (7): GraphTaskRuntime, Semaphore, _result_error(), _run_shutdown(), _SharedWorker, WorkerPool, TaskInjector

### Community 21 - "Datagram Packet Parsing"
Cohesion: 0.16
Nodes (4): Config, Give, Tag, ContextualAttribute

### Community 24 - "Request"
Cohesion: 0.06
Nodes (20): HttpKernel, Middleware, MiddlewarePipeline, json_response(), JSONResponse, response(), ResponseFactory, ApiUser (+12 more)

### Community 25 - "lifecycle_controller.py"
Cohesion: 0.10
Nodes (19): AppServiceProvider, ServiceProvider, TaskBuilder, Lifecycle, Pipeline, Task, TaskRuntimeInterface, AppServiceProvider (+11 more)

### Community 26 - "Command Request Packet"
Cohesion: 0.17
Nodes (5): Error, ErrorKindInterface, Enforces that any error type object has a code string and message string., Accepts any Enum instance that implements a .message property., GenericError

### Community 27 - "Command Response Packet"
Cohesion: 0.19
Nodes (5): ABC, Configurable, _resolve_config_type(), Controller, ModuleLoaderError

### Community 28 - "Server Message Packet"
Cohesion: 0.20
Nodes (3): CommandHeader, CommandResponsePacket, BattleEyeInvalidPacketException

### Community 29 - "Config Value Management"
Cohesion: 0.15
Nodes (6): __getattr__(), _LegacyTask, TaskThreadingPolicy, StatusCallback, TaskCallback, TaskInterface

### Community 30 - "Player Response Parsing"
Cohesion: 0.11
Nodes (7): ServiceProvider, CoreApplication, AbstractEventLoop, Any, InstanceContainer, Result, SupervisorInterface

### Community 33 - "Type Discovery Provider"
Cohesion: 0.18
Nodes (3): # TODO: handle stateful messages (responses to sequenced messages), # TODO: implement event system, # TODO: handle stateful messages (responses to sequences)

### Community 34 - "App Lifecycle Callbacks"
Cohesion: 0.22
Nodes (4): ModuleLoader, TypeDiscoveryError, TypeDiscoveryServiceProvider, ModuleType

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
Cohesion: 0.29
Nodes (4): APIRouter, RouteCompiler, RouteParameter, HttpKernel

### Community 42 - "Auto Shutdown Flag"
Cohesion: 0.16
Nodes (8): TaskThreadingPolicy, ArmaReforgerExecutableFlag, ArmaReforgerExecutableFlagError, Arma Reforger CLI startup flags., RestartPolicy, ApplicationError, ApplicationStatus, StrEnum

### Community 44 - "Resource Database Regeneration"
Cohesion: 0.20
Nodes (3): RequestMessage, CommandRequestPacket, UnknownPacket

### Community 45 - "Debugger Port Setting"
Cohesion: 0.25
Nodes (3): Bind, Scoped, Singleton

### Community 48 - "Freeze Behaviour Mode"
Cohesion: 0.15
Nodes (6): Application, ApplicationBase, Application (ApplicationBase), Application, DefaultApplication, Application

### Community 49 - "Crash File Retention Flag"
Cohesion: 0.18
Nodes (7): PolicyEngine, Any, Any, Result, TaskThreadingPolicy, Task, TaskPolicy

### Community 52 - "Game Language Setting"
Cohesion: 0.08
Nodes (8): route(), URL, RequestContext, RouteNotFoundException, RouteParameterMissingException, UrlGenerator, auth(), request()

### Community 53 - "Server FPS Cap"
Cohesion: 0.33
Nodes (3): PlayerResponseData, Parse a single data row from ``players`` output.          Returns ``None``  if t, A connected player returned by the ``players`` command.

### Community 62 - ".custom"
Cohesion: 0.27
Nodes (3): Any, TaskGraph, TaskGraphCompiler

### Community 65 - ".disable_crash_reporter"
Cohesion: 0.13
Nodes (5): Any, Result, ScheduleBuilder, _ScheduledTask, ScheduleFacade

### Community 67 - ".enable_night_grain"
Cohesion: 0.19
Nodes (7): Parameter, Lifecycle, Pipeline, TaskRuntimeInterface, UnresolvedDependencyError, TaskInjector, _UnresolvedSentinel

### Community 68 - "Agent Guidelines Docs"
Cohesion: 0.11
Nodes (16): Event, ProgressChannel, _ExclusiveWorker, ProcessInfoData, RequestInfoData, SupervisorError, TaskRecord, ThreadInfoData (+8 more)

### Community 79 - "Package Init Module"
Cohesion: 0.33
Nodes (8): HealthStatus, GetAppStatus, HealthResponseData, RestartRequestData, RestartResponseData, ServiceHealthData, ShutdownRequestData, ShutdownResponseData

### Community 100 - ".single_threaded_update"
Cohesion: 0.14
Nodes (7): Future, Any, AsyncStreamCallback, Path, Result, TaskRuntime, TaskStateData

### Community 126 - "JSONResponse"
Cohesion: 0.29
Nodes (4): Any, AsyncStreamCallback, Path, Result

### Community 161 - "Any"
Cohesion: 0.22
Nodes (8): ArmaDen, Build Locally, CLI Entrypoints, Install, Manual Application Setup, Packages, Run with Docker, Scaffold an Application

### Community 175 - "Result"
Cohesion: 0.33
Nodes (5): MANDATORY: Code Comment Conventions, MANDATORY: Git Rules, MANDATORY: Local Code Search/Traversal, MANDATORY: Use td for Task Management, MANDATORY: Worktree Management

### Community 231 - "Executable"
Cohesion: 0.33
Nodes (3): DuplicateTaskNameError, TaskError, TaskGraphCycleError

### Community 249 - "DatagramTransportInterface"
Cohesion: 0.22
Nodes (3): RconPacketInterface, DatagramTransportInterface, Protocol

## Knowledge Gaps
- **26 isolated node(s):** `armaden`, `ApiResponseData`, `MANDATORY: Local Code Search/Traversal`, `MANDATORY: Use td for Task Management`, `MANDATORY: Worktree Management` (+21 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **226 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ArmaReforgerServerExecutable` connect `IoC Container Binding` to `.addons_verify`, `Result`, `.autoshutdown`, `.backend_local_storage`, `.cfg`, `.create_db`, `.custom`, `.debugger`, `.debugger_port`, `.disable_crash_reporter`, `.disable_shaders_build`, `Server Path Configuration`, `.jobsys_long_worker_count`, `.limit_fps`, `.log_rdb_checksum`, `.logs_dir`, `.minidump`, `.nds`, `.no_splash`, `.no_throw`, `.nwk_resolution`, `.profile`, `.scenario`, `.script_authorize_all`, `.server_id`, `Local Backend Storage Flag`, `Freeze Detection Timeout`, `List Scenarios Flag`, `Log Append Mode Flag`, `.autoshutdown`, `Error Dialog Suppression`, `.backend_disable_storage`, `.backend_local_storage`, `.debugger_port`, `.disable_ai`, `Global Streaming Budget`, `Package Init Module`, `Package Init Module`, `Package Entry Point`, `Package Init Module`, `Package Init Module`, `Package Init Module`, `Package Init Module`, `Package Init Module`, `.freeze_check`, `.jobsys_long_worker_count`, `.keep_crash_files`, `.keep_session_save`, `.log_voting`, `.nds`, `.no_backend`, `.nwk_resolution`, `.server_id`, `.staggering_budget`, `.disable_navmesh_streaming`, `.streams_delta`, `.freeze_check_mode`, `Any`, `Config`, `.list_scenarios`, `Self`, `.log_scr_checksum`, `TaskRuntimeInterface`, `__init__.py`, `.no_backend`, `.no_sound`, `Result`, `.rpl_encode_as_long_jobs`, `.server_world`, `.addon_temp_dir`?**
  _High betweenness centrality (0.176) - this node is a cross-community bridge._
- **Why does `Executable` connect `Server Path Configuration` to `IoC Container Binding`, `Command Response Packet`?**
  _High betweenness centrality (0.149) - this node is a cross-community bridge._
- **Why does `Task` connect `Crash File Retention Flag` to `.disable_crash_reporter`, `Application Kernel Interface`, `.enable_night_grain`, `App Config Module`, `Typed Environment Config`, `Command Response Packet`, `Config Value Management`, `.custom`?**
  _High betweenness centrality (0.117) - this node is a cross-community bridge._
- **Are the 11 inferred relationships involving `InstanceContainer` (e.g. with `Application` and `Config`) actually correct?**
  _`InstanceContainer` has 11 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `ArmaReforgerServerExecutable` (e.g. with `Executable` and `Dictionary`) actually correct?**
  _`ArmaReforgerServerExecutable` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 13 inferred relationships involving `Supervisor` (e.g. with `ApplicationError` and `ApplicationException`) actually correct?**
  _`Supervisor` has 13 INFERRED edges - model-reasoned connections that need verification._
- **Are the 21 inferred relationships involving `TaskGraph` (e.g. with `SupervisorInterface` and `ConcurrencyBuilder`) actually correct?**
  _`TaskGraph` has 21 INFERRED edges - model-reasoned connections that need verification._