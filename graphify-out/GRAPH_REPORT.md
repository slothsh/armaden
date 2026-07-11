# Graph Report - feature-supervisor-task-refactor-worktree  (2026-07-11)

## Corpus Check
- 164 files · ~29,763 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1608 nodes · 2863 edges · 250 communities (57 shown, 193 thin omitted)
- Extraction: 81% EXTRACTED · 19% INFERRED · 0% AMBIGUOUS · INFERRED: 539 edges (avg confidence: 0.55)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `ecbf6896`
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
- .freeze_check_mode
- .list_scenarios
- .log_scr_checksum
- .no_backend
- .no_sound
- .rpl_encode_as_long_jobs
- .server_world
- __init__.py
- __init__.py
- DatagramTransportInterface
- Executable
- ApplicationInterface
- route_compiler.py
- ApplicationInterface
- RequestContext
- Result
- ServiceProvider
- Result
- Result

## God Nodes (most connected - your core abstractions)
1. `InstanceContainer` - 109 edges
2. `ArmaReforgerServerExecutable` - 91 edges
3. `Supervisor` - 54 edges
4. `Request` - 49 edges
5. `TaskGraph` - 46 edges
6. `app()` - 38 edges
7. `BattleEyeRconClient` - 36 edges
8. `CoreApplication` - 35 edges
9. `TaskInjector` - 34 edges
10. `TaskGraphCompiler` - 31 edges

## Surprising Connections (you probably didn't know these)
- `Application` --uses--> `Application`  [INFERRED]
  user/bootstrap/application.py → src/armaden/framework/application.py
- `AppServiceProvider` --uses--> `ServiceProvider`  [INFERRED]
  user/app/providers/app_service_provider.py → src/armaden/framework/classes/service_provider.py
- `AppServiceProvider` --uses--> `TaskBuilder`  [INFERRED]
  user/app/providers/app_service_provider.py → src/armaden/framework/classes/task.py
- `GetAppStatus` --uses--> `HealthStatus`  [INFERRED]
  user/app/http/actions/get_app_status.py → src/armaden/framework/enums/health_status.py
- `RestartRequestData` --uses--> `HealthStatus`  [INFERRED]
  user/app/http/dto/lifecycle_data.py → src/armaden/framework/enums/health_status.py

## Import Cycles
- None detected.

## Communities (250 total, 193 thin omitted)

### Community 0 - "IoC Container Binding"
Cohesion: 0.03
Nodes (31): ArmaReforgerServerExecutable, Directory for profiles (saves, logs, settings).          The directory is create, Redirect log output to the given directory., Bind the server to specific addresses / ports.          Keyword Args:, Configure BattlEye / RCON remote console.          Keyword Args:             add, Cap the server frame rate., ID of the scenario to host., Auto-restart the server when it crashes (default: ``True``). (+23 more)

### Community 1 - "Supervisor Request Handling"
Cohesion: 0.31
Nodes (5): SupervisorRequestArgs, SupervisorRequestData, SupervisorRequestKind, RestartAppService, ShutdownAppService

### Community 3 - "Application Kernel Interface"
Cohesion: 0.06
Nodes (12): RestartPolicy, Self, TaskBuilderInterface, TaskInterface, _BuiltCallbacks, _BuiltTask, Any, Result (+4 more)

### Community 4 - "App Facade Container"
Cohesion: 0.08
Nodes (4): app(), config(), get_application(), T

### Community 5 - "Executable Argument Builder"
Cohesion: 0.06
Nodes (4): Executable, Task, TaskBuilder, TaskThreadingPolicy

### Community 6 - "Task Lifecycle Management"
Cohesion: 0.11
Nodes (13): ABC, BoundMethod, CircularDependencyException, EntryNotFoundException, LogicException, SelfBuilding, get_class_for_callable(), get_contextual_attribute_from_dependency() (+5 more)

### Community 7 - "Async Datagram Transport"
Cohesion: 0.10
Nodes (10): DatagramProtocol, DatagramTransport, Exception, entry(), main(), entry(), main(), AsyncDatagramTransport (+2 more)

