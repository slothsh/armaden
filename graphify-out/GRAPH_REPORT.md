# Graph Report - feature-filesystem-storage-worktree  (2026-07-18)

## Corpus Check
- 202 files · ~37,948 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1950 nodes · 3635 edges · 322 communities (67 shown, 255 thin omitted)
- Extraction: 79% EXTRACTED · 21% INFERRED · 0% AMBIGUOUS · INFERRED: 758 edges (avg confidence: 0.55)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `2d6c3a82`
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
- Message
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
- Dictionary
- CommandRequestPacket
- ArmaDen
- DatagramTransportInterface
- Bind
- RconCommandInterface
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
- .log_append
- api.py
- .log_scr_checksum
- .minidump
- .player_limits
- .backend_fresh_session
- .scenario
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
- FilesystemServiceProvider
- .a2s
- .cfg
- .create_db
- .addon
- __init__.py
- .addon_download_dir
- .addon_temp_dir
- .addons
- api.py
- .disable_crash_reporter
- .addons_dir
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
- .addons_repair
- .addons_verify
- .server_id
- .generate_shaders
- .keep_crash_files
- .ai_partial_sim
- .auto_reload
- .backend_disable_storage
- .log_level
- .backend_local_storage
- .check_instance
- .log_time
- .custom
- .no_sound
- .no_splash
- .debugger
- .disable_ai
- .player_limits
- .load_session_save
- .disable_navmesh_streaming
- .logs_dir
- .disable_shaders_build
- .enable_night_grain
- .streaming_budget
- .freeze_check
- .freeze_check_mode
- Executable
- .profile
- .jobsys_long_worker_count
- Future
- .keep_crash_files
- .script_authorize_all
- .keep_num_of_logs
- .keep_session_save
- .language
- Any
- .limit_fps
- .list_scenarios
- Any
- RconCommandInterface
- .log_append
- .log_fs
- .log_level
- .log_rdb_checksum
- RconCommandRepository
- async_datagram_transport.py
- .log_scr_checksum
- .log_stats
- .log_voting
- .minidump
- .nds
- .no_backend
- .no_splash
- .no_throw
- .nwk_resolution
- .player_limits
- .region
- .rpl_encode_as_long_jobs
- .scenario
- .server_world
- .silent_crash_report
- .single_threaded_update
- .staggering_budget
- .streaming_budget
- .vm_error_mode
- .world

## God Nodes (most connected - your core abstractions)
1. `InstanceContainer` - 123 edges
2. `ArmaReforgerServerExecutable` - 92 edges
3. `Supervisor` - 52 edges
4. `Request` - 49 edges
5. `BattleEyeRconClient` - 44 edges
6. `RconCommandInterface` - 43 edges
7. `app()` - 41 edges
8. `CacheProtocol` - 36 edges
9. `S3Filesystem` - 35 edges
10. `LocalFilesystem` - 35 edges

## Surprising Connections (you probably didn't know these)
- `AppServiceProvider` --uses--> `ServiceProvider`  [INFERRED]
  user/app/providers/app_service_provider.py → src/armaden/framework/classes/service_provider.py
- `TelemetryServiceProvider` --uses--> `ServiceProvider`  [INFERRED]
  user/app/providers/telemetry_service_provider.py → src/armaden/framework/classes/service_provider.py
- `RestartRequestData` --uses--> `HealthStatus`  [INFERRED]
  user/app/http/dto/lifecycle_data.py → src/armaden/framework/enums/health_status.py
- `ServiceHealthData` --uses--> `HealthStatus`  [INFERRED]
  user/app/http/dto/lifecycle_data.py → src/armaden/framework/enums/health_status.py
- `ShutdownRequestData` --uses--> `HealthStatus`  [INFERRED]
  user/app/http/dto/lifecycle_data.py → src/armaden/framework/enums/health_status.py

## Import Cycles
- None detected.

## Communities (322 total, 255 thin omitted)

### Community 0 - "ArmaReforgerServerExecutable"
Cohesion: 0.13
Nodes (7): ArmaReforgerServerExecutable, Bind the server to specific addresses / ports.          Keyword Args:, Configure BattlEye / RCON remote console.          Keyword Args:             add, Force loading a session save even if version mismatched., Skip the initial load request and start a brand-new session., Limit the number of streams opened for a client (1..1000)., Threads for short jobs (capped to CPU count or 16).

