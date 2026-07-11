# Graph Report - feature-supervisor-task-refactor-worktree  (2026-07-11)

## Corpus Check
- 167 files · ~30,194 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1636 nodes · 2885 edges · 289 communities (62 shown, 227 thin omitted)
- Extraction: 82% EXTRACTED · 18% INFERRED · 0% AMBIGUOUS · INFERRED: 529 edges (avg confidence: 0.55)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `4fe2b11f`
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
- Middleware
- app() facade
- .no_backend
- .no_sound
- CoreApplicationInterface
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
2. `ArmaReforgerServerExecutable` - 91 edges
3. `Supervisor` - 50 edges
4. `Request` - 49 edges
5. `TaskGraph` - 42 edges
6. `app()` - 38 edges
7. `BattleEyeRconClient` - 36 edges
8. `CoreApplication` - 35 edges
9. `TaskInjector` - 34 edges
10. `TaskGraphCompiler` - 31 edges

## Surprising Connections (you probably didn't know these)
- `Application` --uses--> `Application`  [INFERRED]
  user/bootstrap/application.py → src/armaden/framework/application.py
- `RestartRequestData` --uses--> `HealthStatus`  [INFERRED]
  user/app/http/dto/lifecycle_data.py → src/armaden/framework/enums/health_status.py
- `ServiceHealthData` --uses--> `HealthStatus`  [INFERRED]
  user/app/http/dto/lifecycle_data.py → src/armaden/framework/enums/health_status.py
- `ShutdownRequestData` --uses--> `HealthStatus`  [INFERRED]
  user/app/http/dto/lifecycle_data.py → src/armaden/framework/enums/health_status.py
- `LifecycleController` --uses--> `Controller`  [INFERRED]
  user/app/http/controllers/lifecycle_controller.py → src/armaden/framework/runtime/http/controller.py

## Import Cycles
- None detected.

## Communities (289 total, 227 thin omitted)

### Community 0 - "IoC Container Binding"
Cohesion: 0.13
Nodes (7): ArmaReforgerServerExecutable, Bind the server to specific addresses / ports.          Keyword Args:, Configure BattlEye / RCON remote console.          Keyword Args:             add, Force loading a session save even if version mismatched., Skip the initial load request and start a brand-new session., Limit the number of streams opened for a client (1..1000)., Threads for short jobs (capped to CPU count or 16).

### Community 1 - "Supervisor Request Handling"
Cohesion: 0.22
Nodes (5): SupervisorRequestArgs, SupervisorRequestData, SupervisorRequestKind, RestartAppService, ShutdownAppService

### Community 3 - "Application Kernel Interface"
Cohesion: 0.06
Nodes (12): RestartPolicy, Self, TaskBuilderInterface, TaskInterface, _BuiltCallbacks, _BuiltTask, Any, Result (+4 more)

### Community 4 - "App Facade Container"
Cohesion: 0.10
Nodes (4): app(), config(), get_application(), T

### Community 6 - "Task Lifecycle Management"
Cohesion: 0.13
Nodes (13): BoundMethod, CircularDependencyException, EntryNotFoundException, LogicException, SelfBuilding, get_class_for_callable(), get_contextual_attribute_from_dependency(), get_parameter_class_name() (+5 more)

### Community 7 - "Async Datagram Transport"
Cohesion: 0.10
Nodes (10): DatagramProtocol, DatagramTransport, Exception, entry(), main(), entry(), main(), AsyncDatagramTransport (+2 more)

### Community 8 - "Bound Method Resolution"
Cohesion: 0.15
Nodes (19): TaskError, ConcurrencyFacade, ProcessFacade, ScheduleFacade, PolicyEngine, ProgressChannel, ProgressUpdate, _ExclusiveWorker (+11 more)

### Community 10 - "Core Application Bootstrap"
Cohesion: 0.06
Nodes (15): ABC, DeferrableProvider, ServiceProvider, set_application(), ApplicationInterface, Controller, bootstrap_console(), bootstrap_http() (+7 more)

