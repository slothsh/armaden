# Graph Report - feature-filesystem-storage-worktree  (2026-07-18)

## Corpus Check
- 203 files · ~39,596 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 2009 nodes · 3880 edges · 303 communities (68 shown, 235 thin omitted)
- Extraction: 80% EXTRACTED · 20% INFERRED · 0% AMBIGUOUS · INFERRED: 760 edges (avg confidence: 0.55)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `e5d8cf7e`
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
- TaskBuilder
- .log_append
- api.py
- .log_scr_checksum
- Executable
- .minidump
- DefaultApi
- .player_limits
- .backend_fresh_session
- .scenario
- LoginRequestPacket
- lifecycle_controller.py
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
- api.py
- FilesystemServiceProvider
- DefaultApplication
- .a2s
- .cfg
- .create_db
- .addon
- __init__.py
- .addon_download_dir
- .addon_temp_dir
- .addons
- api.py
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
- .generate_shaders
- .keep_crash_files
- .backend_disable_storage
- .log_level
- .backend_local_storage
- .check_instance
- .log_time
- .custom
- .no_splash
- .disable_ai
- .player_limits
- .logs_dir
- .disable_shaders_build
- .streaming_budget
- .freeze_check
- .freeze_check_mode
- Executable
- .jobsys_long_worker_count
- Future
- .script_authorize_all
- .keep_num_of_logs
- .keep_session_save
- .language
- Any
- .limit_fps
- .list_scenarios
- Any
- RconCommandInterface
- .log_fs
- .log_rdb_checksum
- RconCommandRepository
- async_datagram_transport.py
- .log_scr_checksum
- .log_stats
- .no_splash
- .nwk_resolution
- .player_limits
- .scenario
- .server_world
- .silent_crash_report
- .staggering_budget

## God Nodes (most connected - your core abstractions)
1. `InstanceContainer` - 123 edges
2. `ArmaReforgerServerExecutable` - 92 edges
3. `Supervisor` - 52 edges
4. `CacheStorageDriver` - 50 edges
5. `Request` - 49 edges
6. `BattleEyeRconClient` - 44 edges
7. `RconCommandInterface` - 43 edges
8. `app()` - 41 edges
9. `CacheProtocol` - 36 edges
10. `S3Filesystem` - 35 edges

## Surprising Connections (you probably didn't know these)
- `Application` --uses--> `Application`  [INFERRED]
  user/bootstrap/application.py → src/armaden/framework/application.py
- `AppServiceProvider` --uses--> `ServiceProvider`  [INFERRED]
  user/app/providers/app_service_provider.py → src/armaden/framework/classes/service_provider.py
- `TelemetryServiceProvider` --uses--> `ServiceProvider`  [INFERRED]
  user/app/providers/telemetry_service_provider.py → src/armaden/framework/classes/service_provider.py
- `RestartRequestData` --uses--> `HealthStatus`  [INFERRED]
  user/app/http/dto/lifecycle_data.py → src/armaden/framework/enums/health_status.py
- `ServiceHealthData` --uses--> `HealthStatus`  [INFERRED]
  user/app/http/dto/lifecycle_data.py → src/armaden/framework/enums/health_status.py

## Import Cycles
- None detected.

## Communities (303 total, 235 thin omitted)

### Community 0 - "ArmaReforgerServerExecutable"
Cohesion: 0.03
Nodes (36): ArmaReforgerServerExecutable, Path to a server configuration JSON file., Directory for profiles (saves, logs, settings).          The directory is create, Configure BattlEye / RCON remote console.          Keyword Args:             add, Auto-restart the server when it crashes (default: ``True``)., Unique server identifier., Server region tag (used by the server browser)., Path to a session save to load on startup. (+28 more)

### Community 2 - "AuthManager"
Cohesion: 0.15
Nodes (5): LoginCommand, RconCommandArgSpec, BanCreateCommand, BanListCommand, KickCommand

### Community 5 - "SteamCmdExecutable"
Cohesion: 0.13
Nodes (4): SteamCmd — Python wrapper for the steamcmd CLI tool., Config, SteamCmdExecutable, SteamCmdExecutableError

### Community 6 - "BattleEyeRconServer"
Cohesion: 0.08
Nodes (7): AbstractEventLoop, InstanceContainer, ServiceProvider, ApplicationException, CoreApplication, FilesystemServiceProvider, SupervisorInterface

### Community 7 - "lifecycle_controller.py"
Cohesion: 0.23
Nodes (8): HealthStatus, GetAppStatus, HealthResponseData, RestartRequestData, RestartResponseData, ServiceHealthData, ShutdownRequestData, ShutdownResponseData

### Community 8 - "TaskThreadingPolicy"
Cohesion: 0.15
Nodes (6): AuthManager, Authenticate, AuthenticateWithBasic, AuthenticateWithHeader, AuthenticateWithToken, HttpServiceProvider

