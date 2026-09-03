# Graph Report - armaden  (2026-09-03)

## Corpus Check
- 271 files · ~54,962 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 2826 nodes · 5918 edges · 380 communities (121 shown, 259 thin omitted)
- Extraction: 86% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 800 edges (avg confidence: 0.55)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `343b0c05`
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
- RestartPolicy
- SupervisorInterface
- RouteGroupStack
- _BuiltTask
- SubprocessHandle
- ._initialize_configs
- Message
- BoundMethod
- TaskInterface
- .make
- ContextualAttribute
- get_application
- AppServiceProvider
- URL
- Dictionary
- CommandRequestPacket
- ArmaDen
- .instance
- ArmaReforgerRconClient
- SelfBuildingTag
- StrEnum
- arma_reforger_server_executable.py
- Application
- Config
- LoginResponsePacket
- SupervisorRequestKind
- task_record_data.py
- .kind
- .addon
- Supervisor
- Cache
- CacheProtocol
- SteamCmdExecutableError
- S3Filesystem
- ErrorInterface
- Storage
- RouteFacade
- TaskInjector
- Executable
- RconCommandInterface
- DefaultApi
- CacheQueueDriver
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
- ApiUser
- Result
- instance_container.py
- Any
- AsyncStreamCallback
- Path
- Result
- Any
- Result
- .generate
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
- UrlGenerator
- FilesystemServiceProvider
- DefaultApplication
- .profile
- Middleware
- .keep_num_of_logs
- DatabaseServiceProvider
- Exception
- TaskGraph
- TaskInterface
- TaskRuntimeInterface
- api.py
- Result
- .disable_shaders_build
- .enable_night_grain
- .force_session_load
- .freeze_check_mode
- .jobsys_long_worker_count
- .keep_num_of_logs
- AuthManager
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
- ScheduleFacade
- .staggering_budget
- __init__.py
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
- env
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
- .resolve_dependencies
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
- __init__.py
- .language
- .log_rdb_checksum
- .nwk_resolution
- .keep_crash_files
- Job
- .rpl_encode_as_long_jobs
- .scenario
- .log_level
- .server_id
- .streams_delta
- .world
- ABC
- SupervisorInterface
- .no_splash
- TaskInjector
- UrlGenerator
- .player_limits
- Supervisor
- CacheSerializer
- Error
- WorkerPool
- SteamCmdExecutableFlag
- .streaming_budget
- .log_voting
- .minidump
- Executable
- .nds
- .no_backend
- Future
- _LegacyTask
- .no_throw
- CoreApplicationInterface
- Any
- Result
- Any
- ServiceProvider
- RouteGroupStack
- Any
- RconCommandInterface
- .nwk_resolution
- .player_limits
- .region
- .rpl_encode_as_long_jobs
- RconCommandRepository
- async_datagram_transport.py
- .scenario
- Result
- .single_threaded_update
- .streaming_budget
- .streams_delta
- .vm_error_mode
- arma_reforger_server_executable.py
- Executable
- ContextualAttribute
- SyncQueueDriver
- RouteRegistrar
- Queue
- ApplicationInterface
- .a2s
- .addons_repair
- .addons_verify
- .backend_fresh_session
- .custom
- .debugger_port
- .disable_ai
- QueueDriver
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
- QueueWorker
- TaskBuilder
- RouteGroup
- QueueServiceProvider
- ._dispatch_to_worker
- TaskBuilderInterface
- Dictionary
- RegisteredRconClient
- ErrorKindProtocol
- LoginResponsePacket
- URL
- __init__.py
- ConcurrencyBuilder
- Bind
- ContextualBindingBuilder
- _Missing
- .execute
- ContainerDunderProtocol
- Result
- DatagramTransportInterface
- create_cache_driver
- .add_task
- HealthStatus
- supervisor.py
- .dispatch_subprocess
- SelfBuildingTag

## God Nodes (most connected - your core abstractions)
1. `ErrorInterface` - 167 edges
2. `InstanceContainer` - 138 edges
3. `Container` - 109 edges
4. `ArmaReforgerServerExecutable` - 82 edges
5. `ContainerMethodsProtocol` - 81 edges
6. `Request` - 69 edges
7. `CacheStorageDriver` - 56 edges
8. `Supervisor` - 53 edges
9. `CoreApplication` - 52 edges
10. `TaskGraph` - 47 edges

