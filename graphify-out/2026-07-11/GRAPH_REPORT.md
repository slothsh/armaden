# Graph Report - armaden  (2026-07-11)

## Corpus Check
- 147 files · ~25,150 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1399 nodes · 2298 edges · 235 communities (54 shown, 181 thin omitted)
- Extraction: 86% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 316 edges (avg confidence: 0.55)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `5c850e37`
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
- Arma Games Module
- Scaffold CLI Tool
- App Config File
- Environment Variables File
- ArmaDen Core Package
- ArmaDen Documentation
- Package Init Module
- Package Init Module
- Package Init Module
- Package Entry Point
- Package Init Module
- Package Init Module
- Package Init Module
- .jobsys_long_worker_count
- .keep_crash_files
- .no_backend
- .rpl_timeout_ms
- .server_id
- .silent_crash_report
- .streams_delta
- .vm_error_mode
- Any
- Config
- Self
- .resolve
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
- .freeze_check_mode
- .list_scenarios
- .log_rdb_checksum
- .logs_dir
- .no_backend
- .no_sound
- .no_splash
- .server_world
- .extend
- DatagramTransportInterface
- Executable
- ApplicationInterface
- route_compiler.py
- ApplicationInterface
- RequestContext
- Result
- ServiceProvider
- Result

## God Nodes (most connected - your core abstractions)
1. `InstanceContainer` - 112 edges
2. `ArmaReforgerServerExecutable` - 92 edges
3. `Request` - 55 edges
4. `CoreApplication` - 45 edges
5. `app()` - 38 edges
6. `BattleEyeRconClient` - 30 edges
7. `BattleEyeRconServer` - 29 edges
8. `Supervisor` - 26 edges
9. `SupervisorInterface` - 24 edges
10. `RouteRegistrar` - 23 edges

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

## Communities (235 total, 181 thin omitted)

### Community 0 - "IoC Container Binding"
Cohesion: 0.03
Nodes (34): ArmaReforgerServerExecutable, Path to a server configuration JSON file., Bind the server to specific addresses / ports.          Keyword Args:, Configure BattlEye / RCON remote console.          Keyword Args:             add, Cap the server frame rate., Load a server-side addon (mod) by ID.          May be called multiple times to l, Load multiple addons at once.          Args:             mod_ids: Variable-lengt, Auto-restart the server when it crashes (default: ``True``). (+26 more)

### Community 1 - "Supervisor Request Handling"
Cohesion: 0.08
Nodes (16): Future, SupervisorRequestArgs, SupervisorRequestData, SupervisorRequestKind, SupervisorRequestInterface, TaskInterface, ProcessInfoData, RequestInfoData (+8 more)

### Community 3 - "Application Kernel Interface"
Cohesion: 0.09
Nodes (14): AbstractEventLoop, CommandHeader, CommandResponsePacket, DatagramTransportFactory, datetime, LoginResponsePacket, Packet, ServerMessageRequestPacket (+6 more)

### Community 4 - "App Facade Container"
Cohesion: 0.09
Nodes (4): app(), config(), get_application(), T

### Community 5 - "Executable Argument Builder"
Cohesion: 0.08
Nodes (4): Task, TaskBuilder, TaskThreadingPolicy, AppServiceProvider

### Community 6 - "Task Lifecycle Management"
Cohesion: 0.15
Nodes (9): BoundMethod, LogicException, get_class_for_callable(), get_parameter_class_name(), is_parameter_required(), Utility helpers shared between the container and bound-method resolution., Determine the class name associated with a callable for build-stack tracking., resolve_string_to_class() (+1 more)

### Community 7 - "Async Datagram Transport"
Cohesion: 0.12
Nodes (9): DatagramProtocol, DatagramTransport, Exception, entry(), main(), entry(), main(), AsyncDatagramTransport (+1 more)

### Community 10 - "Core Application Bootstrap"
Cohesion: 0.14
Nodes (8): set_application(), bootstrap_console(), bootstrap_http(), ConsoleKernel, HttpKernel, Kernel, RuntimeEntry, TypedResult

### Community 11 - "BattleEye RCON Server"
Cohesion: 0.17
Nodes (6): BattleEyeRconServer, Client, ClientState, ResponseMessage, LoginStatus, IntEnum

### Community 12 - "Console Kernel Bootstrap"
Cohesion: 0.16
Nodes (3): KeepAlivePacket, LoginResponsePacket, BattleEyeInvalidPacketException

### Community 13 - "Scaffold File Generator"
Cohesion: 0.14
Nodes (10): Generator, GeneratorResult, _detect_poetry_package_path(), _fmt_list(), main(), _print_result(), # TODO: Register bindings on the service container., # TODO: Build and register tasks with the supervisor. (+2 more)

### Community 15 - "Arma Server Task Runtime"
Cohesion: 0.20
Nodes (4): ErrorInterface, KernelInterface, RconPacketInterface, Protocol

### Community 16 - "Server Path Configuration"
Cohesion: 0.13
Nodes (4): SteamCmd — Python wrapper for the steamcmd CLI tool., Config, SteamCmdExecutable, SteamCmdExecutableError

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
Cohesion: 0.15
Nodes (4): Error, Accepts any Enum instance that implements a .message property., GenericError, ModuleLoaderError

### Community 29 - "Config Value Management"
Cohesion: 0.18
Nodes (3): Application, SupervisorInterface, TypeDiscoveryError

### Community 33 - "Type Discovery Provider"
Cohesion: 0.19
Nodes (3): RequestMessage, ServerMessageResponsePacket, UnknownPacket

