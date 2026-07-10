# Graph Report - feature-auth-plumbing-worktree  (2026-07-10)

## Corpus Check
- 147 files · ~24,626 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1369 nodes · 2345 edges · 249 communities (51 shown, 198 thin omitted)
- Extraction: 84% EXTRACTED · 16% INFERRED · 0% AMBIGUOUS · INFERRED: 378 edges (avg confidence: 0.55)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `40ee5cb2`
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
- .disable_shaders_build
- .freeze_check_mode
- .jobsys_long_worker_count
- .limit_fps
- .list_scenarios
- .log_rdb_checksum
- .log_scr_checksum
- .logs_dir
- .nds
- .no_backend
- .no_sound
- .no_splash
- .nwk_resolution
- .rpl_encode_as_long_jobs
- .script_authorize_all
- .server_id
- .server_world

## God Nodes (most connected - your core abstractions)
1. `InstanceContainer` - 114 edges
2. `ArmaReforgerServerExecutable` - 92 edges
3. `Request` - 59 edges
4. `CoreApplication` - 46 edges
5. `app()` - 38 edges
6. `BattleEyeRconClient` - 36 edges
7. `BattleEyeRconServer` - 29 edges
8. `ServiceProvider` - 26 edges
9. `Supervisor` - 26 edges
10. `SupervisorInterface` - 24 edges

## Surprising Connections (you probably didn't know these)
- `Application` --uses--> `Application`  [INFERRED]
  user/bootstrap/application.py → src/armaden/framework/application.py
- `AppServiceProvider` --uses--> `ServiceProvider`  [INFERRED]
  user/app/providers/app_service_provider.py → src/armaden/framework/classes/service_provider.py
- `RestartRequestData` --uses--> `HealthStatus`  [INFERRED]
  user/app/http/dto/lifecycle_data.py → src/armaden/framework/enums/health_status.py
- `ServiceHealthData` --uses--> `HealthStatus`  [INFERRED]
  user/app/http/dto/lifecycle_data.py → src/armaden/framework/enums/health_status.py
- `ShutdownRequestData` --uses--> `HealthStatus`  [INFERRED]
  user/app/http/dto/lifecycle_data.py → src/armaden/framework/enums/health_status.py

## Import Cycles
- None detected.

## Communities (249 total, 198 thin omitted)

### Community 0 - "IoC Container Binding"
Cohesion: 0.13
Nodes (7): ArmaReforgerServerExecutable, Bind the server to specific addresses / ports.          Keyword Args:, Configure BattlEye / RCON remote console.          Keyword Args:             add, Force loading a session save even if version mismatched., Skip the initial load request and start a brand-new session., Limit the number of streams opened for a client (1..1000)., Threads for short jobs (capped to CPU count or 16).

### Community 1 - "Supervisor Request Handling"
Cohesion: 0.08
Nodes (16): Future, SupervisorRequestArgs, SupervisorRequestData, SupervisorRequestKind, SupervisorRequestInterface, TaskInterface, ProcessInfoData, RequestInfoData (+8 more)

### Community 3 - "Application Kernel Interface"
Cohesion: 0.22
Nodes (8): TaskRuntimeInterface, Dictionary, ArmaReforgerRconClient, ArmaReforgerServerError, ArmaReforgerServerException, Config, ExecutableContainer, PathContainer

### Community 4 - "App Facade Container"
Cohesion: 0.09
Nodes (4): app(), config(), get_application(), T

### Community 5 - "Executable Argument Builder"
Cohesion: 0.08
Nodes (4): Task, TaskBuilder, TaskThreadingPolicy, AppServiceProvider

### Community 6 - "Task Lifecycle Management"
Cohesion: 0.11
Nodes (12): BoundMethod, CircularDependencyException, EntryNotFoundException, LogicException, SelfBuilding, get_class_for_callable(), get_parameter_class_name(), is_parameter_required() (+4 more)

### Community 7 - "Async Datagram Transport"
Cohesion: 0.08
Nodes (10): DatagramProtocol, DatagramTransport, Exception, entry(), main(), entry(), main(), AsyncDatagramTransport (+2 more)

### Community 10 - "Core Application Bootstrap"
Cohesion: 0.14
Nodes (8): set_application(), bootstrap_console(), bootstrap_http(), ConsoleKernel, HttpKernel, Kernel, RuntimeEntry, TypedResult

### Community 11 - "BattleEye RCON Server"
Cohesion: 0.14
Nodes (7): BattleEyeRconServer, Client, ClientState, ResponseMessage, LoginStatus, LoginResponsePacket, IntEnum

### Community 12 - "Console Kernel Bootstrap"
Cohesion: 0.15
Nodes (3): ABC, DeferrableProvider, ServiceProvider