### Community 8 - "Bound Method Resolution"
Cohesion: 0.15
Nodes (19): TaskError, ConcurrencyFacade, ProcessFacade, ScheduleFacade, PolicyEngine, ProgressChannel, ProgressUpdate, _ExclusiveWorker (+11 more)

### Community 10 - "Core Application Bootstrap"
Cohesion: 0.15
Nodes (8): set_application(), bootstrap_console(), bootstrap_http(), ConsoleKernel, HttpKernel, Kernel, RuntimeEntry, TypedResult

### Community 11 - "BattleEye RCON Server"
Cohesion: 0.15
Nodes (7): BattleEyeRconServer, Client, ClientState, ResponseMessage, LoginStatus, LoginResponsePacket, IntEnum

### Community 12 - "Console Kernel Bootstrap"
Cohesion: 0.09
Nodes (10): Future, AbstractEventLoop, Any, InstanceContainer, Result, Self, _result_error(), Supervisor (+2 more)

### Community 13 - "Scaffold File Generator"
Cohesion: 0.14
Nodes (10): Generator, GeneratorResult, _detect_poetry_package_path(), _fmt_list(), main(), _print_result(), # TODO: Register bindings on the service container., # TODO: Build and register tasks with the supervisor. (+2 more)

### Community 16 - "Server Path Configuration"
Cohesion: 0.13
Nodes (4): SteamCmd — Python wrapper for the steamcmd CLI tool., Config, SteamCmdExecutable, SteamCmdExecutableError

### Community 19 - "Typed Environment Config"
Cohesion: 0.33
Nodes (10): A2SConfig, GameConfig, GamePropertiesConfig, GamePropertiesPersistence, JoinQueueConfig, OperatingConfig, RconConfig, ServerConfig (+2 more)

### Community 21 - "Datagram Packet Parsing"
Cohesion: 0.16
Nodes (4): Config, Give, Tag, ContextualAttribute

### Community 24 - "Request"
Cohesion: 0.06
Nodes (21): HttpKernel, Middleware, MiddlewarePipeline, json_response(), JSONResponse, response(), ResponseFactory, ApiUser (+13 more)

### Community 25 - "lifecycle_controller.py"
Cohesion: 0.27
Nodes (7): HealthStatus, HealthResponseData, RestartRequestData, RestartResponseData, ServiceHealthData, ShutdownRequestData, ShutdownResponseData

### Community 26 - "Command Request Packet"
Cohesion: 0.17
Nodes (5): Error, ErrorKindInterface, Enforces that any error type object has a code string and message string., Accepts any Enum instance that implements a .message property., GenericError

### Community 27 - "Command Response Packet"
Cohesion: 0.12
Nodes (13): Configurable, _resolve_config_type(), Dictionary, ArmaReforgerRconClient, ArmaReforgerServer, ArmaReforgerServerError, ArmaReforgerServerException, Config (+5 more)

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
Cohesion: 0.29
Nodes (3): ModuleLoader, ModuleLoaderError, ModuleType

### Community 35 - "Async Subprocess Dispatch"
Cohesion: 0.14
Nodes (5): config(), env(), Facade for reading typed environment variables from the application., config(), config()

### Community 37 - "App Config Module"
Cohesion: 0.10
Nodes (7): ProcessBuilder, _ProcessTask, Any, AsyncStreamCallback, Path, Result, SubprocessHandle

### Community 40 - "Addon Auto Repair Flag"
Cohesion: 0.15
Nodes (5): APIRouter, Controller, RouteCompiler, RouteParameter, HttpKernel

### Community 42 - "Auto Shutdown Flag"
Cohesion: 0.16
Nodes (8): ArmaReforgerExecutableFlag, ArmaReforgerExecutableFlagError, Arma Reforger CLI startup flags., SteamCMD CLI command flags (prefixed with ``+``)., SteamCmdExecutableFlag, ApplicationError, ApplicationStatus, StrEnum

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
Cohesion: 0.18
Nodes (5): AppServiceProvider, ServiceProvider, TaskBuilder, AppServiceProvider, providers()

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
Cohesion: 0.23
Nodes (3): app() facade, GetAppStatus, Controllers for API routes