### Community 34 - "App Lifecycle Callbacks"
Cohesion: 0.24
Nodes (3): ModuleLoader, TypeDiscoveryServiceProvider, ModuleType

### Community 35 - "Async Subprocess Dispatch"
Cohesion: 0.17
Nodes (4): config(), env(), Facade for reading typed environment variables from the application., config()

### Community 37 - "App Config Module"
Cohesion: 0.12
Nodes (13): Configurable, TaskRuntimeInterface, Dictionary, ArmaReforgerRconClient, ArmaReforgerServer, ArmaReforgerServerError, ArmaReforgerServerException, Config (+5 more)

### Community 40 - "Addon Auto Repair Flag"
Cohesion: 0.29
Nodes (4): APIRouter, RouteCompiler, RouteParameter, HttpKernel

### Community 42 - "Auto Shutdown Flag"
Cohesion: 0.16
Nodes (10): Application, ApplicationError, ApplicationException, ApplicationStatus, DefaultApplication, ConsoleServiceProvider, ArmaReforgerExecutableFlag, ArmaReforgerExecutableFlagError (+2 more)

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

### Community 74 - "ArmaDen Documentation"
Cohesion: 0.22
Nodes (8): ArmaDen, Build Locally, CLI Entrypoints, Install, Manual Application Setup, Packages, Run with Docker, Scaffold an Application

### Community 79 - "Package Init Module"
Cohesion: 0.07
Nodes (16): app() facade, HealthStatus, DefaultApi, DefaultApiError, GetAppStatus, Api, Controllers for API routes, LifecycleController (+8 more)

### Community 126 - "JSONResponse"
Cohesion: 0.36
Nodes (5): json_response(), JSONResponse, response(), ResponseFactory, StarletteJSONResponse

### Community 253 - "Executable"
Cohesion: 0.33
Nodes (5): MANDATORY: Code Comment Conventions, MANDATORY: Git Rules, MANDATORY: Local Code Search/Traversal, MANDATORY: Use td for Task Management, MANDATORY: Worktree Management

### Community 259 - "Result"
Cohesion: 0.06
Nodes (12): ABC, Any, Executable, DeferrableProvider, ServiceProvider, Controller, HttpKernel, Middleware (+4 more)

## Knowledge Gaps
- **25 isolated node(s):** `MANDATORY: Local Code Search/Traversal`, `MANDATORY: Use td for Task Management`, `MANDATORY: Worktree Management`, `MANDATORY: Code Comment Conventions`, `MANDATORY: Git Rules` (+20 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **181 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ArmaReforgerServerExecutable` connect `IoC Container Binding` to `Result`, `Server Path Configuration`, `Command Response Packet`, `App Config Module`, `Freeze Detection Timeout`, `Crash File Retention Flag`, `List Scenarios Flag`, `Log Append Mode Flag`, `.autoshutdown`, `Error Dialog Suppression`, `.backend_disable_storage`, `.backend_local_storage`, `.custom`, `.debugger_port`, `.disable_ai`, `.disable_crash_reporter`, `Global Streaming Budget`, `Package Init Module`, `Package Init Module`, `Package Entry Point`, `Package Init Module`, `Package Init Module`, `Package Init Module`, `.jobsys_long_worker_count`, `.keep_crash_files`, `.no_backend`, `.rpl_timeout_ms`, `.server_id`, `.silent_crash_report`, `.disable_navmesh_streaming`, `.streams_delta`, `.freeze_check_mode`, `.vm_error_mode`, `Any`, `.list_scenarios`, `.log_rdb_checksum`, `Config`, `.logs_dir`, `Self`, `.no_backend`, `.no_sound`, `.no_splash`, `__init__.py`, `Result`, `.server_world`, `RouteCompiler`?**
  _High betweenness centrality (0.139) - this node is a cross-community bridge._
- **Why does `InstanceContainer` connect `Arma Reforger Server Config` to `Task Lifecycle Management`, `Bound Method Resolution`, `Server Auto Restart Flag`, `Auto Shutdown Flag`, `Local Backend Storage Flag`, `Debugger Port Setting`, `Framework Service Providers`, `Datagram Packet Parsing`, `FastAPI Default Application`, `Request`, `Config Value Management`?**
  _High betweenness centrality (0.132) - this node is a cross-community bridge._
- **Why does `SupervisorInterface` connect `Config Value Management` to `Supervisor Request Handling`, `App Lifecycle Callbacks`, `Bound Method Resolution`, `Auto Shutdown Flag`, `.resolve`, `Arma Server Task Runtime`, `__init__.py`?**
  _High betweenness centrality (0.073) - this node is a cross-community bridge._
- **Are the 14 inferred relationships involving `InstanceContainer` (e.g. with `Application` and `Config`) actually correct?**
  _`InstanceContainer` has 14 INFERRED edges - model-reasoned connections that need verification._
- **Are the 10 inferred relationships involving `ArmaReforgerServerExecutable` (e.g. with `ArmaReforgerServer` and `ArmaReforgerServerError`) actually correct?**
  _`ArmaReforgerServerExecutable` has 10 INFERRED edges - model-reasoned connections that need verification._
- **Are the 7 inferred relationships involving `CoreApplication` (e.g. with `InstanceContainer` and `SupervisorInterface`) actually correct?**
  _`CoreApplication` has 7 INFERRED edges - model-reasoned connections that need verification._
- **What connects `MANDATORY: Local Code Search/Traversal`, `MANDATORY: Use td for Task Management`, `MANDATORY: Worktree Management` to the rest of the system?**
  _116 weakly-connected nodes found - possible documentation gaps or missing edges._