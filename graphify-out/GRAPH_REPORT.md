# Graph Report - armaden  (2026-07-11)

## Corpus Check
- 168 files · ~31,703 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1647 nodes · 3171 edges · 196 communities (67 shown, 129 thin omitted)
- Extraction: 83% EXTRACTED · 17% INFERRED · 0% AMBIGUOUS · INFERRED: 554 edges (avg confidence: 0.56)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `5706f866`
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
- .disable_crash_reporter
- .disable_navmesh_streaming
- .disable_shaders_build
- .enable_night_grain
- .force_session_load
- .freeze_check_mode
- .jobsys_long_worker_count
- .keep_num_of_logs
- .keep_session_save
- .language
- .log_level
- .log_rdb_checksum
- .log_stats
- .log_voting
- .nds
- .no_backend
- .no_sound
- .no_throw
- .nwk_resolution
- .rpl_encode_as_long_jobs
- .rpl_timeout_ms
- .staggering_budget
- .streams_delta
- Future
- Self

## God Nodes (most connected - your core abstractions)
1. `InstanceContainer` - 119 edges
2. `ArmaReforgerServerExecutable` - 94 edges
3. `Request` - 58 edges
4. `CoreApplication` - 47 edges
5. `BattleEyeRconClient` - 46 edges
6. `app()` - 42 edges
7. `Supervisor` - 39 edges
8. `SupervisorInterface` - 36 edges
9. `TaskRuntimeInterface` - 33 edges
10. `Packet` - 31 edges

## Surprising Connections (you probably didn't know these)
- `Application` --uses--> `Application`  [INFERRED]
  user/bootstrap/application.py → src/armaden/framework/application.py
- `AppServiceProvider` --uses--> `ServiceProvider`  [INFERRED]
  user/app/providers/app_service_provider.py → src/armaden/framework/classes/service_provider.py
- `TelemetryServiceProvider` --uses--> `ServiceProvider`  [INFERRED]
  user/app/providers/telemetry_service_provider.py → src/armaden/framework/classes/service_provider.py
- `ServiceHealthData` --uses--> `HealthStatus`  [INFERRED]
  user/app/http/dto/lifecycle_data.py → src/armaden/framework/enums/health_status.py
- `CollectServerTelemetryTask` --uses--> `TaskRuntimeInterface`  [INFERRED]
  user/app/tasks/telemetry_tasks.py → src/armaden/framework/protocols/task_runtime.py

## Import Cycles
- None detected.

## Communities (196 total, 129 thin omitted)

### Community 0 - "ArmaReforgerServerExecutable"
Cohesion: 0.07
Nodes (14): ArmaReforgerServerExecutable, Bind the server to specific addresses / ports.          Keyword Args:, Configure BattlEye / RCON remote console.          Keyword Args:             add, Cap the server frame rate., Load a server-side addon (mod) by ID.          May be called multiple times to l, Server region tag (used by the server browser)., Skip the initial load request and start a brand-new session., Maximum players per faction (``FactionKey:Number`` pairs). (+6 more)

### Community 2 - "AuthManager"
Cohesion: 0.07
Nodes (18): ApiUser, AuthManager, Authenticate, AuthenticateWithBasic, AuthenticateWithHeader, AuthenticateWithToken, ConfigUserProvider, AuthGuard (+10 more)

### Community 3 - "Protocol"
Cohesion: 0.19
Nodes (5): ErrorInterface, CoreApplicationInterface, KernelInterface, Any, Result

### Community 5 - "SteamCmdExecutable"
Cohesion: 0.07
Nodes (15): Executable, Path, PushValue, Result, Self, SteamCMD CLI command flags (prefixed with ``+``)., SteamCmdExecutableFlag, SteamCmd — Python wrapper for the steamcmd CLI tool. (+7 more)

### Community 6 - "BattleEyeRconServer"
Cohesion: 0.10
Nodes (13): IntEnum, BattleEyeRconServer, Client, ClientState, AbstractEventLoop, DatagramTransportFactory, datetime, Exception (+5 more)

### Community 7 - "lifecycle_controller.py"
Cohesion: 0.08
Nodes (21): DefaultApi, DefaultApiError, SupervisorRequestArgs, SupervisorRequestData, HealthStatus, SupervisorRequestKind, GetAppStatus, RestartAppService (+13 more)

### Community 8 - "TaskThreadingPolicy"
Cohesion: 0.18
Nodes (5): Protocol, Any, StrEnum, SupervisorRequestInterface, RconPacketInterface

### Community 9 - "RouteFacade"
Cohesion: 0.05
Nodes (14): APIRouter, Any, Route, RouteCompiler, Any, RouteFacade, GroupState, Any (+6 more)

### Community 10 - "Supervisor"
Cohesion: 0.13
Nodes (7): InstanceContainer, Self, AbstractEventLoop, Supervisor, TaskRecord, ThreadInfoData, TaskInterface