### Community 11 - "BattleEye RCON Server"
Cohesion: 0.15
Nodes (7): BattleEyeRconServer, Client, ClientState, ResponseMessage, LoginStatus, LoginResponsePacket, IntEnum

### Community 12 - "Console Kernel Bootstrap"
Cohesion: 0.09
Nodes (10): Future, AbstractEventLoop, Any, InstanceContainer, Result, Self, _result_error(), Supervisor (+2 more)

### Community 13 - "Scaffold File Generator"
Cohesion: 0.14
Nodes (10): Generator, GeneratorResult, _detect_poetry_package_path(), _fmt_list(), main(), _print_result(), # TODO: Register bindings on the service container., # TODO: Build and register tasks with the supervisor. (+2 more)

### Community 19 - "Typed Environment Config"
Cohesion: 0.33
Nodes (10): A2SConfig, GameConfig, GamePropertiesConfig, GamePropertiesPersistence, JoinQueueConfig, OperatingConfig, RconConfig, ServerConfig (+2 more)

### Community 21 - "Datagram Packet Parsing"
Cohesion: 0.16
Nodes (4): Config, Give, Tag, ContextualAttribute

### Community 24 - "Request"
Cohesion: 0.24
Nodes (6): AuthManager, Authenticate, AuthenticateWithBasic, AuthenticateWithHeader, AuthenticateWithToken, HttpServiceProvider

### Community 25 - "lifecycle_controller.py"
Cohesion: 0.19
Nodes (12): Lifecycle, Pipeline, Task, TaskRuntimeInterface, _emit_banner(), Result, TelemetryServiceProvider, CollectServerTelemetryTask (+4 more)

### Community 26 - "Command Request Packet"
Cohesion: 0.17
Nodes (5): Error, ErrorKindInterface, Enforces that any error type object has a code string and message string., Accepts any Enum instance that implements a .message property., GenericError

### Community 27 - "Command Response Packet"
Cohesion: 0.29
Nodes (9): Configurable, _resolve_config_type(), Dictionary, ArmaReforgerRconClient, ArmaReforgerServerError, ArmaReforgerServerException, Config, ExecutableContainer (+1 more)

### Community 28 - "Server Message Packet"
Cohesion: 0.20
Nodes (3): CommandHeader, CommandResponsePacket, BattleEyeInvalidPacketException

### Community 30 - "Player Response Parsing"
Cohesion: 0.11
Nodes (7): ServiceProvider, CoreApplication, AbstractEventLoop, Any, InstanceContainer, Result, SupervisorInterface

### Community 33 - "Type Discovery Provider"
Cohesion: 0.18
Nodes (3): # TODO: handle stateful messages (responses to sequenced messages), # TODO: implement event system, # TODO: handle stateful messages (responses to sequences)

### Community 34 - "App Lifecycle Callbacks"
Cohesion: 0.25
Nodes (3): ModuleLoader, TypeDiscoveryServiceProvider, ModuleType

### Community 35 - "Async Subprocess Dispatch"
Cohesion: 0.14
Nodes (5): config(), env(), Facade for reading typed environment variables from the application., config(), config()

### Community 37 - "App Config Module"
Cohesion: 0.10
Nodes (8): Any, AsyncStreamCallback, Path, Result, ProcessBuilder, _ProcessTask, SubprocessHandle, TaskGraph

### Community 40 - "Addon Auto Repair Flag"
Cohesion: 0.25
Nodes (4): APIRouter, RouteCompiler, RouteParameter, HttpKernel

### Community 42 - "Auto Shutdown Flag"
Cohesion: 0.14
Nodes (9): DefaultApiError, ArmaReforgerExecutableFlag, ArmaReforgerExecutableFlagError, Arma Reforger CLI startup flags., SteamCMD CLI command flags (prefixed with ``+``)., SteamCmdExecutableFlag, ApplicationError, ApplicationStatus (+1 more)

