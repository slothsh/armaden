# Graph Report - armaden  (2026-07-11)

## Corpus Check
- 168 files · ~31,703 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1637 nodes · 3350 edges · 171 communities (62 shown, 109 thin omitted)
- Extraction: 78% EXTRACTED · 22% INFERRED · 0% AMBIGUOUS · INFERRED: 732 edges (avg confidence: 0.55)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `1ef03bc5`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- ArmaReforgerServerExecutable
- Request
- AuthManager
- Protocol
- InstanceContainer
- SteamCmdExecutable
- BattleEyeRconServer
- lifecycle_controller.py
- TaskThreadingPolicy
- RouteFacade
- Supervisor
- CoreApplication
- HealthStatus
- BattleEyeRconClient
- app
- Packet
- ConsoleKernel
- .generate
- ServiceProvider
- TaskRuntimeInterface
- route_compiler.py
- BoundMethod
- TaskGraph
- AsyncDatagramTransport
- UrlGenerator
- Path
- CommandResponsePacket
- HttpServiceProvider
- TaskRuntime
- Exception
- ProcessBuilder
- TaskBuilder
- WorkerPool
- .get_alias
- RestartPolicy
- env
- ScheduleBuilder
- ContextualAttribute
- SupervisorInterface
- ApplicationInterface
- RouteGroupStack
- RouteRegistrar
- CommandResponse
- _LegacyTask
- _BuiltTask
- ConcurrencyFacade
- SubprocessHandle
- ._initialize_configs
- TaskInjector
- Task
- RouteGroup
- TaskBuilder
- TaskInterface
- TaskBuilderInterface
- TaskRuntime
- TypedDict
- get_application
- AppServiceProvider
- URL
- JSONResponse
- CommandRequestPacket
- ArmaDen
- URL
- Bind
- ServerMessageRequestPacket
- .merge
- PlayerResponseData
- AGENTS.md
- Application
- task.py
- LoginResponsePacket
- ServerMessageResponsePacket
- .kind
- .addon
- .addons_repair
- .addons_verify
- .ai_limit
- .backend_disable_storage
- .backend_local_storage
- .check_instance
- .disable_ai
- .freeze_check
- .generate_shaders
- .jobsys_short_worker_count
- .keep_crash_files
- .limit_fps
- .list_scenarios
- .log_append
- .log_fs
- .log_scr_checksum
- .log_time
- .minidump
- .no_splash
- .player_limits
- .region
- .scenario
- .server_id
- .silent_crash_report
- .single_threaded_update
- .vm_error_mode
- Any
- Any
- NextCallable
- Any
- Any
- Any
- Any
- Parameter
- Any
- Result
- Self
- StatusCallback
- TaskCallback
- Any
- Result
- Self
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
- FastAPI
- Result
- Any
- Result
- Self
- Any
- Parameter
- Any
- Result
- AbstractEventLoop
- Any
- AsyncStreamCallback
- Path
- Result
- Result
- Result
- Result
- armaden

## God Nodes (most connected - your core abstractions)
1. `InstanceContainer` - 132 edges
2. `ArmaReforgerServerExecutable` - 94 edges
3. `Request` - 58 edges
4. `Supervisor` - 53 edges
5. `CoreApplication` - 47 edges
6. `BattleEyeRconClient` - 46 edges
7. `app()` - 42 edges
8. `TaskGraph` - 39 edges
9. `SupervisorInterface` - 36 edges
10. `TaskRuntimeInterface` - 33 edges

## Surprising Connections (you probably didn't know these)
- `ServiceHealthData` --uses--> `HealthStatus`  [INFERRED]
  user/app/http/dto/lifecycle_data.py → src/armaden/framework/enums/health_status.py
- `Application` --uses--> `Application`  [INFERRED]
  user/bootstrap/application.py → src/armaden/framework/application.py
- `AppServiceProvider` --uses--> `ServiceProvider`  [INFERRED]
  user/app/providers/app_service_provider.py → src/armaden/framework/classes/service_provider.py
- `TelemetryServiceProvider` --uses--> `ServiceProvider`  [INFERRED]
  user/app/providers/telemetry_service_provider.py → src/armaden/framework/classes/service_provider.py
- `RestartAppService` --uses--> `SupervisorRequestData`  [INFERRED]
  user/app/http/actions/restart_app_service.py → src/armaden/framework/dto/supervisor_request_data.py