### Community 2 - "AuthManager"
Cohesion: 0.12
Nodes (5): LoginCommand, _Missing, RconCommandArgSpec, BanCreateCommand, BanRemoveCommand

### Community 3 - "Protocol"
Cohesion: 0.15
Nodes (3): BattleEyeRconClient, CommandResponse, Message

### Community 5 - "SteamCmdExecutable"
Cohesion: 0.06
Nodes (19): Executable, A2SConfig, GameConfig, GamePropertiesConfig, GamePropertiesPersistence, JoinQueueConfig, ModConfig, OperatingConfig (+11 more)

### Community 6 - "BattleEyeRconServer"
Cohesion: 0.10
Nodes (6): AbstractEventLoop, InstanceContainer, ServiceProvider, ApplicationException, CoreApplication, SupervisorInterface

### Community 7 - "lifecycle_controller.py"
Cohesion: 0.05
Nodes (23): HealthStatus, GenericError, DefaultApiError, ArmaReforgerExecutableFlag, ArmaReforgerExecutableFlagError, Arma Reforger CLI startup flags., SteamCMD CLI command flags (prefixed with ``+``)., SteamCmdExecutableFlag (+15 more)

### Community 8 - "TaskThreadingPolicy"
Cohesion: 0.06
Nodes (17): HttpKernel, Middleware, MiddlewarePipeline, DefaultApi, ApiUser, AuthManager, Authenticate, AuthenticateWithBasic (+9 more)

