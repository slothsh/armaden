# Graph Report - armaden  (2026-08-31)

## Corpus Check
- 222 files · ~46,302 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 2256 nodes · 4357 edges · 344 communities (85 shown, 259 thin omitted)
- Extraction: 84% EXTRACTED · 16% INFERRED · 0% AMBIGUOUS · INFERRED: 692 edges (avg confidence: 0.55)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `3fdda648`
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
- .disable_crash_reporter
- .force_session_load
- .jobsys_short_worker_count
- .server_id
- .keep_session_save
- .log_rdb_checksum
- .nds
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
- .no_backend
- FilesystemServiceProvider
- DefaultApplication
- .profile
- .rpl_encode_as_long_jobs
- .keep_num_of_logs
- DatabaseServiceProvider
- Exception
- api.py
- Result
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
- .jobsys_long_worker_count
- .language
- .log_rdb_checksum
- .nwk_resolution
- .keep_crash_files
- .rpl_encode_as_long_jobs
- .scenario
- .log_level
- .server_id
- .streams_delta
- .world
- ABC
- ._get_json_body
- .no_splash
- TaskInjector
- UrlGenerator
- .player_limits
- RequestContext
- CacheSerializer
- Error
- PendingChain
- SteamCmdExecutableFlag
- .streaming_budget
- .log_voting
- .minidump
- Executable
- .nds
- .no_backend
- Future
- .no_splash
- .no_throw
- Any
- Result
- Any
- ServiceProvider
- Any
- RconCommandInterface
- .nwk_resolution
- .player_limits
- .region
- .rpl_encode_as_long_jobs
- RconCommandRepository
- async_datagram_transport.py
- .scenario
- .silent_crash_report
- .single_threaded_update
- .streaming_budget
- .streams_delta
- .vm_error_mode
- arma_reforger_server_executable.py
- ArmaReforgerExecutableFlag
- SteamCmdExecutableError
- .make
- SteamCmdExecutableFlag
- FilesystemServiceProvider
- application.py
- .a2s
- .addons_repair
- .addons_verify
- .backend_fresh_session
- .custom
- .debugger_port
- .disable_ai
- .disable_crash_reporter
- .disable_shaders_build
- .force_session_load
- .freeze_check
- .freeze_check_mode
- .keep_num_of_logs
- .limit_fps
- .log_scr_checksum
- .log_stats
- .no_sound
- .rcon
- .rpl_timeout_ms
- .staggering_budget
- Result
- TaskRuntimeInterface

## God Nodes (most connected - your core abstractions)
1. `InstanceContainer` - 123 edges
2. `ArmaReforgerServerExecutable` - 82 edges
3. `Supervisor` - 52 edges
4. `CacheStorageDriver` - 50 edges
5. `Request` - 49 edges
6. `BattleEyeRconClient` - 44 edges
7. `app()` - 41 edges
8. `Cache` - 36 edges
9. `CacheProtocol` - 36 edges
10. `RconCommandInterface` - 36 edges

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

## Communities (344 total, 259 thin omitted)

### Community 0 - "ArmaReforgerServerExecutable"
Cohesion: 0.07
Nodes (15): Executable, ArmaReforgerServerExecutable, Unique server identifier., Disable storage loads and saves (online and local)., Skip splash screens on startup., Set the Steam Query Protocol bind IP address., Print scenario .conf file paths to the log on startup., Maximum players per faction (``FactionKey:Number`` pairs). (+7 more)

### Community 2 - "AuthManager"
Cohesion: 0.28
Nodes (12): A2SConfig, Config, GameConfig, GamePropertiesConfig, GamePropertiesPersistence, JoinQueueConfig, ModConfig, OperatingConfig (+4 more)

### Community 5 - "SteamCmdExecutable"
Cohesion: 0.11
Nodes (7): QueueDriver, CacheQueueDriver, Exception, Result, Persists jobs to a Cache store with a queue-specific index for ordering     and, DatabaseQueueDriver, Persists jobs to a database table via the ORM, supports delayed jobs,     tracks

### Community 7 - "lifecycle_controller.py"
Cohesion: 0.08
Nodes (13): HealthStatus, GetAppStatus, Api, Controllers for API routes, LifecycleController, ApiResponseData, HealthResponseData, RestartRequestData (+5 more)

