# Graph Report - armaden  (2026-07-11)

## Corpus Check
- 147 files · ~25,395 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1412 nodes · 2320 edges · 270 communities (58 shown, 212 thin omitted)
- Extraction: 87% EXTRACTED · 13% INFERRED · 0% AMBIGUOUS · INFERRED: 313 edges (avg confidence: 0.55)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `60bd69d6`
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
- ArmaReforgerExecutableError
- ArmaReforgerExecutableFlag
- Arma Games Module
- Scaffold CLI Tool
- App Config File
- Environment Variables File
- ArmaDen Core Package
- ArmaDen Documentation
- Package Init Module
- SteamCmdExecutableError
- LifecycleController
- Package Init Module
- Package Init Module
- Package Entry Point
- MiddlewarePipeline
- .addon
- Package Init Module
- Package Init Module
- Package Init Module
- .addons
- .jobsys_long_worker_count
- .keep_crash_files
- .addons_verify
- .auto_reload
- .backend_disable_storage
- .no_backend
- .cfg
- .config
- .rpl_timeout_ms
- .server_id
- .silent_crash_report
- .create_db
- .custom
- .streams_delta
- .vm_error_mode
- Any
- Config
- Self
- .resolve
- .debugger
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
- .freeze_check
- .generate_shaders
- .list_scenarios
- .log_rdb_checksum
- .jobsys_long_worker_count
- .logs_dir
- .language
- .no_backend
- .no_sound
- .no_splash
- .limit_fps
- .log_fs
- .log_level
- .log_scr_checksum
- .server_world
- .extend
- DatagramTransportInterface
- Executable
- ApplicationInterface
- route_compiler.py
- ApplicationInterface
- .log_voting
- RequestContext
- Result
- ServiceProvider
- Result
- .minidump
- .nds
- .nwk_resolution
- .region
- .rpl_encode_as_long_jobs
- .script_authorize_all
- .server_id
- .streaming_budget

## God Nodes (most connected - your core abstractions)
1. `InstanceContainer` - 112 edges
2. `ArmaReforgerServerExecutable` - 92 edges
3. `Request` - 55 edges
4. `CoreApplication` - 45 edges
5. `app()` - 38 edges
6. `BattleEyeRconClient` - 32 edges
7. `BattleEyeRconServer` - 29 edges
8. `Supervisor` - 26 edges
9. `SupervisorInterface` - 24 edges
10. `RouteRegistrar` - 23 edges

## Surprising Connections (you probably didn't know these)
- `Application` --uses--> `Application`  [INFERRED]
  user/bootstrap/application.py → src/armaden/framework/application.py
- `RestartAppService` --uses--> `SupervisorRequestData`  [INFERRED]
  user/app/http/actions/restart_app_service.py → src/armaden/framework/dto/supervisor_request_data.py
- `ShutdownAppService` --uses--> `SupervisorRequestData`  [INFERRED]
  user/app/http/actions/shutdown_app_service.py → src/armaden/framework/dto/supervisor_request_data.py
- `RestartRequestData` --uses--> `HealthStatus`  [INFERRED]
  user/app/http/dto/lifecycle_data.py → src/armaden/framework/enums/health_status.py
- `ServiceHealthData` --uses--> `HealthStatus`  [INFERRED]
  user/app/http/dto/lifecycle_data.py → src/armaden/framework/enums/health_status.py

## Import Cycles
- None detected.

## Communities (270 total, 212 thin omitted)

### Community 0 - "IoC Container Binding"
Cohesion: 0.13
Nodes (7): ArmaReforgerServerExecutable, Bind the server to specific addresses / ports.          Keyword Args:, Configure BattlEye / RCON remote console.          Keyword Args:             add, Force loading a session save even if version mismatched., Skip the initial load request and start a brand-new session., Limit the number of streams opened for a client (1..1000)., Threads for short jobs (capped to CPU count or 16).