## Surprising Connections (you probably didn't know these)
- `Application` --uses--> `InstanceContainer`  [INFERRED]
  src/armaden/framework1/application.py → src/armaden/framework1/classes/instance_container.py
- `DefaultApplication` --uses--> `Application`  [INFERRED]
  src/armaden/framework1/runtime/default_application.py → src/armaden/framework1/application.py
- `Bind` --uses--> `InstanceContainer`  [INFERRED]
  src/armaden/framework1/attributes/__init__.py → src/armaden/framework1/classes/instance_container.py
- `Singleton` --uses--> `InstanceContainer`  [INFERRED]
  src/armaden/framework1/attributes/__init__.py → src/armaden/framework1/classes/instance_container.py
- `Scoped` --uses--> `InstanceContainer`  [INFERRED]
  src/armaden/framework1/attributes/__init__.py → src/armaden/framework1/classes/instance_container.py

## Import Cycles
- None detected.

## Communities (380 total, 259 thin omitted)

### Community 0 - "ArmaReforgerServerExecutable"
Cohesion: 0.07
Nodes (15): Executable, ArmaReforgerServerExecutable, Unique server identifier., Disable storage loads and saves (online and local)., Skip splash screens on startup., Set the Steam Query Protocol bind IP address., Print scenario .conf file paths to the log on startup., Maximum players per faction (``FactionKey:Number`` pairs). (+7 more)

### Community 1 - "Request"
Cohesion: 0.07
Nodes (3): Any, Request, StarletteRequest

### Community 2 - "AuthManager"
Cohesion: 0.08
Nodes (3): ContainerInstanceProtocol, ContainerProtocol, Container

### Community 3 - "Protocol"
Cohesion: 0.12
Nodes (3): BattleEyeRconClient, ArmaReforgerRconClient, High-level RCON client for Arma Reforger.      Command registration, dispatch, a

### Community 7 - "lifecycle_controller.py"
Cohesion: 0.08
Nodes (14): GetAppStatus, RestartAppService, ShutdownAppService, Api, Controllers for API routes, LifecycleController, ApiResponseData, HealthResponseData (+6 more)

### Community 8 - "TaskThreadingPolicy"
Cohesion: 0.09
Nodes (14): Path, Result, TaskRuntimeInterface, Path to a server configuration JSON file., Directory for profiles (saves, logs, settings).          The directory is create, Redirect log output to the given directory., Path to a session save to load on startup., Additional directories to search for mods.          Multiple directories can be (+6 more)

### Community 10 - "Supervisor"
Cohesion: 0.08
Nodes (9): ProcessBuilder, _ProcessTask, Any, AsyncStreamCallback, Path, Result, SubprocessHandle, config() (+1 more)

### Community 14 - "app"
Cohesion: 0.08
Nodes (11): TaskThreadingPolicy, Self, TaskBuilderInterface, TaskProtocol, Any, AsyncStreamCallback, Path, Result (+3 more)

### Community 16 - "ConsoleKernel"
Cohesion: 0.15
Nodes (9): set_application(), bootstrap_console(), bootstrap_http(), ConsoleKernel, HttpKernel, Kernel, Any, RuntimeEntry (+1 more)

### Community 17 - ".generate"
Cohesion: 0.08
Nodes (10): BanCreateCommand, BanListCommand, BanRemoveCommand, IdCommand, KickCommand, LogoutCommand, PlayersCommand, RestartCommand (+2 more)

### Community 22 - "BoundMethod"
Cohesion: 0.13
Nodes (3): LoginRequestPacket, BattleEyeInvalidPacketException, ServerMessageResponsePacket

### Community 24 - "AsyncDatagramTransport"
Cohesion: 0.14
Nodes (5): ContextualBindingBuilderProtocol, Self, ContextualBindingBuilderProtocol, ContextualBindingBuilder, ContainerProtocol

### Community 25 - "UrlGenerator"
Cohesion: 0.16
Nodes (8): APIRouter, HttpKernel, Controller, Any, FastAPI, RouteCompiler, RouteParameter, RouteDefinition