## Import Cycles
- None detected.

## Communities (171 total, 109 thin omitted)

### Community 0 - "ArmaReforgerServerExecutable"
Cohesion: 0.03
Nodes (40): ArmaReforgerServerExecutable, Result, Bind the server to specific addresses / ports.          Keyword Args:, Configure A2S query endpoint.          Keyword Args:             address: IP add, Configure BattlEye / RCON remote console.          Keyword Args:             add, Load multiple addons at once.          Args:             mod_ids: Variable-lengt, Auto-restart the server when it crashes (default: ``True``)., Force loading a session save even if version mismatched. (+32 more)

### Community 1 - "Request"
Cohesion: 0.05
Nodes (8): Request, HttpKernel, Middleware, Any, NextCallable, MiddlewarePipeline, Any, StarletteRequest

### Community 2 - "AuthManager"
Cohesion: 0.07
Nodes (13): ApiUser, AuthManager, Authenticate, AuthenticateWithBasic, AuthenticateWithHeader, AuthenticateWithToken, ConfigUserProvider, AuthGuard (+5 more)

### Community 3 - "Protocol"
Cohesion: 0.05
Nodes (17): Protocol, Error, ErrorKindInterface, Enforces that any error type object has a code string and message string., Accepts any Enum instance that implements a .message property., GenericError, ErrorInterface, CoreApplicationInterface (+9 more)

### Community 5 - "SteamCmdExecutable"
Cohesion: 0.07
Nodes (15): Executable, Path, PushValue, Result, Self, SteamCMD CLI command flags (prefixed with ``+``)., SteamCmdExecutableFlag, SteamCmd — Python wrapper for the steamcmd CLI tool. (+7 more)

### Community 6 - "BattleEyeRconServer"
Cohesion: 0.10
Nodes (13): IntEnum, BattleEyeRconServer, Client, ClientState, AbstractEventLoop, DatagramTransportFactory, datetime, Exception (+5 more)

### Community 7 - "lifecycle_controller.py"
Cohesion: 0.13
Nodes (15): GetAppStatus, RestartAppService, ShutdownAppService, Api, Any, Controllers for API routes, LifecycleController, ApiResponseData (+7 more)

### Community 8 - "TaskThreadingPolicy"
Cohesion: 0.21
Nodes (20): TaskError, ProcessFacade, ScheduleFacade, PolicyEngine, TaskGraphState, SupervisorRequestArgs, SupervisorRequestData, SupervisorRequestKind (+12 more)

### Community 9 - "RouteFacade"
Cohesion: 0.11
Nodes (6): config(), Any, Any, Route, Any, RouteFacade

### Community 10 - "Supervisor"
Cohesion: 0.12
Nodes (5): AbstractEventLoop, Future, Result, Self, Supervisor

### Community 12 - "HealthStatus"
Cohesion: 0.13
Nodes (18): DefaultApiError, Configurable, _resolve_config_type(), HealthStatus, Dictionary, ArmaReforgerServerError, ArmaReforgerServerException, Config (+10 more)

### Community 13 - "BattleEyeRconClient"
Cohesion: 0.11
Nodes (5): BattleEyeRconClient, AbstractEventLoop, Any, DatagramTransportFactory, Exception

### Community 15 - "Packet"
Cohesion: 0.14
Nodes (4): KeepAlivePacket, BattleEyeInvalidPacketException, Packet, Self

### Community 16 - "ConsoleKernel"
Cohesion: 0.15
Nodes (9): set_application(), bootstrap_console(), bootstrap_http(), ConsoleKernel, HttpKernel, Kernel, Any, RuntimeEntry (+1 more)

### Community 17 - ".generate"
Cohesion: 0.14
Nodes (12): Generator, GeneratorResult, Path, _detect_poetry_package_path(), _fmt_list(), main(), _print_result(), Path (+4 more)

### Community 18 - "ServiceProvider"
Cohesion: 0.13
Nodes (7): ABC, MultiImplementation, DeferrableProvider, ServiceProvider, TypeDiscoveryError, TypeDiscoveryServiceProvider, Controller

### Community 20 - "TaskRuntimeInterface"
Cohesion: 0.15
Nodes (6): TaskRuntimeInterface, ArmaReforgerServer, Any, Result, Self, Result