### Community 1 - "Supervisor Request Handling"
Cohesion: 0.23
Nodes (11): SupervisorRequestArgs, SupervisorRequestData, SupervisorRequestKind, SupervisorRequestInterface, ProcessInfoData, RequestInfoData, SupervisorError, TaskRecord (+3 more)

### Community 3 - "Application Kernel Interface"
Cohesion: 0.07
Nodes (17): AbstractEventLoop, CommandHeader, CommandResponsePacket, DatagramTransportFactory, datetime, Future, LoginResponsePacket, Packet (+9 more)

### Community 4 - "App Facade Container"
Cohesion: 0.08
Nodes (4): app(), config(), get_application(), T

### Community 5 - "Executable Argument Builder"
Cohesion: 0.07
Nodes (4): Task, TaskBuilder, TaskThreadingPolicy, AppServiceProvider

### Community 6 - "Task Lifecycle Management"
Cohesion: 0.11
Nodes (10): Exception, BoundMethod, CircularDependencyException, EntryNotFoundException, LogicException, get_class_for_callable(), is_parameter_required(), Utility helpers shared between the container and bound-method resolution. (+2 more)

### Community 7 - "Async Datagram Transport"
Cohesion: 0.07
Nodes (10): DatagramProtocol, DatagramTransport, entry(), main(), entry(), main(), AsyncDatagramTransport, DatagramTransportInterface (+2 more)

### Community 9 - "Application Health Status"
Cohesion: 0.05
Nodes (6): Route, RouteFacade, GroupState, RouteGroup, RouteGroupStack, RouteRegistrar

### Community 10 - "Core Application Bootstrap"
Cohesion: 0.14
Nodes (8): set_application(), bootstrap_console(), bootstrap_http(), ConsoleKernel, HttpKernel, Kernel, RuntimeEntry, TypedResult

### Community 11 - "BattleEye RCON Server"
Cohesion: 0.19
Nodes (6): Client, ClientState, ResponseMessage, LoginStatus, LoginResponsePacket, IntEnum

### Community 13 - "Scaffold File Generator"
Cohesion: 0.14
Nodes (10): Generator, GeneratorResult, _detect_poetry_package_path(), _fmt_list(), main(), _print_result(), # TODO: Register bindings on the service container., # TODO: Build and register tasks with the supervisor. (+2 more)

### Community 15 - "Arma Server Task Runtime"
Cohesion: 0.20
Nodes (4): ErrorInterface, KernelInterface, RconPacketInterface, Protocol

### Community 19 - "Typed Environment Config"
Cohesion: 0.33
Nodes (10): A2SConfig, GameConfig, GamePropertiesConfig, GamePropertiesPersistence, JoinQueueConfig, OperatingConfig, RconConfig, ServerConfig (+2 more)

### Community 20 - "Login Packet Processing"
Cohesion: 0.06
Nodes (12): ApiUser, ConfigUserProvider, Any, AuthGuard, BasicAuthGuard, CustomHeaderGuard, Any, TokenGuard (+4 more)

### Community 21 - "Datagram Packet Parsing"
Cohesion: 0.15
Nodes (5): Config, Give, register_builtin_attributes(), Tag, ContextualAttribute

### Community 22 - "FastAPI Default Application"
Cohesion: 0.22
Nodes (3): BindingResolutionException, SelfBuilding, get_contextual_attribute_from_dependency()

### Community 23 - "Module Discovery Loader"
Cohesion: 0.15
Nodes (11): ApiUser, AuthGuard, AuthManager, ConfigUserProvider, Middleware, AuthManager, Any, Authenticate (+3 more)

### Community 26 - "Command Request Packet"
Cohesion: 0.20
Nodes (5): Error, ErrorKindInterface, Enforces that any error type object has a code string and message string., Accepts any Enum instance that implements a .message property., GenericError

### Community 32 - "Server Message Response"
Cohesion: 0.21
Nodes (3): RequestMessage, LoginRequestPacket, UnknownPacket