### Community 9 - "RouteFacade"
Cohesion: 0.15
Nodes (4): Mixin adding registered RCON command dispatch to any client that     exposes a `, RegisteredRconClient, SendCommandProtocol, RconCommandArgumentError

### Community 13 - "BattleEyeRconClient"
Cohesion: 0.12
Nodes (5): GraphTaskRuntime, _result_error(), _run_shutdown(), Supervisor, Semaphore

### Community 14 - "app"
Cohesion: 0.08
Nodes (4): config(), get_application(), app(), AppServiceProvider

### Community 15 - "Packet"
Cohesion: 0.14
Nodes (10): Generator, GeneratorResult, _detect_poetry_package_path(), _fmt_list(), main(), _print_result(), # TODO: Register bindings on the service container., # TODO: Build and register tasks with the supervisor. (+2 more)

### Community 16 - "ConsoleKernel"
Cohesion: 0.12
Nodes (9): set_application(), bootstrap_console(), bootstrap_http(), ConsoleKernel, HttpKernel, Kernel, RuntimeEntry, ConsoleServiceProvider (+1 more)

### Community 17 - ".generate"
Cohesion: 0.11
Nodes (8): BanListCommand, IdCommand, KickCommand, LogoutCommand, PlayersCommand, RestartCommand, RolesCommand, ShutdownCommand

### Community 18 - "ServiceProvider"
Cohesion: 0.22
Nodes (10): Configurable, Dictionary, Config, RegistersRconCommand, ArmaReforgerRconClient, High-level RCON client for Arma Reforger.      Command registration, dispatch, a, ArmaReforgerServerError, ArmaReforgerServerException (+2 more)

### Community 20 - "TaskRuntimeInterface"
Cohesion: 0.15
Nodes (5): Application, ApplicationBase, Application, DefaultApplication, Application

### Community 22 - "BoundMethod"
Cohesion: 0.11
Nodes (3): KeepAlivePacket, BattleEyeInvalidPacketException, ServerMessageResponsePacket

### Community 23 - "TaskGraph"
Cohesion: 0.19
Nodes (7): DuplicateTaskNameError, TaskGraphCycleError, UnresolvedDependencyError, TaskGraph, TaskGraphCompiler, TaskGraphState, _UnresolvedSentinel

### Community 24 - "AsyncDatagramTransport"
Cohesion: 0.13
Nodes (12): DatagramProtocol, DatagramTransport, entry(), main(), ClientStatus, _PendingCommand, ServerMessage, CommandHeader (+4 more)

### Community 25 - "UrlGenerator"
Cohesion: 0.09
Nodes (3): __getattr__(), _LegacyTask, TaskBuilder

### Community 26 - "Path"
Cohesion: 0.12
Nodes (3): Any, ErrorInterface, CacheProtocol

### Community 28 - "HttpServiceProvider"
Cohesion: 0.20
Nodes (6): TaskThreadingPolicy, _ExclusiveWorker, _SharedWorker, _WorkerBase, WorkerPool, String

### Community 29 - "TaskRuntime"
Cohesion: 0.15
Nodes (4): Event, ProgressChannel, ProgressUpdate, TaskRuntime

### Community 35 - "RestartPolicy"
Cohesion: 0.14
Nodes (8): RestartPolicy, TaskRuntimeInterface, _emit_banner(), TelemetryServiceProvider, CollectServerTelemetryTask, FormatTelemetryReportTask, TelemetryAlertTask, TelemetryReadinessProbeTask

### Community 36 - "env"
Cohesion: 0.14
Nodes (5): config(), env(), Facade for reading typed environment variables from the application., config(), config()

### Community 38 - "ContextualAttribute"
Cohesion: 0.16
Nodes (4): Config, Give, Tag, ContextualAttribute

### Community 42 - "RouteRegistrar"
Cohesion: 0.08
Nodes (8): route(), URL, RequestContext, RouteNotFoundException, RouteParameterMissingException, UrlGenerator, auth(), request()

### Community 43 - "CommandResponse"
Cohesion: 0.21
Nodes (3): RequestMessage, LoginRequestPacket, UnknownPacket

### Community 47 - "SubprocessHandle"
Cohesion: 0.13
Nodes (6): SupervisorRequestInterface, ProcessInfoData, TaskRuntime, TaskStateData, ProcessFacade, ScheduleFacade

### Community 49 - "Message"
Cohesion: 0.26
Nodes (4): DiscoveryHook, TypeDiscoveryError, TypeDiscoveryServiceProvider, MultiImplementation

### Community 53 - "TaskInterface"
Cohesion: 0.25
Nodes (4): APIRouter, RouteCompiler, RouteParameter, HttpKernel

### Community 57 - "get_application"
Cohesion: 0.20
Nodes (4): ModuleLoader, ModuleLoaderError, providers(), ModuleType

### Community 59 - "URL"
Cohesion: 0.18
Nodes (4): ErrorInterface, KernelInterface, RconPacketInterface, Protocol

### Community 60 - "Dictionary"
Cohesion: 0.26
Nodes (3): Lifecycle, Pipeline, TaskInjector

### Community 62 - "ArmaDen"
Cohesion: 0.22
Nodes (8): ArmaDen, Build Locally, CLI Entrypoints, Install, Manual Application Setup, Packages, Run with Docker, Scaffold an Application

### Community 69 - "Application"
Cohesion: 0.36
Nodes (5): json_response(), JSONResponse, response(), ResponseFactory, StarletteJSONResponse

### Community 71 - "LoginResponsePacket"
Cohesion: 0.33
Nodes (3): PlayerResponseData, Parse a single data row from ``players`` output.          Returns ``None``  if t, A connected player returned by the ``players`` command.

### Community 73 - ".resolve_primitive"
Cohesion: 0.13
Nodes (9): BoundMethod, get_class_for_callable(), get_contextual_attribute_from_dependency(), get_parameter_class_name(), is_parameter_required(), Utility helpers shared between the container and bound-method resolution., Determine the class name associated with a callable for build-stack tracking., resolve_string_to_class() (+1 more)

### Community 74 - ".kind"
Cohesion: 0.29
Nodes (4): Error, ErrorKindInterface, Enforces that any error type object has a code string and message string., Accepts any Enum instance that implements a .message property.

### Community 75 - ".addon"
Cohesion: 0.15
Nodes (7): BattleEyeRconServer, Client, ClientState, ResponseMessage, LoginStatus, LoginResponsePacket, IntEnum

### Community 82 - "get_application"
Cohesion: 0.25
Nodes (7): SupervisorRequestArgs, SupervisorRequestData, SupervisorRequestKind, RequestInfoData, SupervisorError, RestartAppService, ShutdownAppService

### Community 84 - "Kernel"
Cohesion: 0.25
Nodes (3): Bind, Scoped, Singleton

### Community 89 - ".log_append"
Cohesion: 0.29
Nodes (4): CircularDependencyException, EntryNotFoundException, LogicException, SelfBuilding

### Community 95 - ".player_limits"
Cohesion: 0.27
Nodes (4): TaskRecord, ThreadInfoData, TaskError, PolicyEngine

### Community 125 - "AbstractEventLoop"
Cohesion: 0.33
Nodes (5): MANDATORY: Code Comment Conventions, MANDATORY: Git Rules, MANDATORY: Local Code Search/Traversal, MANDATORY: Use td for Task Management, MANDATORY: Worktree Management

## Knowledge Gaps
- **14 isolated node(s):** `armaden`, `ApiResponseData`, `MANDATORY: Local Code Search/Traversal`, `MANDATORY: Use td for Task Management`, `MANDATORY: Worktree Management` (+9 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **255 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ArmaReforgerServerExecutable` connect `ArmaReforgerServerExecutable` to `SteamCmdExecutable`, `.addons_repair`, `.addons_verify`, `.server_id`, `.generate_shaders`, `.ai_partial_sim`, `.auto_reload`, `.backend_disable_storage`, `.backend_local_storage`, `.check_instance`, `.log_time`, `ServiceProvider`, `.custom`, `.no_sound`, `.debugger`, `.disable_ai`, `.load_session_save`, `.disable_navmesh_streaming`, `.logs_dir`, `.disable_shaders_build`, `.enable_night_grain`, `.freeze_check`, `.freeze_check_mode`, `.profile`, `.a2s`, `RestartPolicy`, `.cfg`, `.addon`, `.create_db`, `.addon_download_dir`, `.addon_temp_dir`, `.addons`, `.jobsys_long_worker_count`, `.disable_crash_reporter`, `.addons_dir`, `.keep_crash_files`, `.keep_num_of_logs`, `.keep_session_save`, `.language`, `.limit_fps`, `.list_scenarios`, `.log_append`, `TaskBuilder`, `.log_fs`, `.log_level`, `.log_rdb_checksum`, `.log_scr_checksum`, `.log_stats`, `.log_voting`, `.minidump`, `.nds`, `.no_backend`, `.no_splash`, `.no_throw`, `.nwk_resolution`, `.player_limits`, `.region`, `.rpl_encode_as_long_jobs`, `__init__.py`, `.scenario`, `.script_authorize_all`, `.server_world`, `.silent_crash_report`, `.single_threaded_update`, `.staggering_budget`, `.streaming_budget`, `.vm_error_mode`, `.world`, `.backend_local_storage`, `PlayerResponseData`, `.jobsys_short_worker_count`, `api.py`, `.log_scr_checksum`, `.backend_fresh_session`?**
  _High betweenness centrality (0.149) - this node is a cross-community bridge._