### Community 12 - "HealthStatus"
Cohesion: 0.06
Nodes (33): TaskRuntimeInterface, Configurable, _resolve_config_type(), Dictionary, Any, ArmaReforgerServer, ArmaReforgerServerError, ArmaReforgerServerException (+25 more)

### Community 13 - "BattleEyeRconClient"
Cohesion: 0.11
Nodes (5): BattleEyeRconClient, AbstractEventLoop, Any, DatagramTransportFactory, Exception

### Community 14 - "app"
Cohesion: 0.07
Nodes (6): app(), AppServiceProvider, config(), Any, get_application(), T

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
Cohesion: 0.17
Nodes (4): MultiImplementation, DeferrableProvider, ServiceProvider, TypeDiscoveryServiceProvider

### Community 20 - "TaskRuntimeInterface"
Cohesion: 0.22
Nodes (4): HttpKernel, Middleware, MiddlewarePipeline, Any

### Community 21 - "route_compiler.py"
Cohesion: 0.18
Nodes (5): HttpKernel, Controller, RequestContext, Any, FastAPI

### Community 22 - "BoundMethod"
Cohesion: 0.17
Nodes (11): BoundMethod, get_class_for_callable(), get_contextual_attribute_from_dependency(), get_parameter_class_name(), is_parameter_required(), Any, Parameter, Utility helpers shared between the container and bound-method resolution. (+3 more)

### Community 23 - "TaskGraph"
Cohesion: 0.20
Nodes (6): DuplicateTaskNameError, TaskGraphCycleError, UnresolvedDependencyError, TaskGraph, TaskGraphCompiler, TaskGraphState

### Community 24 - "AsyncDatagramTransport"
Cohesion: 0.13
Nodes (10): DatagramProtocol, DatagramTransport, entry(), main(), entry(), main(), AsyncDatagramTransport, Any (+2 more)

### Community 25 - "UrlGenerator"
Cohesion: 0.10
Nodes (9): auth(), request(), Any, route(), URL, Any, RouteNotFoundException, RouteParameterMissingException (+1 more)

### Community 26 - "Path"
Cohesion: 0.09
Nodes (12): Path, Result, Path to a server configuration JSON file., Directory for profiles (saves, logs, settings).          The directory is create, Redirect log output to the given directory., Path to a session save to load on startup., Additional directories to search for mods.          Multiple directories can be, Directory where addons are downloaded. (+4 more)

### Community 27 - "CommandResponsePacket"
Cohesion: 0.20
Nodes (8): ClientStatus, Message, _PendingCommand, datetime, Future, ServerMessage, CommandHeader, CommandResponsePacket

### Community 28 - "HttpServiceProvider"
Cohesion: 0.20
Nodes (11): Application, ApplicationError, ApplicationException, ApplicationStatus, HttpServiceProvider, TypeDiscoveryError, DefaultApplication, Result (+3 more)

### Community 29 - "TaskRuntime"
Cohesion: 0.14
Nodes (6): Event, TaskRuntime, ProgressChannel, RequestInfoData, SupervisorRequestData, SupervisorRequestInterface

### Community 30 - "Exception"
Cohesion: 0.13
Nodes (11): ABC, Exception, BindingResolutionException, CircularDependencyException, ContextualAttribute, EntryNotFoundException, LogicException, SelfBuilding (+3 more)

### Community 31 - "ProcessBuilder"
Cohesion: 0.11
Nodes (3): ProcessBuilder, ProcessFacade, config()

### Community 33 - "WorkerPool"
Cohesion: 0.17
Nodes (7): _ExclusiveWorker, _result_error(), _run_shutdown(), _SharedWorker, SupervisorError, _WorkerBase, WorkerPool

### Community 35 - "RestartPolicy"
Cohesion: 0.22
Nodes (8): RestartPolicy, _emit_banner(), TelemetryServiceProvider, CollectServerTelemetryTask, FormatTelemetryReportTask, TelemetryAlertTask, TelemetryReadinessProbeTask, TaskThreadingPolicy

### Community 36 - "env"
Cohesion: 0.13
Nodes (7): config(), config(), env(), Any, Facade for reading typed environment variables from the application., config(), ArmaReforgerServerConfig

### Community 37 - "ScheduleBuilder"
Cohesion: 0.14
Nodes (3): ScheduleBuilder, _ScheduledTask, ScheduleFacade

### Community 38 - "ContextualAttribute"
Cohesion: 0.20
Nodes (6): Config, Give, Any, Parameter, register_builtin_attributes(), Tag

### Community 40 - "ApplicationInterface"
Cohesion: 0.39
Nodes (4): Any, Path, Result, RouteDiscoveryServiceProvider

### Community 41 - "RouteGroupStack"
Cohesion: 0.13
Nodes (4): AbstractEventLoop, DatagramTransportInterface, Exception, WrapperTransportInterface