### Community 34 - "App Lifecycle Callbacks"
Cohesion: 0.19
Nodes (5): ModuleLoader, ModuleLoaderError, TypeDiscoveryError, TypeDiscoveryServiceProvider, ModuleType

### Community 35 - "Async Subprocess Dispatch"
Cohesion: 0.17
Nodes (4): config(), env(), Facade for reading typed environment variables from the application., config()

### Community 37 - "App Config Module"
Cohesion: 0.16
Nodes (9): Configurable, _resolve_config_type(), TaskRuntimeInterface, Dictionary, ArmaReforgerServerError, ArmaReforgerServerException, Config, ExecutableContainer (+1 more)

### Community 40 - "Addon Auto Repair Flag"
Cohesion: 0.25
Nodes (4): APIRouter, RouteCompiler, RouteParameter, HttpKernel

### Community 42 - "Auto Shutdown Flag"
Cohesion: 0.18
Nodes (9): Application, ApplicationError, ApplicationException, ApplicationStatus, DefaultApplication, ConsoleServiceProvider, SteamCMD CLI command flags (prefixed with ``+``)., SteamCmdExecutableFlag (+1 more)

### Community 45 - "Debugger Port Setting"
Cohesion: 0.25
Nodes (3): Bind, Scoped, Singleton

### Community 48 - "Freeze Behaviour Mode"
Cohesion: 0.29
Nodes (3): ApplicationBase, Application (ApplicationBase), Application

### Community 50 - "Log File Retention Limit"
Cohesion: 0.15
Nodes (6): AppServiceProvider, ServiceProvider, TaskBuilder, providers(), HttpServiceProvider, Result

### Community 52 - "Game Language Setting"
Cohesion: 0.11
Nodes (5): route(), URL, RouteNotFoundException, RouteParameterMissingException, UrlGenerator

### Community 53 - "Server FPS Cap"
Cohesion: 0.33
Nodes (3): PlayerResponseData, Parse a single data row from ``players`` output.          Returns ``None``  if t, A connected player returned by the ``players`` command.

### Community 60 - ".backend_disable_storage"
Cohesion: 0.25
Nodes (3): Api, ApiResponseData, ApiStatus

### Community 65 - ".disable_crash_reporter"
Cohesion: 0.33
Nodes (3): Any, NextCallable, Request

### Community 67 - "ArmaReforgerExecutableError"
Cohesion: 0.47
Nodes (3): ArmaReforgerExecutableError, Config, Arma Reforger dedicated server wrapper.  Provides a typed, fluent interface for

### Community 68 - "ArmaReforgerExecutableFlag"
Cohesion: 0.33
Nodes (3): ArmaReforgerExecutableFlag, ArmaReforgerExecutableFlagError, Arma Reforger CLI startup flags.

### Community 74 - "ArmaDen Documentation"
Cohesion: 0.22
Nodes (8): ArmaDen, Build Locally, CLI Entrypoints, Install, Manual Application Setup, Packages, Run with Docker, Scaffold an Application

### Community 76 - "SteamCmdExecutableError"
Cohesion: 0.47
Nodes (3): SteamCmd — Python wrapper for the steamcmd CLI tool., Config, SteamCmdExecutableError

### Community 79 - "Package Init Module"
Cohesion: 0.16
Nodes (12): app() facade, HealthStatus, GetAppStatus, RestartAppService, ShutdownAppService, Controllers for API routes, HealthResponseData, RestartRequestData (+4 more)

### Community 126 - "JSONResponse"
Cohesion: 0.36
Nodes (5): json_response(), JSONResponse, response(), ResponseFactory, StarletteJSONResponse

### Community 253 - "Executable"
Cohesion: 0.33
Nodes (5): MANDATORY: Code Comment Conventions, MANDATORY: Git Rules, MANDATORY: Local Code Search/Traversal, MANDATORY: Use td for Task Management, MANDATORY: Worktree Management