- **Why does `InstanceContainer` connect `InstanceContainer` to `WorkerPool`, `.get_alias`, `RconCommandArgumentError`, `RconCommandInterface`, `ContextualAttribute`, `.resolve_primitive`, `BattleEyeRconClient`, `SubprocessHandle`, `Exception`, `get_application`, `Message`, `TaskRuntimeInterface`, `Kernel`, `.resolve`, `.log_append`, `HttpServiceProvider`, `.player_limits`?**
  _High betweenness centrality (0.104) - this node is a cross-community bridge._
- **Why does `CacheProtocol` connect `Path` to `ServerMessageResponsePacket`?**
  _High betweenness centrality (0.091) - this node is a cross-community bridge._
- **Are the 25 inferred relationships involving `InstanceContainer` (e.g. with `Application` and `Config`) actually correct?**
  _`InstanceContainer` has 25 INFERRED edges - model-reasoned connections that need verification._
- **Are the 11 inferred relationships involving `ArmaReforgerServerExecutable` (e.g. with `Executable` and `Dictionary`) actually correct?**
  _`ArmaReforgerServerExecutable` has 11 INFERRED edges - model-reasoned connections that need verification._
- **Are the 15 inferred relationships involving `Supervisor` (e.g. with `SupervisorRequestData` and `SupervisorRequestKind`) actually correct?**
  _`Supervisor` has 15 INFERRED edges - model-reasoned connections that need verification._
- **What connects `armaden`, `Mixin adding registered RCON command dispatch to any client that     exposes a ``, `Accepts any Enum instance that implements a .message property.` to the rest of the system?**
  _107 weakly-connected nodes found - possible documentation gaps or missing edges._