### Community 42 - "RouteRegistrar"
Cohesion: 0.35
Nodes (5): GraphTaskRuntime, Semaphore, Task, TaskGraph, TaskInjector

### Community 43 - "CommandResponse"
Cohesion: 0.26
Nodes (3): ArmaReforgerRconClient, High-level RCON client for Arma Reforger with typed command methods.      Each m, CommandResponse

### Community 47 - "SubprocessHandle"
Cohesion: 0.20
Nodes (4): _ProcessTask, SubprocessHandle, TaskError, _UnresolvedSentinel

### Community 48 - "._initialize_configs"
Cohesion: 0.24
Nodes (4): providers(), ModuleType, Any, Result

### Community 49 - "TaskInjector"
Cohesion: 0.21
Nodes (3): Lifecycle, Pipeline, TaskInjector

### Community 50 - "Task"
Cohesion: 0.18
Nodes (3): PolicyEngine, Task, TaskPolicy

### Community 55 - "TaskRuntime"
Cohesion: 0.17
Nodes (5): Future, Any, Result, TaskRuntime, TaskStateData

### Community 56 - "TypedDict"
Cohesion: 0.24
Nodes (5): Error, ErrorKindInterface, Enforces that any error type object has a code string and message string., Accepts any Enum instance that implements a .message property., GenericError

### Community 60 - "JSONResponse"
Cohesion: 0.50
Nodes (3): ProcessInfoData, AsyncStreamCallback, Path

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
- **129 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ArmaReforgerServerExecutable` connect `ArmaReforgerServerExecutable` to `SteamCmdExecutable`, `HealthStatus`, `Path`, `.disable_crash_reporter`, `.disable_navmesh_streaming`, `.disable_shaders_build`, `.enable_night_grain`, `.force_session_load`, `.freeze_check_mode`, `.jobsys_long_worker_count`, `.keep_num_of_logs`, `.keep_session_save`, `.language`, `.log_level`, `.log_rdb_checksum`, `.log_stats`, `.log_voting`, `.nds`, `.no_backend`, `.no_sound`, `.no_throw`, `.nwk_resolution`, `.rpl_encode_as_long_jobs`, `.rpl_timeout_ms`, `.staggering_budget`, `.streams_delta`, `task.py`, `.kind`, `.addon`, `.addons_repair`, `.addons_verify`, `.ai_limit`, `.backend_disable_storage`, `.backend_local_storage`, `.check_instance`, `.disable_ai`, `.freeze_check`, `.generate_shaders`, `.jobsys_short_worker_count`, `.keep_crash_files`, `.limit_fps`, `.list_scenarios`, `.log_append`, `.log_fs`, `.log_scr_checksum`, `.log_time`, `.minidump`, `.no_splash`, `.player_limits`, `.region`, `.scenario`, `.server_id`, `.silent_crash_report`, `.single_threaded_update`, `.vm_error_mode`?**
  _High betweenness centrality (0.180) - this node is a cross-community bridge._
- **Why does `InstanceContainer` connect `InstanceContainer` to `Bind`, `.get_alias`, `ContextualAttribute`, `SupervisorInterface`, `.resolve_primitive`, `CoreApplication`, `ServiceProvider`, `.resolve`, `BoundMethod`, `HttpServiceProvider`, `Exception`?**
  _High betweenness centrality (0.137) - this node is a cross-community bridge._
- **Why does `SupervisorInterface` connect `SupervisorInterface` to `Protocol`, `ScheduleBuilder`, `TaskThreadingPolicy`, `CoreApplication`, `ConcurrencyFacade`, `TaskInjector`, `ServiceProvider`, `TaskInterface`, `TaskGraph`, `HttpServiceProvider`, `Exception`, `ProcessBuilder`?**
  _High betweenness centrality (0.091) - this node is a cross-community bridge._
- **Are the 17 inferred relationships involving `InstanceContainer` (e.g. with `BoundMethod` and `._is_container_type()`) actually correct?**
  _`InstanceContainer` has 17 INFERRED edges - model-reasoned connections that need verification._
- **Are the 10 inferred relationships involving `ArmaReforgerServerExecutable` (e.g. with `ArmaReforgerServer` and `ArmaReforgerServerError`) actually correct?**
  _`ArmaReforgerServerExecutable` has 10 INFERRED edges - model-reasoned connections that need verification._
- **Are the 9 inferred relationships involving `CoreApplication` (e.g. with `InstanceContainer` and `ServiceProvider`) actually correct?**
  _`CoreApplication` has 9 INFERRED edges - model-reasoned connections that need verification._
- **Are the 12 inferred relationships involving `BattleEyeRconClient` (e.g. with `ArmaReforgerRconClient` and `CommandRequestPacket`) actually correct?**
  _`BattleEyeRconClient` has 12 INFERRED edges - model-reasoned connections that need verification._