### Community 13 - "Scaffold File Generator"
Cohesion: 0.14
Nodes (10): Generator, GeneratorResult, _detect_poetry_package_path(), _fmt_list(), main(), _print_result(), # TODO: Register bindings on the service container., # TODO: Build and register tasks with the supervisor. (+2 more)

### Community 14 - "BattleEye RCON Client"
Cohesion: 0.13
Nodes (6): BattleEyeRconClient, ClientStatus, Message, # TODO: handle stateful messages (responses to sequenced messages), # TODO: implement event system, # TODO: handle stateful messages (responses to sequences)

### Community 15 - "Arma Server Task Runtime"
Cohesion: 0.06
Nodes (7): ErrorInterface, CoreApplicationInterface, KernelInterface, TaskBuilderInterface, RconPacketInterface, DatagramTransportInterface, Protocol

### Community 16 - "Server Path Configuration"
Cohesion: 0.13
Nodes (4): SteamCmd — Python wrapper for the steamcmd CLI tool., Config, SteamCmdExecutable, SteamCmdExecutableError

### Community 19 - "Typed Environment Config"
Cohesion: 0.33
Nodes (10): A2SConfig, GameConfig, GamePropertiesConfig, GamePropertiesPersistence, JoinQueueConfig, OperatingConfig, RconConfig, ServerConfig (+2 more)

### Community 20 - "Login Packet Processing"
Cohesion: 0.07
Nodes (5): NextCallable, Any, Any, Request, StarletteRequest

### Community 21 - "Datagram Packet Parsing"
Cohesion: 0.15
Nodes (5): Config, Give, register_builtin_attributes(), Tag, ContextualAttribute

### Community 24 - "Request"
Cohesion: 0.08
Nodes (9): APIRouter, Controller, HttpKernel, Middleware, MiddlewarePipeline, RequestContext, RouteCompiler, RouteParameter (+1 more)

### Community 25 - "lifecycle_controller.py"
Cohesion: 0.10
Nodes (19): ApplicationInterface, Middleware, Result, ServiceProvider, ApiUser, AuthManager, Any, Authenticate (+11 more)

### Community 26 - "Command Request Packet"
Cohesion: 0.17
Nodes (6): Error, ErrorKindInterface, Enforces that any error type object has a code string and message string., Accepts any Enum instance that implements a .message property., GenericError, ModuleLoaderError

### Community 28 - "Server Message Packet"
Cohesion: 0.12
Nodes (4): CommandHeader, CommandResponsePacket, KeepAlivePacket, BattleEyeInvalidPacketException

### Community 29 - "Config Value Management"
Cohesion: 0.18
Nodes (3): Application, SupervisorInterface, TypeDiscoveryError

### Community 34 - "App Lifecycle Callbacks"
Cohesion: 0.24
Nodes (3): ModuleLoader, TypeDiscoveryServiceProvider, ModuleType

### Community 35 - "Async Subprocess Dispatch"
Cohesion: 0.17
Nodes (4): config(), env(), Facade for reading typed environment variables from the application., config()

### Community 36 - "Frontend Dependencies"
Cohesion: 0.11
Nodes (5): route(), URL, RouteNotFoundException, RouteParameterMissingException, UrlGenerator

### Community 41 - "Server Auto Restart Flag"
Cohesion: 0.39
Nodes (3): ArmaReforgerExecutableError, Config, Arma Reforger dedicated server wrapper.  Provides a typed, fluent interface for

### Community 42 - "Auto Shutdown Flag"
Cohesion: 0.33
Nodes (3): ArmaReforgerExecutableFlag, ArmaReforgerExecutableFlagError, Arma Reforger CLI startup flags.

### Community 44 - "Resource Database Regeneration"
Cohesion: 0.20
Nodes (3): RequestMessage, CommandRequestPacket, UnknownPacket

### Community 45 - "Debugger Port Setting"
Cohesion: 0.25
Nodes (3): Bind, Scoped, Singleton

### Community 48 - "Freeze Behaviour Mode"
Cohesion: 0.29
Nodes (3): ApplicationBase, Application (ApplicationBase), Application

### Community 52 - "Game Language Setting"
Cohesion: 0.33
Nodes (5): MANDATORY: Code Comment Conventions, MANDATORY: Git Rules, MANDATORY: Local Code Search/Traversal, MANDATORY: Use td for Task Management, MANDATORY: Worktree Management

### Community 53 - "Server FPS Cap"
Cohesion: 0.33
Nodes (3): PlayerResponseData, Parse a single data row from ``players`` output.          Returns ``None``  if t, A connected player returned by the ``players`` command.

### Community 74 - "ArmaDen Documentation"
Cohesion: 0.22
Nodes (8): ArmaDen, Build Locally, CLI Entrypoints, Install, Manual Application Setup, Packages, Run with Docker, Scaffold an Application

### Community 79 - "Package Init Module"
Cohesion: 0.06
Nodes (16): app() facade, HealthStatus, DefaultApi, DefaultApiError, GetAppStatus, Api, Controllers for API routes, LifecycleController (+8 more)

