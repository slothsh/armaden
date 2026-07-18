# Graph Report - feature-filesystem-storage-worktree  (2026-07-18)

## Corpus Check
- 198 files · ~36,569 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1880 nodes · 3525 edges · 313 communities (59 shown, 254 thin omitted)
- Extraction: 77% EXTRACTED · 23% INFERRED · 0% AMBIGUOUS · INFERRED: 812 edges (avg confidence: 0.55)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `ce38332f`
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
- .resolve
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
- Message
- Task
- RouteGroup
- TaskBuilderInterface
- TaskRuntime
- TypedDict
- get_application
- AppServiceProvider
- URL
- Dictionary
- CommandRequestPacket
- ArmaDen
- DatagramTransportInterface
- Bind
- RconCommandInterface
- RconCommandArgumentError
- PlayerResponseData
- Application
- task.py
- LoginResponsePacket
- ServerMessageResponsePacket
- .resolve_primitive
- .kind
- .addon
- .addons_verify
- .ai_limit
- RouteCompiler
- .backend_local_storage
- Exception
- get_application
- .freeze_check
- Kernel
- .jobsys_short_worker_count
- SteamCmdExecutableError
- LifecycleController
- .log_append
- api.py
- .log_scr_checksum
- ConsoleServiceProvider
- .minidump
- .no_splash
- .player_limits
- .backend_fresh_session
- .scenario
- .server_id
- AppServiceProvider
- .single_threaded_update
- ArmaReforgerExecutableFlag
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
- .ai_partial_sim
- __init__.py
- __init__.py
- .auto_reload
- .cfg
- .create_db
- .debugger
- __init__.py
- .disable_navmesh_streaming
- .custom
- .freeze_check
- api.py
- .disable_crash_reporter
- .disable_shaders_build
- .disable_shaders_build
- .enable_night_grain
- .force_session_load
- .freeze_check_mode
- .jobsys_long_worker_count
- .keep_num_of_logs
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
- .staggering_budget
- Future
- Self
- NextCallable
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
- Any
- Path
- Result
- AbstractEventLoop
- Any
- AsyncStreamCallback
- Future
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
- Future
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
- ArmaReforgerServerConfig
- .keep_num_of_logs
- .no_throw
- .server_id
- .generate_shaders
- .keep_crash_files
- .keep_session_save
- .freeze_check_mode
- .load_session_save
- .log_level
- .log_scr_checksum
- .limit_fps
- .log_time
- .log_stats
- .no_sound
- .no_splash
- .language
- .nwk_resolution
- .player_limits
- .load_session_save
- .log_append
- .logs_dir
- .server_world
- .log_level
- .streaming_budget
- .no_splash
- TypedDict
- Executable
- .profile
- .rpl_encode_as_long_jobs
- Future
- .log_voting
- .script_authorize_all
- .staggering_budget
- .nds
- .addons
- Any
- .no_backend
- CommandResponse
- Any
- RconCommandInterface
- .log_fs
- .region
- .scenario
- .streaming_budget
- RconCommandRepository
- async_datagram_transport.py
- .silent_crash_report
- .single_threaded_update
- .world
- .streams_delta
- .log_rdb_checksum

## God Nodes (most connected - your core abstractions)
1. `InstanceContainer` - 129 edges
2. `ArmaReforgerServerExecutable` - 92 edges
3. `Supervisor` - 53 edges
4. `Request` - 49 edges
5. `CoreApplication` - 48 edges
6. `BattleEyeRconClient` - 44 edges
7. `RconCommandInterface` - 43 edges
8. `app()` - 41 edges
9. `S3Filesystem` - 35 edges
10. `LocalFilesystem` - 35 edges

## Surprising Connections (you probably didn't know these)
- `AppServiceProvider` --uses--> `ServiceProvider`  [INFERRED]
  user/app/providers/app_service_provider.py → src/armaden/framework/classes/service_provider.py
- `TelemetryServiceProvider` --uses--> `ServiceProvider`  [INFERRED]
  user/app/providers/telemetry_service_provider.py → src/armaden/framework/classes/service_provider.py
- `RestartAppService` --uses--> `SupervisorRequestData`  [INFERRED]
  user/app/http/actions/restart_app_service.py → src/armaden/framework/dto/supervisor_request_data.py