### Community 21 - "route_compiler.py"
Cohesion: 0.16
Nodes (8): APIRouter, HttpKernel, RequestContext, Any, FastAPI, RouteCompiler, RouteParameter, RouteDefinition

### Community 22 - "BoundMethod"
Cohesion: 0.17
Nodes (11): BoundMethod, get_class_for_callable(), get_contextual_attribute_from_dependency(), get_parameter_class_name(), is_parameter_required(), Any, Parameter, Utility helpers shared between the container and bound-method resolution. (+3 more)

### Community 23 - "TaskGraph"
Cohesion: 0.19
Nodes (5): Lifecycle, DuplicateTaskNameError, TaskGraphCycleError, TaskGraph, TaskGraphCompiler

### Community 24 - "AsyncDatagramTransport"
Cohesion: 0.13
Nodes (10): DatagramProtocol, DatagramTransport, entry(), main(), entry(), main(), AsyncDatagramTransport, Any (+2 more)

### Community 25 - "UrlGenerator"
Cohesion: 0.14
Nodes (6): auth(), request(), Any, RouteNotFoundException, RouteParameterMissingException, UrlGenerator

### Community 26 - "Path"
Cohesion: 0.10
Nodes (11): Path, Path to a server configuration JSON file., Directory for profiles (saves, logs, settings).          The directory is create, Redirect log output to the given directory., Path to a session save to load on startup., Additional directories to search for mods.          Multiple directories can be, Directory where addons are downloaded., Directory for temporary addon data. (+3 more)

### Community 27 - "CommandResponsePacket"
Cohesion: 0.20
Nodes (8): ClientStatus, Message, _PendingCommand, datetime, Future, ServerMessage, CommandHeader, CommandResponsePacket

### Community 28 - "HttpServiceProvider"
Cohesion: 0.18
Nodes (10): Application, ApplicationError, ApplicationException, ApplicationStatus, HttpServiceProvider, DefaultApplication, Result, ModuleLoader (+2 more)

### Community 29 - "TaskRuntime"
Cohesion: 0.15
Nodes (4): Event, ProgressChannel, ProgressUpdate, TaskRuntime

### Community 30 - "Exception"
Cohesion: 0.18
Nodes (6): Exception, BindingResolutionException, CircularDependencyException, EntryNotFoundException, LogicException, SelfBuilding

### Community 33 - "WorkerPool"
Cohesion: 0.18
Nodes (5): GraphTaskRuntime, Semaphore, _result_error(), _run_shutdown(), WorkerPool

### Community 35 - "RestartPolicy"
Cohesion: 0.22
Nodes (7): RestartPolicy, _emit_banner(), TelemetryServiceProvider, CollectServerTelemetryTask, FormatTelemetryReportTask, TelemetryAlertTask, TelemetryReadinessProbeTask

### Community 36 - "env"
Cohesion: 0.13
Nodes (7): config(), config(), env(), Any, Facade for reading typed environment variables from the application., config(), ArmaReforgerServerConfig

### Community 38 - "ContextualAttribute"
Cohesion: 0.20
Nodes (6): ContextualAttribute, Config, Give, Any, Parameter, Tag

### Community 40 - "ApplicationInterface"
Cohesion: 0.21
Nodes (7): ApplicationInterface, Any, Result, Any, Path, Result, RouteDiscoveryServiceProvider

### Community 41 - "RouteGroupStack"
Cohesion: 0.19
Nodes (4): Any, GroupState, Any, RouteGroupStack

### Community 43 - "CommandResponse"
Cohesion: 0.26
Nodes (3): ArmaReforgerRconClient, High-level RCON client for Arma Reforger with typed command methods.      Each m, CommandResponse

### Community 48 - "._initialize_configs"
Cohesion: 0.24
Nodes (4): providers(), ModuleType, Any, Result

### Community 49 - "TaskInjector"
Cohesion: 0.30
Nodes (3): UnresolvedDependencyError, TaskInjector, _UnresolvedSentinel

### Community 55 - "TaskRuntime"
Cohesion: 0.18
Nodes (4): Any, AsyncStreamCallback, Path, TaskRuntime

### Community 56 - "TypedDict"
Cohesion: 0.33
Nodes (10): A2SConfig, GameConfig, GamePropertiesConfig, GamePropertiesPersistence, JoinQueueConfig, OperatingConfig, RconConfig, ServerConfig (+2 more)

