# Graph Report - feature-auth-plumbing-worktree  (2026-07-10)

## Corpus Check
- 140 files · ~23,712 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1317 nodes · 2217 edges · 230 communities (52 shown, 178 thin omitted)
- Extraction: 83% EXTRACTED · 17% INFERRED · 0% AMBIGUOUS · INFERRED: 377 edges (avg confidence: 0.55)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `3f35cf5e`
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

## God Nodes (most connected - your core abstractions)
1. `InstanceContainer` - 114 edges
2. `ArmaReforgerServerExecutable` - 92 edges
3. `CoreApplication` - 47 edges
4. `Request` - 46 edges
5. `app()` - 38 edges
6. `BattleEyeRconClient` - 36 edges
7. `BattleEyeRconServer` - 29 edges
8. `ServiceProvider` - 27 edges
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

## Communities (230 total, 178 thin omitted)

### Community 0 - "IoC Container Binding"
Cohesion: 0.03
Nodes (31): ArmaReforgerServerExecutable, Redirect log output to the given directory., Bind the server to specific addresses / ports.          Keyword Args:, Cap the server frame rate., Load multiple addons at once.          Args:             mod_ids: Variable-lengt, Unique server identifier., Force loading a session save even if version mismatched., Disable storage loads and saves (online and local). (+23 more)

### Community 1 - "Supervisor Request Handling"
Cohesion: 0.10
Nodes (15): Future, SupervisorRequestArgs, SupervisorRequestData, SupervisorRequestKind, SupervisorRequestInterface, ProcessInfoData, RequestInfoData, Supervisor (+7 more)

### Community 3 - "Application Kernel Interface"
Cohesion: 0.12
Nodes (13): Configurable, TaskRuntimeInterface, Dictionary, ArmaReforgerRconClient, ArmaReforgerServer, ArmaReforgerServerError, ArmaReforgerServerException, Config (+5 more)

### Community 4 - "App Facade Container"
Cohesion: 0.08
Nodes (5): _resolve_config_type(), app(), config(), get_application(), T

### Community 5 - "Executable Argument Builder"
Cohesion: 0.08
Nodes (4): Task, TaskBuilder, TaskThreadingPolicy, AppServiceProvider

### Community 6 - "Task Lifecycle Management"
Cohesion: 0.13
Nodes (11): BoundMethod, CircularDependencyException, EntryNotFoundException, LogicException, get_class_for_callable(), get_contextual_attribute_from_dependency(), is_parameter_required(), Utility helpers shared between the container and bound-method resolution. (+3 more)

### Community 7 - "Async Datagram Transport"
Cohesion: 0.10
Nodes (9): DatagramProtocol, DatagramTransport, Exception, entry(), main(), entry(), main(), AsyncDatagramTransport (+1 more)

### Community 10 - "Core Application Bootstrap"
Cohesion: 0.14
Nodes (8): set_application(), bootstrap_console(), bootstrap_http(), ConsoleKernel, HttpKernel, Kernel, RuntimeEntry, TypedResult

### Community 11 - "BattleEye RCON Server"
Cohesion: 0.15
Nodes (7): BattleEyeRconServer, Client, ClientState, ResponseMessage, LoginStatus, LoginResponsePacket, IntEnum

### Community 12 - "Console Kernel Bootstrap"
Cohesion: 0.18
Nodes (3): ABC, DeferrableProvider, Controller

### Community 13 - "Scaffold File Generator"
Cohesion: 0.14
Nodes (10): Generator, GeneratorResult, _detect_poetry_package_path(), _fmt_list(), main(), _print_result(), # TODO: Register bindings on the service container., # TODO: Build and register tasks with the supervisor. (+2 more)

### Community 14 - "BattleEye RCON Client"
Cohesion: 0.13
Nodes (5): BattleEyeRconClient, ClientStatus, # TODO: handle stateful messages (responses to sequenced messages), # TODO: implement event system, # TODO: handle stateful messages (responses to sequences)

### Community 15 - "Arma Server Task Runtime"
Cohesion: 0.20
Nodes (4): ErrorInterface, KernelInterface, RconPacketInterface, Protocol

### Community 16 - "Server Path Configuration"
Cohesion: 0.13
Nodes (4): SteamCmd — Python wrapper for the steamcmd CLI tool., Config, SteamCmdExecutable, SteamCmdExecutableError

### Community 17 - "BattleEye Packet Protocol"
Cohesion: 0.18
Nodes (3): Message, Packet, UnknownPacket

### Community 19 - "Typed Environment Config"
Cohesion: 0.33
Nodes (10): A2SConfig, GameConfig, GamePropertiesConfig, GamePropertiesPersistence, JoinQueueConfig, OperatingConfig, RconConfig, ServerConfig (+2 more)

### Community 20 - "Login Packet Processing"
Cohesion: 0.16
Nodes (4): request(), RequestContext, RouteNotFoundException, UrlGenerator

### Community 21 - "Datagram Packet Parsing"
Cohesion: 0.15
Nodes (5): Config, Give, register_builtin_attributes(), Tag, ContextualAttribute

### Community 22 - "FastAPI Default Application"
Cohesion: 0.22
Nodes (3): BindingResolutionException, SelfBuilding, get_parameter_class_name()

### Community 24 - "Request"
Cohesion: 0.06
Nodes (6): HttpKernel, Middleware, MiddlewarePipeline, Request, NextCallable, StarletteRequest