### Community 28 - "HttpServiceProvider"
Cohesion: 0.05
Nodes (24): Any, ArmaReforgerRconClient, ArmaReforgerServerConfig, CallbackReference, CoroutineType, ArmaReforgerExecutableFlag, ArmaReforgerExecutableFlagError, Arma Reforger CLI startup flags. (+16 more)

### Community 29 - "TaskRuntime"
Cohesion: 0.12
Nodes (9): Event, ProgressChannel, ProgressUpdate, AbstractEventLoop, Any, AsyncStreamCallback, Path, Result (+1 more)

### Community 31 - "ProcessBuilder"
Cohesion: 0.14
Nodes (9): ProcessInfoData, TaskStateData, ThreadInfoData, Any, AsyncStreamCallback, Path, Result, TaskError (+1 more)

### Community 35 - "RestartPolicy"
Cohesion: 0.14
Nodes (8): AppServiceProvider, _emit_banner(), TelemetryServiceProvider, CollectServerTelemetryTask, FormatTelemetryReportTask, TelemetryAlertTask, TelemetryReadinessProbeTask, providers()

### Community 45 - "_BuiltTask"
Cohesion: 0.08
Nodes (11): DatagramProtocol, DatagramTransport, Exception, entry(), main(), ClientStatus, entry(), main() (+3 more)

### Community 48 - "._initialize_configs"
Cohesion: 0.11
Nodes (7): RestartPolicy, _BuiltCallbacks, _BuiltTask, Any, Result, Self, TaskBuilder

### Community 49 - "Message"
Cohesion: 0.21
Nodes (4): ExclusiveWorker, WorkerPool, SharedWorker, Worker

### Community 50 - "BoundMethod"
Cohesion: 0.25
Nodes (5): BoundMethodProtocol, Signature, BoundMethod, ContainerProtocol, Parameter

### Community 53 - "TaskInterface"
Cohesion: 0.07
Nodes (11): CacheIndex, FileCacheIndex, create_cache_driver(), CacheSerializationError, CacheSerializer, Any, DatabaseQueueDriver, Any (+3 more)

### Community 55 - ".make"
Cohesion: 0.13
Nodes (9): CacheStorageDriver, _failure(), _failure_msg(), _is_already_exists(), _is_not_found(), Any, Exception, Lock (+1 more)

### Community 56 - "ContextualAttribute"
Cohesion: 0.14
Nodes (5): config(), Any, DatabaseError, get_application(), SchemaError

### Community 57 - "get_application"
Cohesion: 0.26
Nodes (5): MultiImplementation, DiscoveryHook, Result, TypeDiscoveryError, TypeDiscoveryServiceProvider

### Community 58 - "AppServiceProvider"
Cohesion: 0.12
Nodes (4): CoreApplication, AbstractEventLoop, Any, Result

### Community 59 - "URL"
Cohesion: 0.08
Nodes (10): RconPacketInterface, DatagramTransportInterface, Protocol, ErrorProtocol, BoundMethodProtocol, ContainerDunderProtocol, ContainerInstanceProtocol, ContainerProtocol (+2 more)

### Community 62 - "ArmaDen"
Cohesion: 0.22
Nodes (8): ArmaDen, Build Locally, CLI Entrypoints, Install, Manual Application Setup, Packages, Run with Docker, Scaffold an Application

### Community 63 - ".instance"
Cohesion: 0.29
Nodes (3): CircularDependencyException, EntryNotFoundException, LogicException

### Community 65 - "ArmaReforgerRconClient"
Cohesion: 0.17
Nodes (23): SupervisorRequestData, SupervisorRequestKind, TaskThreadingPolicy, StrEnum, SupervisorRequestInterface, TaskError, ConcurrencyFacade, ScheduleFacade (+15 more)

### Community 68 - "arma_reforger_server_executable.py"
Cohesion: 0.11
Nodes (15): create_filesystem(), ApplicationError, ApplicationException, ApplicationStatus, DefaultApplication, Result, ConsoleServiceProvider, Result (+7 more)

### Community 71 - "LoginResponsePacket"
Cohesion: 0.33
Nodes (3): PlayerResponseData, Parse a single data row from ``players`` output.          Returns ``None``  if t, A connected player returned by the ``players`` command.