### Community 107 - ".resolve"
Cohesion: 0.20
Nodes (4): AppServiceProvider, ServiceProvider, TaskBuilder, providers()

### Community 112 - "StrEnum"
Cohesion: 0.18
Nodes (9): Application, ApplicationError, ApplicationException, ApplicationStatus, DefaultApplication, ConsoleServiceProvider, SteamCMD CLI command flags (prefixed with ``+``)., SteamCmdExecutableFlag (+1 more)

### Community 126 - "JSONResponse"
Cohesion: 0.36
Nodes (5): json_response(), JSONResponse, response(), ResponseFactory, StarletteJSONResponse

## Knowledge Gaps
- **25 isolated node(s):** `armaden`, `ApiResponseData`, `MANDATORY: Local Code Search/Traversal`, `MANDATORY: Use td for Task Management`, `MANDATORY: Worktree Management` (+20 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **198 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ArmaReforgerServerExecutable` connect `IoC Container Binding` to `.streams_delta`, `Application Kernel Interface`, `.vm_error_mode`, `Any`, `Server Path Configuration`, `Config`, `Self`, `TaskRuntimeInterface`, `App Config Module`, `__init__.py`, `Server Addon Loader`, `Addon Auto Repair Flag`, `Server Auto Restart Flag`, `Result`, `Local Backend Storage Flag`, `Freeze Detection Timeout`, `Crash File Retention Flag`, `List Scenarios Flag`, `Log Append Mode Flag`, `.autoshutdown`, `Error Dialog Suppression`, `.backend_disable_storage`, `.backend_local_storage`, `.custom`, `.debugger_port`, `.disable_ai`, `.disable_crash_reporter`, `Global Streaming Budget`, `.enable_night_grain`, `Agent Guidelines Docs`, `Package Init Module`, `Package Init Module`, `Package Init Module`, `Package Init Module`, `Package Init Module`, `Package Entry Point`, `Package Init Module`, `Package Init Module`, `Package Init Module`, `Package Init Module`, `Package Init Module`, `Package Init Module`, `.freeze_check`, `.jobsys_long_worker_count`, `.keep_crash_files`, `.keep_session_save`, `.log_voting`, `.nds`, `.no_backend`, `.nwk_resolution`, `.rpl_encode_as_long_jobs`, `.rpl_timeout_ms`, `.server_id`, `.silent_crash_report`, `.single_threaded_update`, `.staggering_budget`, `.disable_navmesh_streaming`, `.disable_shaders_build`, `.freeze_check_mode`, `.jobsys_long_worker_count`, `.limit_fps`, `.list_scenarios`, `.log_rdb_checksum`, `.log_scr_checksum`, `.logs_dir`, `.nds`, `.no_backend`, `.no_sound`, `.no_splash`, `.nwk_resolution`, `.rpl_encode_as_long_jobs`, `.script_authorize_all`, `.server_id`, `.server_world`, `RouteCompiler`?**
  _High betweenness centrality (0.149) - this node is a cross-community bridge._
- **Why does `InstanceContainer` connect `Arma Reforger Server Config` to `Task Lifecycle Management`, `Bound Method Resolution`, `Console Kernel Bootstrap`, `Debugger Port Setting`, `StrEnum`, `Framework Service Providers`, `Datagram Packet Parsing`, `FastAPI Default Application`, `Module Discovery Loader`, `Config Value Management`?**
  _High betweenness centrality (0.135) - this node is a cross-community bridge._
- **Why does `ServiceProvider` connect `Console Kernel Bootstrap` to `Arma Reforger Server Config`, `App Lifecycle Callbacks`, `Executable Argument Builder`, `Steam Query Bind Address`, `Bound Method Resolution`, `.resolve`, `Package Init Module`, `StrEnum`, `Config Value Management`?**
  _High betweenness centrality (0.091) - this node is a cross-community bridge._
- **Are the 16 inferred relationships involving `InstanceContainer` (e.g. with `Application` and `Config`) actually correct?**
  _`InstanceContainer` has 16 INFERRED edges - model-reasoned connections that need verification._
- **Are the 10 inferred relationships involving `ArmaReforgerServerExecutable` (e.g. with `ArmaReforgerServer` and `ArmaReforgerServerError`) actually correct?**
  _`ArmaReforgerServerExecutable` has 10 INFERRED edges - model-reasoned connections that need verification._
- **Are the 8 inferred relationships involving `CoreApplication` (e.g. with `InstanceContainer` and `ServiceProvider`) actually correct?**
  _`CoreApplication` has 8 INFERRED edges - model-reasoned connections that need verification._
- **What connects `# TODO: handle this`, `armaden`, `Accepts any Enum instance that implements a .message property.` to the rest of the system?**
  _119 weakly-connected nodes found - possible documentation gaps or missing edges._