### Community 259 - "Result"
Cohesion: 0.17
Nodes (5): ABC, DeferrableProvider, ServiceProvider, Controller, Result

## Knowledge Gaps
- **25 isolated node(s):** `MANDATORY: Local Code Search/Traversal`, `MANDATORY: Use td for Task Management`, `MANDATORY: Worktree Management`, `MANDATORY: Code Comment Conventions`, `MANDATORY: Git Rules` (+20 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **212 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ArmaReforgerServerExecutable` connect `IoC Container Binding` to `.log_voting`, `.streams_delta`, `.minidump`, `.nds`, `.nwk_resolution`, `.region`, `.rpl_encode_as_long_jobs`, `.vm_error_mode`, `.script_authorize_all`, `.server_id`, `Any`, `.streaming_budget`, `Server Path Configuration`, `Config`, `Self`, `Login Response Packet`, `App Config Module`, `Steam Query Bind Address`, `__init__.py`, `Result`, `Freeze Detection Timeout`, `Crash File Retention Flag`, `Log Append Mode Flag`, `.autoshutdown`, `Error Dialog Suppression`, `.backend_local_storage`, `.custom`, `.debugger_port`, `.disable_ai`, `Global Streaming Budget`, `ArmaReforgerExecutableError`, `.server_world`, `Package Init Module`, `Package Init Module`, `Package Entry Point`, `.addon`, `Package Init Module`, `Package Init Module`, `Package Init Module`, `.addons`, `.jobsys_long_worker_count`, `.keep_crash_files`, `.addons_verify`, `.auto_reload`, `.backend_disable_storage`, `.no_backend`, `.cfg`, `.config`, `.rpl_timeout_ms`, `.server_id`, `.silent_crash_report`, `.create_db`, `.custom`, `.disable_navmesh_streaming`, `.disable_shaders_build`, `.freeze_check_mode`, `.freeze_check`, `.generate_shaders`, `.list_scenarios`, `.debugger`, `.jobsys_long_worker_count`, `.log_rdb_checksum`, `.language`, `StrEnum`, `.logs_dir`, `.no_backend`, `.limit_fps`, `.log_fs`, `.log_level`, `.log_scr_checksum`, `.no_sound`, `.no_splash`, `RouteCompiler`, `DatagramTransportInterface`?**
  _High betweenness centrality (0.136) - this node is a cross-community bridge._
- **Why does `InstanceContainer` connect `Arma Reforger Server Config` to `Task Lifecycle Management`, `Bound Method Resolution`, `Server Auto Restart Flag`, `Auto Shutdown Flag`, `Local Backend Storage Flag`, `Debugger Port Setting`, `Framework Service Providers`, `Datagram Packet Parsing`, `FastAPI Default Application`, `Request`, `Config Value Management`?**
  _High betweenness centrality (0.121) - this node is a cross-community bridge._
- **Are the 14 inferred relationships involving `InstanceContainer` (e.g. with `Application` and `Config`) actually correct?**
  _`InstanceContainer` has 14 INFERRED edges - model-reasoned connections that need verification._
- **Are the 10 inferred relationships involving `ArmaReforgerServerExecutable` (e.g. with `ArmaReforgerServer` and `ArmaReforgerServerError`) actually correct?**
  _`ArmaReforgerServerExecutable` has 10 INFERRED edges - model-reasoned connections that need verification._
- **Are the 7 inferred relationships involving `CoreApplication` (e.g. with `InstanceContainer` and `SupervisorInterface`) actually correct?**
  _`CoreApplication` has 7 INFERRED edges - model-reasoned connections that need verification._
- **What connects `High-level RCON client for Arma Reforger with typed command methods.      Each m`, `MANDATORY: Local Code Search/Traversal`, `MANDATORY: Use td for Task Management` to the rest of the system?**
  _117 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `IoC Container Binding` be split into smaller, more focused modules?**
  _Cohesion score 0.1323529411764706 - nodes in this community are weakly interconnected._