### Community 74 - ".kind"
Cohesion: 0.06
Nodes (23): A2SConfig, Config, GameConfig, GamePropertiesConfig, GamePropertiesPersistence, JoinQueueConfig, ModConfig, OperatingConfig (+15 more)

### Community 75 - ".addon"
Cohesion: 0.14
Nodes (7): BattleEyeRconServer, Client, ClientState, ResponseMessage, LoginStatus, LoginResponsePacket, IntEnum

### Community 83 - "Supervisor"
Cohesion: 0.08
Nodes (10): GraphTaskRuntime, Semaphore, AbstractEventLoop, Any, Future, Result, Self, _result_error() (+2 more)

### Community 85 - "CacheProtocol"
Cohesion: 0.12
Nodes (3): CacheProtocol, Any, Result

### Community 86 - "SteamCmdExecutableError"
Cohesion: 0.19
Nodes (6): CommandResponse, Message, _PendingCommand, ServerMessage, CommandHeader, CommandResponsePacket

### Community 88 - "ErrorInterface"
Cohesion: 0.15
Nodes (3): ErrorInterface, Filesystem, Result

### Community 90 - "RouteFacade"
Cohesion: 0.13
Nodes (4): Any, Route, Any, RouteFacade

### Community 91 - "TaskInjector"
Cohesion: 0.13
Nodes (7): Any, Parameter, TaskInjector, Any, Result, Task, TaskPolicy

### Community 92 - "Executable"
Cohesion: 0.34
Nodes (3): DB, Any, Result

### Community 93 - "RconCommandInterface"
Cohesion: 0.12
Nodes (8): RconCommandRepository, RconDiscoveryHook, Any, CommandResponse, Future, RconCommandInterface, RegistersRconCommand, Result

### Community 94 - "DefaultApi"
Cohesion: 0.16
Nodes (3): app(), Any, T

### Community 95 - "CacheQueueDriver"
Cohesion: 0.24
Nodes (5): CacheQueueDriver, Exception, Lock, Result, Persists jobs to a Cache store with a queue-specific index for ordering     and

### Community 101 - ".nds"
Cohesion: 0.24
Nodes (8): auth(), RequestContext, json_response(), JSONResponse, Any, response(), ResponseFactory, StarletteJSONResponse

### Community 128 - "instance_container.py"
Cohesion: 0.17
Nodes (12): BoundMethod, array_wrap(), get_class_for_callable(), get_contextual_attribute_from_dependency(), get_parameter_class_name(), is_parameter_required(), Any, Parameter (+4 more)

### Community 135 - ".generate"
Cohesion: 0.14
Nodes (12): Generator, GeneratorResult, Path, _detect_poetry_package_path(), _fmt_list(), main(), _print_result(), Path (+4 more)

### Community 159 - "UrlGenerator"
Cohesion: 0.12
Nodes (8): Any, route(), URL, request(), Any, RouteNotFoundException, RouteParameterMissingException, UrlGenerator

### Community 163 - "Middleware"
Cohesion: 0.15
Nodes (7): HttpKernel, Middleware, Any, NextCallable, MiddlewarePipeline, Any, # TODO: handle this

### Community 167 - "TaskGraph"
Cohesion: 0.19
Nodes (7): DuplicateTaskNameError, TaskGraphCycleError, UnresolvedDependencyError, Any, TaskGraph, TaskGraphCompiler, _UnresolvedSentinel

### Community 168 - "TaskInterface"
Cohesion: 0.14
Nodes (5): Self, StatusCallback, TaskCallback, TaskBuilderInterface, TaskInterface

### Community 169 - "TaskRuntimeInterface"
Cohesion: 0.13
Nodes (10): Any, AsyncStreamCallback, Path, Result, TaskRuntimeInterface, DefaultApi, DefaultApiError, Any (+2 more)

### Community 179 - "AuthManager"
Cohesion: 0.14
Nodes (14): ApiUser, AuthManager, Any, Authenticate, AuthenticateWithBasic, AuthenticateWithHeader, AuthenticateWithToken, ConfigUserProvider (+6 more)