### Community 44 - "Resource Database Regeneration"
Cohesion: 0.20
Nodes (3): RequestMessage, CommandRequestPacket, UnknownPacket

### Community 45 - "Debugger Port Setting"
Cohesion: 0.25
Nodes (3): Bind, Scoped, Singleton

### Community 48 - "Freeze Behaviour Mode"
Cohesion: 0.20
Nodes (5): Application, ApplicationBase, Application (ApplicationBase), DefaultApplication, Application

### Community 49 - "Crash File Retention Flag"
Cohesion: 0.14
Nodes (8): Parameter, Any, TaskInjector, Any, Result, Task, TaskPolicy, TaskThreadingPolicy

### Community 50 - "Log File Retention Limit"
Cohesion: 0.16
Nodes (8): AppServiceProvider, ServiceProvider, TaskBuilder, TypeDiscoveryError, AppServiceProvider, Result, providers(), ServiceProvider

### Community 52 - "Game Language Setting"
Cohesion: 0.08
Nodes (8): route(), URL, RequestContext, RouteNotFoundException, RouteParameterMissingException, UrlGenerator, auth(), request()

### Community 53 - "Server FPS Cap"
Cohesion: 0.33
Nodes (3): PlayerResponseData, Parse a single data row from ``players`` output.          Returns ``None``  if t, A connected player returned by the ``players`` command.

### Community 62 - ".custom"
Cohesion: 0.20
Nodes (6): DuplicateTaskNameError, TaskGraphCycleError, UnresolvedDependencyError, Any, TaskGraph, TaskGraphCompiler

### Community 65 - ".disable_crash_reporter"
Cohesion: 0.14
Nodes (4): Any, Result, ScheduleBuilder, _ScheduledTask

### Community 67 - ".enable_night_grain"
Cohesion: 0.18
Nodes (8): Lifecycle, Pipeline, Any, AsyncStreamCallback, Path, Result, TaskRuntimeInterface, _UnresolvedSentinel

### Community 68 - "Agent Guidelines Docs"
Cohesion: 0.17
Nodes (6): Event, Any, AsyncStreamCallback, Path, Result, TaskRuntime

### Community 79 - "Package Init Module"
Cohesion: 0.29
Nodes (8): HealthStatus, GetAppStatus, HealthResponseData, RestartRequestData, RestartResponseData, ServiceHealthData, ShutdownRequestData, ShutdownResponseData

### Community 103 - ".vm_error_mode"
Cohesion: 0.22
Nodes (3): ApiUser, ConfigUserProvider, TokenGuard

### Community 161 - "Any"
Cohesion: 0.22
Nodes (8): ArmaDen, Build Locally, CLI Entrypoints, Install, Manual Application Setup, Packages, Run with Docker, Scaffold an Application

### Community 175 - "Result"
Cohesion: 0.33
Nodes (5): MANDATORY: Code Comment Conventions, MANDATORY: Git Rules, MANDATORY: Local Code Search/Traversal, MANDATORY: Use td for Task Management, MANDATORY: Worktree Management

### Community 233 - "Kernel"
Cohesion: 0.31
Nodes (5): json_response(), JSONResponse, response(), ResponseFactory, StarletteJSONResponse

### Community 246 - "ArmaReforgerExecutableError"
Cohesion: 0.47
Nodes (3): ArmaReforgerExecutableError, Config, Arma Reforger dedicated server wrapper.  Provides a typed, fluent interface for

### Community 248 - "SteamCmdExecutableError"
Cohesion: 0.47
Nodes (3): SteamCmd — Python wrapper for the steamcmd CLI tool., Config, SteamCmdExecutableError

### Community 250 - "__init__.py"
Cohesion: 0.25
Nodes (3): SupervisorRequestInterface, RconPacketInterface, Protocol