### Community 9 - "RouteFacade"
Cohesion: 0.14
Nodes (4): Mixin adding registered RCON command dispatch to any client that     exposes a `, RegisteredRconClient, SendCommandProtocol, RconCommandArgumentError

### Community 14 - "app"
Cohesion: 0.09
Nodes (3): config(), get_application(), app()

### Community 15 - "Packet"
Cohesion: 0.14
Nodes (10): Generator, GeneratorResult, _detect_poetry_package_path(), _fmt_list(), main(), _print_result(), # TODO: Register bindings on the service container., # TODO: Build and register tasks with the supervisor. (+2 more)

### Community 16 - "ConsoleKernel"
Cohesion: 0.15
Nodes (8): set_application(), bootstrap_console(), bootstrap_http(), ConsoleKernel, HttpKernel, Kernel, RuntimeEntry, TypedResult

### Community 17 - ".generate"
Cohesion: 0.12
Nodes (7): BanRemoveCommand, IdCommand, LogoutCommand, PlayersCommand, RestartCommand, RolesCommand, ShutdownCommand

### Community 18 - "ServiceProvider"
Cohesion: 0.18
Nodes (11): Configurable, _resolve_config_type(), Dictionary, Config, RegistersRconCommand, ArmaReforgerRconClient, High-level RCON client for Arma Reforger.      Command registration, dispatch, a, ArmaReforgerServerError (+3 more)

### Community 22 - "BoundMethod"
Cohesion: 0.13
Nodes (3): KeepAlivePacket, BattleEyeInvalidPacketException, ServerMessageRequestPacket

### Community 23 - "TaskGraph"
Cohesion: 0.19
Nodes (6): DuplicateTaskNameError, TaskGraphCycleError, UnresolvedDependencyError, TaskGraph, TaskGraphCompiler, _UnresolvedSentinel

### Community 24 - "AsyncDatagramTransport"
Cohesion: 0.06
Nodes (10): DatagramProtocol, DatagramTransport, Exception, entry(), main(), entry(), main(), AsyncDatagramTransport (+2 more)

### Community 26 - "Path"
Cohesion: 0.12
Nodes (3): Any, ErrorInterface, CacheProtocol

### Community 28 - "HttpServiceProvider"
Cohesion: 0.18
Nodes (5): GraphTaskRuntime, _result_error(), _run_shutdown(), WorkerPool, Semaphore

### Community 29 - "TaskRuntime"
Cohesion: 0.15
Nodes (4): Event, ProgressChannel, ProgressUpdate, TaskRuntime

### Community 35 - "RestartPolicy"
Cohesion: 0.22
Nodes (7): RestartPolicy, _emit_banner(), TelemetryServiceProvider, CollectServerTelemetryTask, FormatTelemetryReportTask, TelemetryAlertTask, TelemetryReadinessProbeTask

### Community 36 - "env"
Cohesion: 0.14
Nodes (5): config(), env(), Facade for reading typed environment variables from the application., config(), config()

### Community 38 - "ContextualAttribute"
Cohesion: 0.16
Nodes (4): Config, Give, Tag, ContextualAttribute

### Community 41 - "RouteGroupStack"
Cohesion: 0.11
Nodes (10): CacheIndex, CacheProtocol, Lock, CacheStorageDriver, _failure(), _failure_msg(), _is_already_exists(), _is_not_found() (+2 more)

### Community 42 - "RouteRegistrar"
Cohesion: 0.08
Nodes (8): route(), URL, RequestContext, RouteNotFoundException, RouteParameterMissingException, UrlGenerator, auth(), request()

### Community 43 - "CommandResponse"
Cohesion: 0.21
Nodes (3): RequestMessage, ServerMessageResponsePacket, UnknownPacket

### Community 47 - "SubprocessHandle"
Cohesion: 0.18
Nodes (19): SupervisorRequestKind, TaskThreadingPolicy, SupervisorRequestInterface, _ExclusiveWorker, ProcessInfoData, RequestInfoData, _SharedWorker, SupervisorError (+11 more)

### Community 49 - "Message"
Cohesion: 0.26
Nodes (4): DiscoveryHook, TypeDiscoveryError, TypeDiscoveryServiceProvider, MultiImplementation

### Community 52 - "TaskBuilder"
Cohesion: 0.19
Nodes (14): A2SConfig, GameConfig, GamePropertiesConfig, GamePropertiesPersistence, JoinQueueConfig, ModConfig, OperatingConfig, RconConfig (+6 more)

### Community 53 - "TaskInterface"
Cohesion: 0.19
Nodes (4): APIRouter, RouteCompiler, RouteParameter, HttpKernel

### Community 57 - "get_application"
Cohesion: 0.20
Nodes (4): ModuleLoader, ModuleLoaderError, providers(), ModuleType

### Community 59 - "URL"
Cohesion: 0.11
Nodes (5): ErrorInterface, CoreApplicationInterface, KernelInterface, RconPacketInterface, Protocol

### Community 62 - "ArmaDen"
Cohesion: 0.22
Nodes (8): ArmaDen, Build Locally, CLI Entrypoints, Install, Manual Application Setup, Packages, Run with Docker, Scaffold an Application

### Community 65 - "RconCommandInterface"
Cohesion: 0.14
Nodes (3): ConsoleServiceProvider, DeferrableProvider, ServiceProvider

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
Cohesion: 0.14
Nodes (7): BattleEyeRconServer, Client, ClientState, ResponseMessage, LoginStatus, LoginResponsePacket, IntEnum

### Community 77 - ".addons_verify"
Cohesion: 0.40
Nodes (3): CacheSerializationError, CacheSerializer, Any

### Community 78 - ".ai_limit"
Cohesion: 0.16
Nodes (5): ApiUser, ConfigUserProvider, AuthGuard, CustomHeaderGuard, TokenGuard

### Community 82 - "get_application"
Cohesion: 0.25
Nodes (4): SupervisorRequestArgs, SupervisorRequestData, RestartAppService, ShutdownAppService

### Community 83 - ".freeze_check"
Cohesion: 0.18
Nodes (7): GenericError, ArmaReforgerExecutableFlag, ArmaReforgerExecutableFlagError, Arma Reforger CLI startup flags., ApplicationError, ApplicationStatus, StrEnum

### Community 84 - "Kernel"
Cohesion: 0.25
Nodes (3): Bind, Scoped, Singleton

### Community 86 - "SteamCmdExecutableError"
Cohesion: 0.19
Nodes (8): ClientStatus, CommandResponse, Message, _PendingCommand, ServerMessage, CommandHeader, CommandResponsePacket, TransportNotConnectedException

### Community 89 - ".log_append"
Cohesion: 0.29
Nodes (4): CircularDependencyException, EntryNotFoundException, LogicException, SelfBuilding

### Community 125 - "AbstractEventLoop"
Cohesion: 0.33
Nodes (5): MANDATORY: Code Comment Conventions, MANDATORY: Git Rules, MANDATORY: Local Code Search/Traversal, MANDATORY: Use td for Task Management, MANDATORY: Worktree Management

## Knowledge Gaps
- **14 isolated node(s):** `armaden`, `ApiResponseData`, `MANDATORY: Local Code Search/Traversal`, `MANDATORY: Use td for Task Management`, `MANDATORY: Worktree Management` (+9 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **235 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ArmaReforgerServerExecutable` connect `ArmaReforgerServerExecutable` to `SteamCmdExecutable`, `.generate_shaders`, `.backend_disable_storage`, `.backend_local_storage`, `.check_instance`, `.log_time`, `ServiceProvider`, `.custom`, `.disable_ai`, `.logs_dir`, `.disable_shaders_build`, `.freeze_check`, `.freeze_check_mode`, `.a2s`, `.jobsys_long_worker_count`, `.create_db`, `.addon`, `__init__.py`, `.addon_download_dir`, `.addon_temp_dir`, `.addons`, `.keep_num_of_logs`, `.keep_session_save`, `.addons_dir`, `.language`, `.limit_fps`, `.list_scenarios`, `.log_fs`, `.log_rdb_checksum`, `TaskBuilder`, `.log_scr_checksum`, `.log_stats`, `.no_splash`, `.nwk_resolution`, `.player_limits`, `.scenario`, `.server_world`, `.silent_crash_report`, `.script_authorize_all`, `.staggering_budget`, `PlayerResponseData`, `.backend_local_storage`, `api.py`, `.log_scr_checksum`, `Executable`, `.backend_fresh_session`?**
  _High betweenness centrality (0.139) - this node is a cross-community bridge._