### Community 191 - "ScheduleFacade"
Cohesion: 0.14
Nodes (4): Any, Result, ScheduleBuilder, _ScheduledTask

### Community 193 - "__init__.py"
Cohesion: 0.13
Nodes (8): Error, ErrorKindInterface, Enforces that any error type object has a code string and message string., Accepts any Enum instance that implements a .message property., GenericError, Any, RconCommandArgumentError, ModuleLoaderError

### Community 207 - "env"
Cohesion: 0.10
Nodes (9): config(), config(), config(), config(), config(), config(), env(), Any (+1 more)

### Community 225 - ".resolve_dependencies"
Cohesion: 0.18
Nodes (3): BindingResolutionException, Parameter, SelfBuilding

### Community 262 - "__init__.py"
Cohesion: 0.23
Nodes (4): T, Repository, Lifecycle, Pipeline

### Community 267 - "Job"
Cohesion: 0.20
Nodes (6): Job, Any, Exception, Result, Self, Base class for all queue jobs. Users subclass this and implement handle().

### Community 275 - "SupervisorInterface"
Cohesion: 0.13
Nodes (4): Application, Result, Self, SupervisorInterface

### Community 280 - "Supervisor"
Cohesion: 0.14
Nodes (5): AbstractEventLoop, Container, Any, Supervisor, SupervisorRequestInterface

### Community 292 - "_LegacyTask"
Cohesion: 0.18
Nodes (4): __getattr__(), _LegacyTask, StatusCallback, TaskCallback

### Community 294 - "CoreApplicationInterface"
Cohesion: 0.20
Nodes (4): CoreApplicationInterface, KernelInterface, Any, Result

### Community 299 - "RouteGroupStack"
Cohesion: 0.23
Nodes (3): GroupState, Any, RouteGroupStack

### Community 309 - "Result"
Cohesion: 0.27
Nodes (3): Future, Result, TaskRecord

### Community 315 - "Executable"
Cohesion: 0.21
Nodes (5): PushValue, Executable, Path, Result, Self

### Community 316 - "ContextualAttribute"
Cohesion: 0.20
Nodes (7): Config, Give, Any, Parameter, register_builtin_attributes(), Tag, ContextualAttribute

### Community 317 - "SyncQueueDriver"
Cohesion: 0.23
Nodes (4): Exception, Result, Runs jobs immediately on the calling thread with no persistence., SyncQueueDriver

### Community 320 - "ApplicationInterface"
Cohesion: 0.23
Nodes (6): ApplicationInterface, Any, Result, Any, Path, Result

### Community 328 - "QueueDriver"
Cohesion: 0.24
Nodes (4): Exception, Result, QueueDriver, Contract for queue backend drivers. Sync, Database, and Cache drivers     implem

### Community 344 - "QueueWorker"
Cohesion: 0.22
Nodes (4): Any, Result, QueueWorker, Supervisor-managed Task that polls a queue driver and processes jobs     with re

### Community 347 - "QueueServiceProvider"
Cohesion: 0.27
Nodes (3): Any, Result, QueueServiceProvider

### Community 348 - "._dispatch_to_worker"
Cohesion: 0.29
Nodes (3): Task, TaskGraph, TaskInjector

### Community 349 - "TaskBuilderInterface"
Cohesion: 0.42
Nodes (4): ModuleType, ModuleLoader, Any, Result

### Community 351 - "Dictionary"
Cohesion: 0.31
Nodes (4): Configurable, _resolve_config_type(), Dictionary, Any