## Knowledge Gaps
- **25 isolated node(s):** `armaden`, `ApiResponseData`, `MANDATORY: Local Code Search/Traversal`, `MANDATORY: Use td for Task Management`, `MANDATORY: Worktree Management` (+20 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **227 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ArmaReforgerServerExecutable` connect `IoC Container Binding` to `.addons_verify`, `Result`, `.autoshutdown`, `.backend_local_storage`, `.cfg`, `.create_db`, `.custom`, `.debugger`, `.debugger_port`, `.disable_crash_reporter`, `.disable_shaders_build`, `Server Path Configuration`, `.jobsys_long_worker_count`, `.limit_fps`, `.log_rdb_checksum`, `.logs_dir`, `.minidump`, `.nds`, `.no_splash`, `.no_throw`, `.nwk_resolution`, `.profile`, `Command Response Packet`, `.scenario`, `.script_authorize_all`, `.server_id`, `Steam Query Bind Address`, `Local Backend Storage Flag`, `Freeze Detection Timeout`, `List Scenarios Flag`, `Log Append Mode Flag`, `.autoshutdown`, `Error Dialog Suppression`, `.backend_disable_storage`, `.backend_local_storage`, `.debugger_port`, `.disable_ai`, `Global Streaming Budget`, `Package Init Module`, `Package Init Module`, `Package Entry Point`, `Package Init Module`, `Package Init Module`, `Package Init Module`, `Package Init Module`, `Package Init Module`, `.freeze_check`, `.jobsys_long_worker_count`, `.keep_crash_files`, `.keep_session_save`, `.log_voting`, `.nds`, `.no_backend`, `.nwk_resolution`, `.server_id`, `.staggering_budget`, `.disable_navmesh_streaming`, `Executable`, `.freeze_check_mode`, `.streams_delta`, `Any`, `.list_scenarios`, `Config`, `.log_scr_checksum`, `Self`, `TaskRuntimeInterface`, `.no_backend`, `.no_sound`, `__init__.py`, `config.py`, `.rpl_encode_as_long_jobs`, `Result`, `ArmaReforgerExecutableError`, `.server_world`, `.addon_temp_dir`?**
  _High betweenness centrality (0.189) - this node is a cross-community bridge._
- **Why does `InstanceContainer` connect `Arma Reforger Server Config` to `Task Lifecycle Management`, `Server Auto Restart Flag`, `Core Application Bootstrap`, `Debugger Port Setting`, `Framework Service Providers`, `Datagram Packet Parsing`, `FastAPI Default Application`, `Module Discovery Loader`, `Config Value Management`?**
  _High betweenness centrality (0.120) - this node is a cross-community bridge._
- **Why does `ServiceProvider` connect `Core Application Bootstrap` to `Arma Reforger Server Config`, `App Lifecycle Callbacks`, `Package Init Module`, `Log File Retention Limit`, `Request`?**
  _High betweenness centrality (0.081) - this node is a cross-community bridge._
- **Are the 11 inferred relationships involving `InstanceContainer` (e.g. with `Application` and `Config`) actually correct?**
  _`InstanceContainer` has 11 INFERRED edges - model-reasoned connections that need verification._
- **Are the 9 inferred relationships involving `ArmaReforgerServerExecutable` (e.g. with `ArmaReforgerServer` and `ArmaReforgerServerError`) actually correct?**
  _`ArmaReforgerServerExecutable` has 9 INFERRED edges - model-reasoned connections that need verification._
- **Are the 17 inferred relationships involving `Supervisor` (e.g. with `ApplicationError` and `ApplicationException`) actually correct?**
  _`Supervisor` has 17 INFERRED edges - model-reasoned connections that need verification._
- **Are the 22 inferred relationships involving `TaskGraph` (e.g. with `ConcurrencyBuilder` and `ScheduleBuilder`) actually correct?**
  _`TaskGraph` has 22 INFERRED edges - model-reasoned connections that need verification._