### Community 26 - "Command Request Packet"
Cohesion: 0.14
Nodes (6): Error, ErrorKindInterface, Enforces that any error type object has a code string and message string., Accepts any Enum instance that implements a .message property., GenericError, ModuleLoaderError

### Community 28 - "Server Message Packet"
Cohesion: 0.20
Nodes (3): CommandHeader, CommandResponsePacket, BattleEyeInvalidPacketException

### Community 29 - "Config Value Management"
Cohesion: 0.18
Nodes (3): Application, SupervisorInterface, TypeDiscoveryError

### Community 32 - "Server Message Response"
Cohesion: 0.21
Nodes (3): RequestMessage, KeepAlivePacket, LoginRequestPacket

### Community 34 - "App Lifecycle Callbacks"
Cohesion: 0.24
Nodes (3): ModuleLoader, TypeDiscoveryServiceProvider, ModuleType

### Community 35 - "Async Subprocess Dispatch"
Cohesion: 0.17
Nodes (4): config(), env(), Facade for reading typed environment variables from the application., config()

### Community 36 - "Frontend Dependencies"
Cohesion: 0.20
Nodes (3): route(), URL, RouteParameterMissingException

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
Cohesion: 0.28
Nodes (3): AppServiceProvider, ServiceProvider, TaskBuilder

### Community 112 - "StrEnum"
Cohesion: 0.15
Nodes (11): Application, ApplicationError, ApplicationException, ApplicationStatus, DefaultApplication, ConsoleServiceProvider, HttpServiceProvider, ArmaReforgerExecutableFlag (+3 more)

### Community 123 - "RouteCompiler"
Cohesion: 0.25
Nodes (4): APIRouter, RouteCompiler, RouteParameter, HttpKernel

### Community 126 - "JSONResponse"
Cohesion: 0.36
Nodes (5): json_response(), JSONResponse, response(), ResponseFactory, StarletteJSONResponse

## Knowledge Gaps
- **25 isolated node(s):** `armaden`, `ApiResponseData`, `MANDATORY: Local Code Search/Traversal`, `MANDATORY: Use td for Task Management`, `MANDATORY: Worktree Management` (+20 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **178 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ArmaReforgerServerExecutable` connect `IoC Container Binding` to `Application Kernel Interface`, `App Facade Container`, `Server Path Configuration`, `Addon Auto Repair Flag`, `.autoshutdown`, `Error Dialog Suppression`, `.backend_disable_storage`, `.backend_local_storage`, `.custom`, `.debugger_port`, `.disable_ai`, `.disable_crash_reporter`, `Global Streaming Budget`, `.enable_night_grain`, `Agent Guidelines Docs`, `Package Init Module`, `Package Init Module`, `Package Init Module`, `Package Init Module`, `Package Init Module`, `Package Entry Point`, `Package Init Module`, `Package Init Module`, `Package Init Module`, `Package Init Module`, `Package Init Module`, `Package Init Module`, `.freeze_check`, `.jobsys_long_worker_count`, `.keep_crash_files`, `.keep_session_save`, `.log_voting`, `.nds`, `.no_backend`, `.nwk_resolution`, `.rpl_encode_as_long_jobs`, `.rpl_timeout_ms`, `.server_id`, `.silent_crash_report`, `.single_threaded_update`, `.staggering_budget`, `.streams_delta`, `.vm_error_mode`, `Any`, `Config`, `Self`, `TaskRuntimeInterface`, `__init__.py`, `Result`?**
  _High betweenness centrality (0.159) - this node is a cross-community bridge._
- **Why does `InstanceContainer` connect `Arma Reforger Server Config` to `App Config Module`, `Task Lifecycle Management`, `Bound Method Resolution`, `Console Kernel Bootstrap`, `Debugger Port Setting`, `StrEnum`, `Framework Service Providers`, `Datagram Packet Parsing`, `FastAPI Default Application`, `Module Discovery Loader`, `lifecycle_controller.py`, `Config Value Management`?**
  _High betweenness centrality (0.144) - this node is a cross-community bridge._
- **Why does `HttpServiceProvider` connect `StrEnum` to `Executable Argument Builder`, `Steam Query Bind Address`, `Bound Method Resolution`, `Command Response Packet`, `.resolve`, `Package Init Module`, `lifecycle_controller.py`, `RouteCompiler`?**
  _High betweenness centrality (0.093) - this node is a cross-community bridge._
- **Are the 16 inferred relationships involving `InstanceContainer` (e.g. with `Application` and `Config`) actually correct?**
  _`InstanceContainer` has 16 INFERRED edges - model-reasoned connections that need verification._
- **Are the 10 inferred relationships involving `ArmaReforgerServerExecutable` (e.g. with `ArmaReforgerServer` and `ArmaReforgerServerError`) actually correct?**
  _`ArmaReforgerServerExecutable` has 10 INFERRED edges - model-reasoned connections that need verification._
- **Are the 9 inferred relationships involving `CoreApplication` (e.g. with `InstanceContainer` and `ServiceProvider`) actually correct?**
  _`CoreApplication` has 9 INFERRED edges - model-reasoned connections that need verification._
- **What connects `armaden`, `Accepts any Enum instance that implements a .message property.`, `Enforces that any error type object has a code string and message string.` to the rest of the system?**
  _119 weakly-connected nodes found - possible documentation gaps or missing edges._