### Community 352 - "RegisteredRconClient"
Cohesion: 0.18
Nodes (5): Any, CommandResponse, Mixin adding registered RCON command dispatch to any client that     exposes a `, RegisteredRconClient, SendCommandProtocol

### Community 353 - "ErrorKindProtocol"
Cohesion: 0.29
Nodes (6): MANDATORY: Code Comment Conventions, MANDATORY: General Development Guidelines, MANDATORY: Git Rules, MANDATORY: Local Code Search/Traversal, MANDATORY: Use td for Task Management, MANDATORY: Worktree Management

### Community 354 - "LoginResponsePacket"
Cohesion: 0.21
Nodes (3): RequestMessage, KeepAlivePacket, UnknownPacket

### Community 356 - "__init__.py"
Cohesion: 0.13
Nodes (9): ABC, ContextualAttributeProtocol, PendingChain, Marker interface. Jobs that implement this are dispatched asynchronously     to, Stub for chained job dispatch. Full chaining support is deferred to a     later, ShouldQueue, ContextualAttribute, ContainerProtocol (+1 more)

### Community 358 - "Bind"
Cohesion: 0.25
Nodes (3): Bind, Scoped, Singleton

### Community 361 - ".execute"
Cohesion: 0.40
Nodes (3): _MasoniteModel, Model, Base ORM model for armaden applications.      Extends masoniteorm's Model, overr

### Community 363 - "Result"
Cohesion: 0.16
Nodes (4): DeferrableProvider, Any, Result, ServiceProvider

### Community 368 - "supervisor.py"
Cohesion: 0.50
Nodes (3): _result_error(), _run_shutdown(), SupervisorError

## Knowledge Gaps
- **27 isolated node(s):** `MANDATORY: Local Code Search/Traversal`, `MANDATORY: Use td for Task Management`, `MANDATORY: Worktree Management`, `MANDATORY: Code Comment Conventions`, `MANDATORY: Git Rules` (+22 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **259 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ArmaReforgerServerExecutable` connect `ArmaReforgerServerExecutable` to `.language`, `TaskThreadingPolicy`, `.log_rdb_checksum`, `.nwk_resolution`, `.rpl_encode_as_long_jobs`, `.scenario`, `.server_id`, `.streams_delta`, `.world`, `ABC`, `UrlGenerator`, `Error`, `SteamCmdExecutableFlag`, `.log_voting`, `.minidump`, `FilesystemServiceProvider`, `.nds`, `.profile`, `.no_backend`, `.keep_num_of_logs`, `DatabaseServiceProvider`, `.no_throw`, `.nwk_resolution`, `.region`, `.rpl_encode_as_long_jobs`, `.scenario`, `.single_threaded_update`, `.streaming_budget`, `.streams_delta`, `.vm_error_mode`, `.a2s`, `.addons_repair`, `.addons_verify`, `.backend_fresh_session`, `.custom`, `.debugger_port`, `.disable_ai`, `.disable_crash_reporter`, `.kind`, `.disable_shaders_build`, `.force_session_load`, `.freeze_check`, `.freeze_check_mode`, `.keep_num_of_logs`, `.limit_fps`, `.log_scr_checksum`, `.log_stats`, `.no_sound`, `.rcon`, `.rpl_timeout_ms`, `.staggering_budget`, `.force_session_load`, `.jobsys_short_worker_count`, `.keep_session_save`, `.log_rdb_checksum`?**
  _High betweenness centrality (0.108) - this node is a cross-community bridge._
- **Why does `ArmaReforgerExecutableError` connect `.kind` to `ArmaReforgerRconClient`?**
  _High betweenness centrality (0.103) - this node is a cross-community bridge._
- **Why does `InstanceContainer` connect `SelfBuildingTag` to `instance_container.py`, `.resolve_dependencies`, `ArmaReforgerRconClient`, `arma_reforger_server_executable.py`, `Bind`, `ContextualBindingBuilder`, `Config`, `Result`, `SupervisorInterface`, `RconCommandInterface`, `Supervisor`, `get_application`, `AppServiceProvider`, `ContextualAttribute`, `AbstractEventLoop`?**
  _High betweenness centrality (0.093) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `ErrorInterface` (e.g. with `CoreApplicationInterface` and `KernelInterface`) actually correct?**
  _`ErrorInterface` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Are the 30 inferred relationships involving `InstanceContainer` (e.g. with `Application` and `Config`) actually correct?**
  _`InstanceContainer` has 30 INFERRED edges - model-reasoned connections that need verification._
- **Are the 9 inferred relationships involving `Container` (e.g. with `BoundMethod` and `ContextualAttribute`) actually correct?**
  _`Container` has 9 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `ContainerMethodsProtocol` (e.g. with `ContextualBindingBuilderProtocol` and `ContainerProtocol`) actually correct?**
  _`ContainerMethodsProtocol` has 2 INFERRED edges - model-reasoned connections that need verification._