- **Why does `InstanceContainer` connect `InstanceContainer` to `WorkerPool`, `.get_alias`, `RconCommandArgumentError`, `RconCommandInterface`, `ContextualAttribute`, `SupervisorInterface`, `.resolve_primitive`, `BattleEyeRconClient`, `SubprocessHandle`, `Exception`, `Message`, `.resolve`, `Kernel`, `.log_append`, `HttpServiceProvider`?**
  _High betweenness centrality (0.137) - this node is a cross-community bridge._
- **Why does `ServiceProvider` connect `RconCommandInterface` to `PlayerResponseData`, `InstanceContainer`, `RestartPolicy`, `lifecycle_controller.py`, `ServerMessageResponsePacket`, `TaskThreadingPolicy`, `Exception`, `Message`, `TypedDict`, `get_application`?**
  _High betweenness centrality (0.079) - this node is a cross-community bridge._
- **Are the 25 inferred relationships involving `InstanceContainer` (e.g. with `Application` and `Config`) actually correct?**
  _`InstanceContainer` has 25 INFERRED edges - model-reasoned connections that need verification._
- **Are the 11 inferred relationships involving `ArmaReforgerServerExecutable` (e.g. with `Executable` and `Dictionary`) actually correct?**
  _`ArmaReforgerServerExecutable` has 11 INFERRED edges - model-reasoned connections that need verification._
- **Are the 15 inferred relationships involving `Supervisor` (e.g. with `SupervisorRequestData` and `SupervisorRequestKind`) actually correct?**
  _`Supervisor` has 15 INFERRED edges - model-reasoned connections that need verification._
- **What connects `armaden`, `Mixin adding registered RCON command dispatch to any client that     exposes a ``, `Accepts any Enum instance that implements a .message property.` to the rest of the system?**
  _107 weakly-connected nodes found - possible documentation gaps or missing edges._