### Community 8 - "TaskThreadingPolicy"
Cohesion: 0.09
Nodes (14): Path, Result, TaskRuntimeInterface, Path to a server configuration JSON file., Directory for profiles (saves, logs, settings).          The directory is create, Redirect log output to the given directory., Path to a session save to load on startup., Additional directories to search for mods.          Multiple directories can be (+6 more)

### Community 9 - "RouteFacade"
Cohesion: 0.21
Nodes (4): Mixin adding registered RCON command dispatch to any client that     exposes a `, RegisteredRconClient, RconCommandInterface, SendCommandProtocol

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
Nodes (8): BanCreateCommand, BanRemoveCommand, IdCommand, LogoutCommand, PlayersCommand, RestartCommand, RolesCommand, ShutdownCommand

### Community 18 - "ServiceProvider"
Cohesion: 0.18
Nodes (4): RconDiscoveryHook, RegistersRconCommand, ArmaReforgerRconClient, High-level RCON client for Arma Reforger.      Command registration, dispatch, a

### Community 20 - "TaskRuntimeInterface"
Cohesion: 0.27
Nodes (3): QueueWorker, Supervisor-managed Task that polls a queue driver and processes jobs     with re, Task

### Community 23 - "TaskGraph"
Cohesion: 0.18
Nodes (6): DuplicateTaskNameError, TaskGraphCycleError, UnresolvedDependencyError, TaskGraph, TaskGraphCompiler, _UnresolvedSentinel

### Community 24 - "AsyncDatagramTransport"
Cohesion: 0.16
Nodes (4): MultiImplementation, Self, Job, Base class for all queue jobs. Users subclass this and implement handle().

### Community 25 - "UrlGenerator"
Cohesion: 0.09
Nodes (3): __getattr__(), _LegacyTask, TaskBuilder

### Community 28 - "HttpServiceProvider"
Cohesion: 0.13
Nodes (7): RconCommandInterface, RconCommandRepository, RegistersRconCommand, SendCommandProtocol, ArmaReforgerServer, PathContainer, TaskRuntimeInterface

### Community 29 - "TaskRuntime"
Cohesion: 0.15
Nodes (4): Event, ProgressChannel, ProgressUpdate, TaskRuntime

### Community 30 - "Exception"
Cohesion: 0.07
Nodes (6): Result, LocalFilesystem, QueueDriver, Contract for queue backend drivers. Sync, Database, and Cache drivers     implem, Runs jobs immediately on the calling thread with no persistence., SyncQueueDriver

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
Cohesion: 0.12
Nodes (3): ABC, Controller, CacheIndex

### Community 45 - "_BuiltTask"
Cohesion: 0.06
Nodes (10): DatagramProtocol, DatagramTransport, Exception, entry(), main(), entry(), main(), AsyncDatagramTransport (+2 more)

### Community 47 - "SubprocessHandle"
Cohesion: 0.18
Nodes (21): SupervisorRequestKind, TaskThreadingPolicy, GenericError, SupervisorRequestInterface, _ExclusiveWorker, ProcessInfoData, RequestInfoData, _SharedWorker (+13 more)

### Community 48 - "._initialize_configs"
Cohesion: 0.18
Nodes (5): GraphTaskRuntime, _result_error(), _run_shutdown(), WorkerPool, Semaphore

### Community 49 - "Message"
Cohesion: 0.26
Nodes (4): DiscoveryHook, TypeDiscoveryError, TypeDiscoveryServiceProvider, MultiImplementation

### Community 50 - "Task"
Cohesion: 0.18
Nodes (3): Lifecycle, Pipeline, TaskRuntimeInterface

### Community 53 - "TaskInterface"
Cohesion: 0.25
Nodes (4): APIRouter, RouteCompiler, RouteParameter, HttpKernel

### Community 54 - "TaskBuilderInterface"
Cohesion: 0.29
Nodes (5): ArmaReforgerRconClient, ArmaReforgerServerConfig, ArmaReforgerServerError, ArmaReforgerServerException, ExecutableContainer

### Community 57 - "get_application"
Cohesion: 0.20
Nodes (4): ModuleLoader, ModuleLoaderError, providers(), ModuleType

### Community 58 - "AppServiceProvider"
Cohesion: 0.13
Nodes (3): KeepAlivePacket, BattleEyeInvalidPacketException, ServerMessageRequestPacket

### Community 59 - "URL"
Cohesion: 0.11
Nodes (5): ErrorInterface, CoreApplicationInterface, KernelInterface, RconPacketInterface, Protocol

### Community 60 - "Dictionary"
Cohesion: 0.12
Nodes (5): LoginCommand, _Missing, RconCommandArgSpec, BanListCommand, KickCommand

### Community 62 - "ArmaDen"
Cohesion: 0.22
Nodes (8): ArmaDen, Build Locally, CLI Entrypoints, Install, Manual Application Setup, Packages, Run with Docker, Scaffold an Application

### Community 67 - "PlayerResponseData"
Cohesion: 0.25
Nodes (4): SupervisorRequestArgs, SupervisorRequestData, RestartAppService, ShutdownAppService

### Community 71 - "LoginResponsePacket"
Cohesion: 0.33
Nodes (3): PlayerResponseData, Parse a single data row from ``players`` output.          Returns ``None``  if t, A connected player returned by the ``players`` command.

### Community 72 - "ServerMessageResponsePacket"
Cohesion: 0.20
Nodes (6): AuthManager, Authenticate, AuthenticateWithBasic, AuthenticateWithHeader, AuthenticateWithToken, HttpServiceProvider

### Community 73 - ".resolve_primitive"
Cohesion: 0.13
Nodes (9): BoundMethod, get_class_for_callable(), get_contextual_attribute_from_dependency(), get_parameter_class_name(), is_parameter_required(), Utility helpers shared between the container and bound-method resolution., Determine the class name associated with a callable for build-stack tracking., resolve_string_to_class() (+1 more)

### Community 75 - ".addon"
Cohesion: 0.14
Nodes (7): BattleEyeRconServer, Client, ClientState, ResponseMessage, LoginStatus, LoginResponsePacket, IntEnum

### Community 84 - "Kernel"
Cohesion: 0.25
Nodes (3): Bind, Scoped, Singleton

### Community 86 - "SteamCmdExecutableError"
Cohesion: 0.19
Nodes (8): ClientStatus, CommandResponse, Message, _PendingCommand, ServerMessage, CommandHeader, CommandResponsePacket, TransportNotConnectedException

### Community 89 - ".log_append"
Cohesion: 0.29
Nodes (4): CircularDependencyException, EntryNotFoundException, LogicException, SelfBuilding

### Community 91 - ".log_scr_checksum"
Cohesion: 0.22
Nodes (3): ApiUser, ConfigUserProvider, BasicAuthGuard

### Community 92 - "Executable"
Cohesion: 0.21
Nodes (3): RequestMessage, ServerMessageResponsePacket, UnknownPacket

### Community 94 - "DefaultApi"
Cohesion: 0.40
Nodes (3): _MasoniteModel, Model, Base ORM model for armaden applications.      Extends masoniteorm's Model, overr

### Community 101 - ".nds"
Cohesion: 0.36
Nodes (5): json_response(), JSONResponse, response(), ResponseFactory, StarletteJSONResponse

### Community 125 - "AbstractEventLoop"
Cohesion: 0.33
Nodes (5): MANDATORY: Code Comment Conventions, MANDATORY: Git Rules, MANDATORY: Local Code Search/Traversal, MANDATORY: Use td for Task Management, MANDATORY: Worktree Management

### Community 159 - ".no_backend"
Cohesion: 0.28
Nodes (3): Configurable, _resolve_config_type(), Dictionary

### Community 161 - "DefaultApplication"
Cohesion: 0.15
Nodes (5): Application, ApplicationBase, Application, DefaultApplication, Application

### Community 275 - "._get_json_body"
Cohesion: 0.29
Nodes (4): Error, ErrorKindInterface, Enforces that any error type object has a code string and message string., Accepts any Enum instance that implements a .message property.

### Community 281 - "CacheSerializer"
Cohesion: 0.40
Nodes (3): CacheSerializationError, CacheSerializer, Any

### Community 283 - "PendingChain"
Cohesion: 0.25
Nodes (4): PendingChain, Marker interface. Jobs that implement this are dispatched asynchronously     to, Stub for chained job dispatch. Full chaining support is deferred to a     later, ShouldQueue

### Community 314 - "arma_reforger_server_executable.py"
Cohesion: 0.33
Nodes (3): Config, ArmaReforgerExecutableError, Arma Reforger dedicated server wrapper.  Provides a typed, fluent interface for

### Community 315 - "ArmaReforgerExecutableFlag"
Cohesion: 0.33
Nodes (3): ArmaReforgerExecutableFlag, ArmaReforgerExecutableFlagError, Arma Reforger CLI startup flags.

### Community 316 - "SteamCmdExecutableError"
Cohesion: 0.47
Nodes (3): SteamCmd — Python wrapper for the steamcmd CLI tool., Config, SteamCmdExecutableError

## Knowledge Gaps
- **14 isolated node(s):** `armaden`, `ApiResponseData`, `MANDATORY: Local Code Search/Traversal`, `MANDATORY: Use td for Task Management`, `MANDATORY: Worktree Management` (+9 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **259 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `InstanceContainer` connect `InstanceContainer` to `DefaultApplication`, `.get_alias`, `WorkerPool`, `RconCommandArgumentError`, `RconCommandInterface`, `ContextualAttribute`, `.resolve_primitive`, `.addons_verify`, `BattleEyeRconClient`, `SubprocessHandle`, `._initialize_configs`, `Message`, `ServiceProvider`, `.resolve`, `Kernel`, `.log_append`?**
  _High betweenness centrality (0.139) - this node is a cross-community bridge._
- **Why does `ArmaReforgerServerExecutable` connect `ArmaReforgerServerExecutable` to `.language`, `TaskThreadingPolicy`, `.log_rdb_checksum`, `.nwk_resolution`, `.rpl_encode_as_long_jobs`, `.scenario`, `.server_id`, `.streams_delta`, `.world`, `ABC`, `UrlGenerator`, `Error`, `SteamCmdExecutableFlag`, `.log_voting`, `.minidump`, `FilesystemServiceProvider`, `.nds`, `.profile`, `.no_backend`, `.keep_num_of_logs`, `DatabaseServiceProvider`, `.no_throw`, `.nwk_resolution`, `.region`, `.rpl_encode_as_long_jobs`, `.scenario`, `.single_threaded_update`, `.streaming_budget`, `.streams_delta`, `.vm_error_mode`, `arma_reforger_server_executable.py`, `.a2s`, `.addons_repair`, `.addons_verify`, `.backend_fresh_session`, `.custom`, `.debugger_port`, `.disable_ai`, `.disable_crash_reporter`, `.disable_shaders_build`, `.force_session_load`, `.freeze_check`, `.freeze_check_mode`, `.keep_num_of_logs`, `.limit_fps`, `.log_scr_checksum`, `.log_stats`, `.no_sound`, `.rcon`, `.rpl_timeout_ms`, `.staggering_budget`, `.force_session_load`, `.jobsys_short_worker_count`, `.keep_session_save`, `.log_rdb_checksum`?**
  _High betweenness centrality (0.124) - this node is a cross-community bridge._
- **Why does `ArmaReforgerExecutableError` connect `arma_reforger_server_executable.py` to `SubprocessHandle`?**
  _High betweenness centrality (0.116) - this node is a cross-community bridge._
- **Are the 25 inferred relationships involving `InstanceContainer` (e.g. with `Application` and `Config`) actually correct?**
  _`InstanceContainer` has 25 INFERRED edges - model-reasoned connections that need verification._
- **Are the 15 inferred relationships involving `Supervisor` (e.g. with `SupervisorRequestData` and `SupervisorRequestKind`) actually correct?**
  _`Supervisor` has 15 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Arma Reforger dedicated server wrapper.  Provides a typed, fluent interface for`, `Path to a server configuration JSON file.`, `Directory for profiles (saves, logs, settings).          The directory is create` to the rest of the system?**
  _116 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `ArmaReforgerServerExecutable` be split into smaller, more focused modules?**
  _Cohesion score 0.07142857142857142 - nodes in this community are weakly interconnected._