- `ShutdownAppService` --uses--> `SupervisorRequestData`  [INFERRED]
  user/app/http/actions/shutdown_app_service.py → src/armaden/framework/dto/supervisor_request_data.py
- `RestartRequestData` --uses--> `HealthStatus`  [INFERRED]
  user/app/http/dto/lifecycle_data.py → src/armaden/framework/enums/health_status.py

## Import Cycles
- None detected.

## Communities (313 total, 254 thin omitted)

### Community 0 - "ArmaReforgerServerExecutable"
Cohesion: 0.13
Nodes (7): ArmaReforgerServerExecutable, Bind the server to specific addresses / ports.          Keyword Args:, Configure BattlEye / RCON remote console.          Keyword Args:             add, Force loading a session save even if version mismatched., Skip the initial load request and start a brand-new session., Limit the number of streams opened for a client (1..1000)., Threads for short jobs (capped to CPU count or 16).

### Community 2 - "AuthManager"
Cohesion: 0.12
Nodes (5): LoginCommand, _Missing, RconCommandArgSpec, BanCreateCommand, KickCommand

### Community 3 - "Protocol"
Cohesion: 0.15
Nodes (3): BattleEyeRconClient, CommandResponse, Message

### Community 5 - "SteamCmdExecutable"
Cohesion: 0.06
Nodes (20): Executable, SupervisorRequestArgs, A2SConfig, GameConfig, GamePropertiesConfig, GamePropertiesPersistence, JoinQueueConfig, ModConfig (+12 more)

### Community 7 - "lifecycle_controller.py"
Cohesion: 0.06
Nodes (15): HealthStatus, DefaultApi, DefaultApiError, GetAppStatus, Api, Controllers for API routes, LifecycleController, ApiResponseData (+7 more)

### Community 8 - "TaskThreadingPolicy"
Cohesion: 0.05
Nodes (19): APIRouter, HttpKernel, Middleware, MiddlewarePipeline, RouteCompiler, RouteParameter, ApiUser, AuthManager (+11 more)