### Community 161 - "Any"
Cohesion: 0.22
Nodes (8): ArmaDen, Build Locally, CLI Entrypoints, Install, Manual Application Setup, Packages, Run with Docker, Scaffold an Application

### Community 175 - "Result"
Cohesion: 0.33
Nodes (5): MANDATORY: Code Comment Conventions, MANDATORY: Git Rules, MANDATORY: Local Code Search/Traversal, MANDATORY: Use td for Task Management, MANDATORY: Worktree Management

### Community 250 - "__init__.py"
Cohesion: 0.25
Nodes (3): SupervisorRequestInterface, RconPacketInterface, Protocol

## Knowledge Gaps
- **25 isolated node(s):** `armaden`, `ApiResponseData`, `MANDATORY: Local Code Search/Traversal`, `MANDATORY: Use td for Task Management`, `MANDATORY: Worktree Management` (+20 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **193 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ArmaReforgerServerExecutable` connect `IoC Container Binding` to `App Facade Container`, `Executable Argument Builder`, `Server Path Configuration`, `Command Response Packet`, `Local Backend Storage Flag`, `Freeze Detection Timeout`, `List Scenarios Flag`, `Log Append Mode Flag`, `.autoshutdown`, `Error Dialog Suppression`, `.backend_disable_storage`, `.backend_local_storage`, `.debugger_port`, `.disable_ai`, `Global Streaming Budget`, `Package Init Module`, `Package Init Module`, `Package Entry Point`, `Package Init Module`, `Package Init Module`, `Package Init Module`, `Package Init Module`, `Package Init Module`, `.freeze_check`, `.jobsys_long_worker_count`, `.keep_crash_files`, `.keep_session_save`, `.log_voting`, `.nds`, `.no_backend`, `.nwk_resolution`, `.server_id`, `.staggering_budget`, `.disable_navmesh_streaming`, `.vm_error_mode`, `.freeze_check_mode`, `.streams_delta`, `Any`, `.list_scenarios`, `Config`, `.log_scr_checksum`, `Self`, `TaskRuntimeInterface`, `.no_backend`, `.no_sound`, `__init__.py`, `Result`, `.rpl_encode_as_long_jobs`, `.server_world`?**
  _High betweenness centrality (0.167) - this node is a cross-community bridge._
- **Why does `InstanceContainer` connect `Arma Reforger Server Config` to `Result`, `Task Lifecycle Management`, `Server Auto Restart Flag`, `Debugger Port Setting`, `Framework Service Providers`, `Datagram Packet Parsing`, `FastAPI Default Application`, `Module Discovery Loader`, `Config Value Management`?**
  _High betweenness centrality (0.132) - this node is a cross-community bridge._
- **Why does `Supervisor` connect `Console Kernel Bootstrap` to `.disable_crash_reporter`, `App Config Module`, `Async Datagram Transport`, `Bound Method Resolution`, `Auto Shutdown Flag`, `Package Init Module`, `Crash File Retention Flag`, `.custom`, `Player Response Parsing`?**
  _High betweenness centrality (0.105) - this node is a cross-community bridge._
- **Are the 11 inferred relationships involving `InstanceContainer` (e.g. with `Application` and `Config`) actually correct?**
  _`InstanceContainer` has 11 INFERRED edges - model-reasoned connections that need verification._
- **Are the 9 inferred relationships involving `ArmaReforgerServerExecutable` (e.g. with `ArmaReforgerServer` and `ArmaReforgerServerError`) actually correct?**
  _`ArmaReforgerServerExecutable` has 9 INFERRED edges - model-reasoned connections that need verification._
- **Are the 21 inferred relationships involving `Supervisor` (e.g. with `ApplicationError` and `ApplicationException`) actually correct?**
  _`Supervisor` has 21 INFERRED edges - model-reasoned connections that need verification._
- **Are the 25 inferred relationships involving `TaskGraph` (e.g. with `ConcurrencyBuilder` and `ProcessBuilder`) actually correct?**
  _`TaskGraph` has 25 INFERRED edges - model-reasoned connections that need verification._