### Community 59 - "URL"
Cohesion: 0.29
Nodes (3): Any, route(), URL

### Community 60 - "JSONResponse"
Cohesion: 0.36
Nodes (6): json_response(), JSONResponse, Any, response(), ResponseFactory, StarletteJSONResponse

### Community 62 - "ArmaDen"
Cohesion: 0.22
Nodes (8): ArmaDen, Build Locally, CLI Entrypoints, Install, Manual Application Setup, Packages, Run with Docker, Scaffold an Application

### Community 64 - "Bind"
Cohesion: 0.25
Nodes (3): Bind, Scoped, Singleton

### Community 67 - "PlayerResponseData"
Cohesion: 0.33
Nodes (4): PlayerResponseData, Self, Parse a single data row from ``players`` output.          Returns ``None``  if t, A connected player returned by the ``players`` command.

### Community 68 - "AGENTS.md"
Cohesion: 0.33
Nodes (5): MANDATORY: Code Comment Conventions, MANDATORY: Git Rules, MANDATORY: Local Code Search/Traversal, MANDATORY: Use td for Task Management, MANDATORY: Worktree Management

### Community 69 - "Application"
Cohesion: 0.33
Nodes (3): ApplicationBase, Application, Result

## Knowledge Gaps
- **13 isolated node(s):** `armaden`, `MANDATORY: Local Code Search/Traversal`, `MANDATORY: Use td for Task Management`, `MANDATORY: Worktree Management`, `MANDATORY: Code Comment Conventions` (+8 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **109 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ArmaReforgerServerExecutable` connect `ArmaReforgerServerExecutable` to `SteamCmdExecutable`, `HealthStatus`, `TaskRuntimeInterface`, `Path`, `.merge`, `.addon`, `.addons_repair`, `.addons_verify`, `.ai_limit`, `.backend_disable_storage`, `.backend_local_storage`, `.check_instance`, `.disable_ai`, `.freeze_check`, `.generate_shaders`, `.jobsys_short_worker_count`, `.keep_crash_files`, `.limit_fps`, `.list_scenarios`, `.log_append`, `.log_fs`, `.log_scr_checksum`, `.log_time`, `.minidump`, `.no_splash`, `.player_limits`, `.region`, `.scenario`, `.server_id`, `.silent_crash_report`, `.single_threaded_update`, `.vm_error_mode`?**
  _High betweenness centrality (0.183) - this node is a cross-community bridge._
- **Why does `InstanceContainer` connect `InstanceContainer` to `Bind`, `WorkerPool`, `.get_alias`, `ContextualAttribute`, `SupervisorInterface`, `TaskThreadingPolicy`, `.resolve_primitive`, `Supervisor`, `CoreApplication`, `ServiceProvider`, `.resolve`, `BoundMethod`, `TaskRuntime`, `HttpServiceProvider`, `Exception`?**
  _High betweenness centrality (0.154) - this node is a cross-community bridge._
- **Why does `TaskRuntimeInterface` connect `TaskRuntimeInterface` to `ArmaReforgerServerExecutable`, `AuthManager`, `Protocol`, `RestartPolicy`, `task.py`, `HealthStatus`, `TaskInjector`, `TaskInterface`, `TaskBuilderInterface`, `TaskGraph`?**
  _High betweenness centrality (0.101) - this node is a cross-community bridge._
- **Are the 29 inferred relationships involving `InstanceContainer` (e.g. with `._is_container_type()` and `BoundMethod`) actually correct?**
  _`InstanceContainer` has 29 INFERRED edges - model-reasoned connections that need verification._
- **Are the 10 inferred relationships involving `ArmaReforgerServerExecutable` (e.g. with `ArmaReforgerServer` and `ArmaReforgerServerError`) actually correct?**
  _`ArmaReforgerServerExecutable` has 10 INFERRED edges - model-reasoned connections that need verification._
- **Are the 16 inferred relationships involving `Supervisor` (e.g. with `.register_base_bindings()` and `InstanceContainer`) actually correct?**
  _`Supervisor` has 16 INFERRED edges - model-reasoned connections that need verification._
- **Are the 9 inferred relationships involving `CoreApplication` (e.g. with `InstanceContainer` and `ServiceProvider`) actually correct?**
  _`CoreApplication` has 9 INFERRED edges - model-reasoned connections that need verification._