### Community 9 - "RouteFacade"
Cohesion: 0.15
Nodes (4): Mixin adding registered RCON command dispatch to any client that     exposes a `, RegisteredRconClient, SendCommandProtocol, RconCommandArgumentError

### Community 11 - "CoreApplication"
Cohesion: 0.05
Nodes (8): ErrorInterface, Filesystem, Result, ServiceProvider, LocalFilesystem, S3Filesystem, Filesystem, FilesystemServiceProvider

### Community 12 - "HealthStatus"
Cohesion: 0.22
Nodes (3): Lifecycle, Pipeline, TaskRuntimeInterface

### Community 14 - "app"
Cohesion: 0.09
Nodes (3): config(), get_application(), app()

### Community 15 - "Packet"
Cohesion: 0.14
Nodes (10): Generator, GeneratorResult, _detect_poetry_package_path(), _fmt_list(), main(), _print_result(), # TODO: Register bindings on the service container., # TODO: Build and register tasks with the supervisor. (+2 more)

### Community 16 - "ConsoleKernel"
Cohesion: 0.14
Nodes (8): set_application(), bootstrap_console(), bootstrap_http(), ConsoleKernel, HttpKernel, Kernel, RuntimeEntry, TypedResult

### Community 17 - ".generate"
Cohesion: 0.11
Nodes (8): BanListCommand, BanRemoveCommand, IdCommand, LogoutCommand, PlayersCommand, RestartCommand, RolesCommand, ShutdownCommand

### Community 18 - "ServiceProvider"
Cohesion: 0.21
Nodes (11): Configurable, _resolve_config_type(), Dictionary, Config, RegistersRconCommand, ArmaReforgerRconClient, High-level RCON client for Arma Reforger.      Command registration, dispatch, a, ArmaReforgerServerError (+3 more)

### Community 20 - "TaskRuntimeInterface"
Cohesion: 0.19
Nodes (8): Application, DefaultApplication, ConsoleServiceProvider, ApplicationError, ApplicationException, ApplicationStatus, RconServiceProvider, HttpServiceProvider

### Community 22 - "BoundMethod"
Cohesion: 0.11
Nodes (3): KeepAlivePacket, BattleEyeInvalidPacketException, ServerMessageResponsePacket

### Community 23 - "TaskGraph"
Cohesion: 0.19
Nodes (6): DuplicateTaskNameError, TaskGraphCycleError, UnresolvedDependencyError, TaskGraph, TaskGraphCompiler, _UnresolvedSentinel

### Community 24 - "AsyncDatagramTransport"
Cohesion: 0.13
Nodes (12): DatagramProtocol, DatagramTransport, entry(), main(), ClientStatus, _PendingCommand, ServerMessage, CommandHeader (+4 more)

### Community 28 - "HttpServiceProvider"
Cohesion: 0.18
Nodes (5): GraphTaskRuntime, _result_error(), _run_shutdown(), WorkerPool, Semaphore

### Community 29 - "TaskRuntime"
Cohesion: 0.15
Nodes (4): Event, ProgressChannel, ProgressUpdate, TaskRuntime

### Community 35 - "RestartPolicy"
Cohesion: 0.24
Nodes (7): RestartPolicy, _emit_banner(), TelemetryServiceProvider, CollectServerTelemetryTask, FormatTelemetryReportTask, TelemetryAlertTask, TelemetryReadinessProbeTask

### Community 36 - "env"
Cohesion: 0.14
Nodes (5): config(), env(), Facade for reading typed environment variables from the application., config(), config()

### Community 38 - "ContextualAttribute"
Cohesion: 0.15
Nodes (5): Config, Give, register_builtin_attributes(), Tag, ContextualAttribute

### Community 39 - "SupervisorInterface"
Cohesion: 0.11
Nodes (4): ApplicationBase, Application, Application, SupervisorInterface

### Community 42 - "RouteRegistrar"
Cohesion: 0.08
Nodes (8): route(), URL, RequestContext, RouteNotFoundException, RouteParameterMissingException, UrlGenerator, auth(), request()

### Community 43 - "CommandResponse"
Cohesion: 0.21
Nodes (3): RequestMessage, LoginRequestPacket, UnknownPacket

### Community 47 - "SubprocessHandle"
Cohesion: 0.16
Nodes (21): SupervisorRequestData, SupervisorRequestKind, TaskThreadingPolicy, SupervisorRequestInterface, _ExclusiveWorker, ProcessInfoData, RequestInfoData, _SharedWorker (+13 more)

### Community 49 - "Message"
Cohesion: 0.26
Nodes (4): DiscoveryHook, TypeDiscoveryError, TypeDiscoveryServiceProvider, MultiImplementation

### Community 57 - "get_application"
Cohesion: 0.11
Nodes (8): Error, ErrorKindInterface, Enforces that any error type object has a code string and message string., Accepts any Enum instance that implements a .message property., ModuleLoader, ModuleLoaderError, providers(), ModuleType

### Community 59 - "URL"
Cohesion: 0.18
Nodes (4): ErrorInterface, KernelInterface, RconPacketInterface, Protocol

### Community 62 - "ArmaDen"
Cohesion: 0.22
Nodes (8): ArmaDen, Build Locally, CLI Entrypoints, Install, Manual Application Setup, Packages, Run with Docker, Scaffold an Application

### Community 65 - "RconCommandInterface"
Cohesion: 0.13
Nodes (4): ABC, Controller, DeferrableProvider, ServiceProvider

### Community 69 - "Application"
Cohesion: 0.36
Nodes (5): json_response(), JSONResponse, response(), ResponseFactory, StarletteJSONResponse

### Community 71 - "LoginResponsePacket"
Cohesion: 0.33
Nodes (3): PlayerResponseData, Parse a single data row from ``players`` output.          Returns ``None``  if t, A connected player returned by the ``players`` command.

### Community 73 - ".resolve_primitive"
Cohesion: 0.11
Nodes (12): BoundMethod, get_class_for_callable(), get_contextual_attribute_from_dependency(), is_parameter_required(), Utility helpers shared between the container and bound-method resolution., Determine the class name associated with a callable for build-stack tracking., resolve_string_to_class(), unwrap_if_closure() (+4 more)

### Community 75 - ".addon"
Cohesion: 0.15
Nodes (7): BattleEyeRconServer, Client, ClientState, ResponseMessage, LoginStatus, LoginResponsePacket, IntEnum

### Community 84 - "Kernel"
Cohesion: 0.25
Nodes (3): Bind, Scoped, Singleton

### Community 101 - "ArmaReforgerExecutableFlag"
Cohesion: 0.33
Nodes (3): ArmaReforgerExecutableFlag, ArmaReforgerExecutableFlagError, Arma Reforger CLI startup flags.

### Community 125 - "AbstractEventLoop"
Cohesion: 0.33
Nodes (5): MANDATORY: Code Comment Conventions, MANDATORY: Git Rules, MANDATORY: Local Code Search/Traversal, MANDATORY: Use td for Task Management, MANDATORY: Worktree Management

## Knowledge Gaps
- **14 isolated node(s):** `armaden`, `ApiResponseData`, `MANDATORY: Local Code Search/Traversal`, `MANDATORY: Use td for Task Management`, `MANDATORY: Worktree Management` (+9 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **254 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ArmaReforgerServerExecutable` connect `ArmaReforgerServerExecutable` to `SteamCmdExecutable`, `.keep_num_of_logs`, `.no_throw`, `.server_id`, `.generate_shaders`, `.keep_session_save`, `HealthStatus`, `.freeze_check_mode`, `.load_session_save`, `.log_scr_checksum`, `.limit_fps`, `.log_time`, `ServiceProvider`, `.log_stats`, `.no_sound`, `.language`, `.nwk_resolution`, `Exception`, `.load_session_save`, `.log_append`, `.logs_dir`, `.server_world`, `.log_level`, `.no_splash`, `.ai_partial_sim`, `__init__.py`, `__init__.py`, `.auto_reload`, `.cfg`, `.create_db`, `.debugger`, `.log_voting`, `.disable_navmesh_streaming`, `.addons`, `.custom`, `.freeze_check`, `.disable_crash_reporter`, `.disable_shaders_build`, `CommandResponse`, `.log_fs`, `.nds`, `.no_backend`, `.profile`, `.region`, `.scenario`, `TaskBuilder`, `TypedDict`, `.rpl_encode_as_long_jobs`, `.streams_delta`, `.log_rdb_checksum`, `.silent_crash_report`, `.single_threaded_update`, `.world`, `.script_authorize_all`, `__init__.py`, `.staggering_budget`, `.kind`, `.addons_verify`, `.ai_limit`, `.backend_local_storage`, `.freeze_check`, `.jobsys_short_worker_count`, `.log_append`, `api.py`, `.log_scr_checksum`, `ConsoleServiceProvider`, `.minidump`, `.player_limits`, `.backend_fresh_session`, `.scenario`, `.server_id`, `AppServiceProvider`, `.single_threaded_update`, `.streaming_budget`?**
  _High betweenness centrality (0.172) - this node is a cross-community bridge._
- **Why does `InstanceContainer` connect `InstanceContainer` to `WorkerPool`, `.get_alias`, `RconCommandInterface`, `ContextualAttribute`, `SupervisorInterface`, `BattleEyeRconServer`, `.resolve_primitive`, `BattleEyeRconClient`, `SubprocessHandle`, `Exception`, `Message`, `.resolve`, `Kernel`, `TaskRuntimeInterface`, `TaskInterface`, `HttpServiceProvider`?**
  _High betweenness centrality (0.119) - this node is a cross-community bridge._
- **Why does `Filesystem` connect `CoreApplication` to `RconCommandInterface`?**
  _High betweenness centrality (0.111) - this node is a cross-community bridge._
- **Are the 31 inferred relationships involving `InstanceContainer` (e.g. with `Application` and `Config`) actually correct?**
  _`InstanceContainer` has 31 INFERRED edges - model-reasoned connections that need verification._
- **Are the 11 inferred relationships involving `ArmaReforgerServerExecutable` (e.g. with `Executable` and `Dictionary`) actually correct?**
  _`ArmaReforgerServerExecutable` has 11 INFERRED edges - model-reasoned connections that need verification._
- **Are the 16 inferred relationships involving `Supervisor` (e.g. with `SupervisorRequestData` and `SupervisorRequestKind`) actually correct?**
  _`Supervisor` has 16 INFERRED edges - model-reasoned connections that need verification._
- **What connects `armaden`, `Mixin adding registered RCON command dispatch to any client that     exposes a ``, `Accepts any Enum instance that implements a .message property.` to the rest of the system?**
  _107 weakly-connected nodes found - possible documentation gaps or missing edges._