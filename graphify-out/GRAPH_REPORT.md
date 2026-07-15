# Graph Report - armaden  (2026-07-15)

## Corpus Check
- 191 files · ~33,900 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1778 nodes · 3009 edges · 314 communities (58 shown, 256 thin omitted)
- Extraction: 81% EXTRACTED · 19% INFERRED · 0% AMBIGUOUS · INFERRED: 572 edges (avg confidence: 0.55)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `a8ee621a`
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
- T
- Bind
- RconCommandInterface
- SupervisorRequestData
- PlayerResponseData
- AGENTS.md
- Application
- task.py
- LoginResponsePacket
- ServerMessageResponsePacket
- .resolve_primitive
- .kind
- .addon
- .addons_verify
- .ai_limit
- .backend_disable_storage
- .backend_local_storage
- Exception
- .disable_ai
- .freeze_check
- Kernel
- .jobsys_short_worker_count
- SteamCmdExecutableError
- .limit_fps
- GenericError
- .log_append
- .log_scr_checksum
- ConsoleServiceProvider
- .minidump
- .no_splash
- .player_limits
- .backend_fresh_session
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
- __init__.py
- __init__.py
- __init__.py
- __init__.py
- __main__.py
- .create_db
- .debugger
- __init__.py
- .disable_navmesh_streaming
- __init__.py
- .freeze_check
- .freeze_check_mode
- .disable_navmesh_streaming
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
- .keep_session_save
- .limit_fps
- .load_session_save
- .log_level
- .log_scr_checksum
- .log_stats
- .log_time
- .nds
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
- .addon_download_dir
- .script_authorize_all
- .staggering_budget
- .silent_crash_report
- .addons
- .disable_shaders_build
- CommandResponse
- RconCommandInterface
- .log_fs
- .region
- .scenario
- .streaming_budget
- RconCommandRepository
- async_datagram_transport.py
- ._resolve_parameter
- RegisteredRconClient
- .streams_delta
- .log_rdb_checksum
- .single_threaded_update
- Exception
- RconCommandInterface
- RconCommandRepository
- SendCommandProtocol

## God Nodes (most connected - your core abstractions)
1. `InstanceContainer` - 118 edges
2. `ArmaReforgerServerExecutable` - 86 edges
3. `Supervisor` - 52 edges
4. `Request` - 49 edges
5. `app()` - 41 edges
6. `CoreApplication` - 36 edges
7. `BattleEyeRconClient` - 33 edges
8. `TaskGraph` - 33 edges
9. `Task` - 31 edges
10. `TaskGraphCompiler` - 29 edges

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

## Communities (314 total, 256 thin omitted)

### Community 0 - "ArmaReforgerServerExecutable"
Cohesion: 0.13
Nodes (7): ArmaReforgerServerExecutable, Bind the server to specific addresses / ports.          Keyword Args:, Configure BattlEye / RCON remote console.          Keyword Args:             add, Force loading a session save even if version mismatched., Skip the initial load request and start a brand-new session., Limit the number of streams opened for a client (1..1000)., Threads for short jobs (capped to CPU count or 16).

### Community 6 - "BattleEyeRconServer"
Cohesion: 0.28
Nodes (12): A2SConfig, Config, GameConfig, GamePropertiesConfig, GamePropertiesPersistence, JoinQueueConfig, ModConfig, OperatingConfig (+4 more)

### Community 7 - "lifecycle_controller.py"
Cohesion: 0.08
Nodes (13): HealthStatus, GetAppStatus, Api, Controllers for API routes, LifecycleController, ApiResponseData, HealthResponseData, RestartRequestData (+5 more)

### Community 8 - "TaskThreadingPolicy"
Cohesion: 0.05
Nodes (21): HttpKernel, Middleware, MiddlewarePipeline, json_response(), JSONResponse, response(), ResponseFactory, ApiUser (+13 more)

### Community 9 - "RouteFacade"
Cohesion: 0.06
Nodes (18): Any, ServiceProvider, InstanceContainer, RconDiscoveryHook, DiscoveryHook, ApplicationError, ApplicationException, ApplicationStatus (+10 more)

### Community 12 - "HealthStatus"
Cohesion: 0.22
Nodes (3): Lifecycle, Pipeline, TaskRuntimeInterface

### Community 13 - "BattleEyeRconClient"
Cohesion: 0.09
Nodes (5): GraphTaskRuntime, _result_error(), _run_shutdown(), Supervisor, Semaphore

### Community 15 - "Packet"
Cohesion: 0.14
Nodes (10): Generator, GeneratorResult, _detect_poetry_package_path(), _fmt_list(), main(), _print_result(), # TODO: Register bindings on the service container., # TODO: Build and register tasks with the supervisor. (+2 more)

### Community 16 - "ConsoleKernel"
Cohesion: 0.08
Nodes (11): set_application(), ApplicationInterface, bootstrap_console(), bootstrap_http(), ConsoleKernel, HttpKernel, Kernel, RuntimeEntry (+3 more)

### Community 22 - "BoundMethod"
Cohesion: 0.16
Nodes (3): KeepAlivePacket, BattleEyeInvalidPacketException, ServerMessageResponsePacket

### Community 23 - "TaskGraph"
Cohesion: 0.19
Nodes (6): DuplicateTaskNameError, TaskGraphCycleError, UnresolvedDependencyError, TaskGraph, TaskGraphCompiler, _UnresolvedSentinel

### Community 24 - "AsyncDatagramTransport"
Cohesion: 0.08
Nodes (10): DatagramProtocol, DatagramTransport, Exception, entry(), main(), entry(), main(), AsyncDatagramTransport (+2 more)

### Community 25 - "UrlGenerator"
Cohesion: 0.08
Nodes (8): route(), URL, RequestContext, RouteNotFoundException, RouteParameterMissingException, UrlGenerator, auth(), request()

### Community 29 - "TaskRuntime"
Cohesion: 0.15
Nodes (4): Event, ProgressChannel, ProgressUpdate, TaskRuntime

### Community 33 - "WorkerPool"
Cohesion: 0.13
Nodes (4): get_class_for_callable(), get_contextual_attribute_from_dependency(), Determine the class name associated with a callable for build-stack tracking., BindingResolutionException

### Community 35 - "RestartPolicy"
Cohesion: 0.22
Nodes (7): RestartPolicy, _emit_banner(), TelemetryServiceProvider, CollectServerTelemetryTask, FormatTelemetryReportTask, TelemetryAlertTask, TelemetryReadinessProbeTask

### Community 36 - "env"
Cohesion: 0.14
Nodes (5): config(), env(), Facade for reading typed environment variables from the application., config(), config()

### Community 38 - "ContextualAttribute"
Cohesion: 0.16
Nodes (4): Config, Give, Tag, ContextualAttribute

### Community 42 - "RouteRegistrar"
Cohesion: 0.33
Nodes (5): MANDATORY: Code Comment Conventions, MANDATORY: Git Rules, MANDATORY: Local Code Search/Traversal, MANDATORY: Use td for Task Management, MANDATORY: Worktree Management

### Community 43 - "CommandResponse"
Cohesion: 0.16
Nodes (8): Client, ClientState, RequestMessage, ResponseMessage, LoginStatus, LoginRequestPacket, UnknownPacket, IntEnum

### Community 44 - "_LegacyTask"
Cohesion: 0.09
Nodes (3): __getattr__(), _LegacyTask, TaskBuilder

### Community 47 - "SubprocessHandle"
Cohesion: 0.18
Nodes (20): SupervisorRequestKind, TaskThreadingPolicy, SupervisorRequestInterface, _ExclusiveWorker, ProcessInfoData, RequestInfoData, _SharedWorker, SupervisorError (+12 more)

### Community 48 - "._initialize_configs"
Cohesion: 0.15
Nodes (5): Application, ApplicationBase, Application, DefaultApplication, Application

### Community 49 - "Message"
Cohesion: 0.08
Nodes (15): AbstractEventLoop, DatagramTransportFactory, datetime, LoginResponsePacket, Packet, ServerMessageRequestPacket, BattleEyeRconClient, ClientStatus (+7 more)

### Community 57 - "get_application"
Cohesion: 0.15
Nodes (7): Error, ErrorKindInterface, Enforces that any error type object has a code string and message string., Accepts any Enum instance that implements a .message property., ModuleLoader, ModuleLoaderError, ModuleType

### Community 59 - "URL"
Cohesion: 0.13
Nodes (3): ErrorInterface, CoreApplicationInterface, KernelInterface

### Community 62 - "ArmaDen"
Cohesion: 0.22
Nodes (8): ArmaDen, Build Locally, CLI Entrypoints, Install, Manual Application Setup, Packages, Run with Docker, Scaffold an Application

### Community 65 - "RconCommandInterface"
Cohesion: 0.11
Nodes (6): ABC, Configurable, _resolve_config_type(), Controller, DeferrableProvider, ServiceProvider

### Community 66 - "SupervisorRequestData"
Cohesion: 0.39
Nodes (3): SupervisorRequestData, RestartAppService, ShutdownAppService

### Community 68 - "AGENTS.md"
Cohesion: 0.25
Nodes (3): Bind, Scoped, Singleton

### Community 69 - "Application"
Cohesion: 0.08
Nodes (19): ArmaReforgerRconClient, ArmaReforgerServerConfig, BattleEyeRconClient, FastAPI, RegisteredRconClient, RegistersRconCommand, Result, Self (+11 more)

### Community 71 - "LoginResponsePacket"
Cohesion: 0.33
Nodes (3): PlayerResponseData, Parse a single data row from ``players`` output.          Returns ``None``  if t, A connected player returned by the ``players`` command.

### Community 72 - "ServerMessageResponsePacket"
Cohesion: 0.33
Nodes (3): ArmaReforgerExecutableFlag, ArmaReforgerExecutableFlagError, Arma Reforger CLI startup flags.

### Community 73 - ".resolve_primitive"
Cohesion: 0.13
Nodes (11): BoundMethod, get_parameter_class_name(), is_parameter_required(), Utility helpers shared between the container and bound-method resolution., resolve_string_to_class(), unwrap_if_closure(), CircularDependencyException, EntryNotFoundException (+3 more)

### Community 79 - ".backend_disable_storage"
Cohesion: 0.29
Nodes (4): APIRouter, RouteCompiler, RouteParameter, HttpKernel

### Community 81 - "Exception"
Cohesion: 0.47
Nodes (3): ArmaReforgerExecutableError, Config, Arma Reforger dedicated server wrapper.  Provides a typed, fluent interface for

### Community 86 - "SteamCmdExecutableError"
Cohesion: 0.47
Nodes (3): SteamCmd — Python wrapper for the steamcmd CLI tool., Config, SteamCmdExecutableError

### Community 291 - "Future"
Cohesion: 0.11
Nodes (11): Future, RconCommandRepository, Any, CommandResponse, Mixin adding registered RCON command dispatch to any client that     exposes a `, RegisteredRconClient, Any, CommandResponse (+3 more)

### Community 309 - "._resolve_parameter"
Cohesion: 0.22
Nodes (3): RconPacketInterface, DatagramTransportInterface, Protocol

### Community 310 - "RegisteredRconClient"
Cohesion: 0.10
Nodes (16): RconCommandInterface, BanCreateCommand, Any, BanListCommand, Any, BanRemoveCommand, Any, IdCommand (+8 more)

## Knowledge Gaps
- **15 isolated node(s):** `MANDATORY: Local Code Search/Traversal`, `MANDATORY: Use td for Task Management`, `MANDATORY: Worktree Management`, `MANDATORY: Code Comment Conventions`, `MANDATORY: Git Rules` (+10 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **256 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ArmaReforgerServerExecutable` connect `ArmaReforgerServerExecutable` to `SteamCmdExecutable`, `.keep_num_of_logs`, `.no_throw`, `.server_id`, `.generate_shaders`, `.keep_session_save`, `HealthStatus`, `.limit_fps`, `.load_session_save`, `.log_scr_checksum`, `.log_stats`, `.generate`, `.log_time`, `.nds`, `.no_sound`, `.language`, `.nwk_resolution`, `.load_session_save`, `.log_append`, `.logs_dir`, `.server_world`, `.log_level`, `.no_splash`, `__init__.py`, `__init__.py`, `__init__.py`, `__init__.py`, `__main__.py`, `.create_db`, `.debugger`, `.addon_download_dir`, `.disable_navmesh_streaming`, `.addons`, `__init__.py`, `.disable_shaders_build`, `.freeze_check`, `.freeze_check_mode`, `CommandResponse`, `.log_fs`, `.profile`, `.region`, `.scenario`, `.streaming_budget`, `.disable_navmesh_streaming`, `.rpl_encode_as_long_jobs`, `TypedDict`, `.streams_delta`, `.log_rdb_checksum`, `.single_threaded_update`, `Dictionary`, `.script_authorize_all`, `__init__.py`, `.staggering_budget`, `.kind`, `.addons_verify`, `.ai_limit`, `.silent_crash_report`, `.backend_local_storage`, `Exception`, `.disable_ai`, `.freeze_check`, `.jobsys_short_worker_count`, `.limit_fps`, `.log_append`, `.log_scr_checksum`, `ConsoleServiceProvider`, `.minidump`, `.player_limits`, `.backend_fresh_session`, `.scenario`, `.server_id`, `.silent_crash_report`, `.single_threaded_update`, `.vm_error_mode`?**
  _High betweenness centrality (0.163) - this node is a cross-community bridge._
- **Why does `InstanceContainer` connect `InstanceContainer` to `WorkerPool`, `AuthManager`, `.get_alias`, `RconCommandInterface`, `ContextualAttribute`, `.resolve_primitive`, `BattleEyeRconClient`, `SubprocessHandle`, `._initialize_configs`, `.resolve`?**
  _High betweenness centrality (0.138) - this node is a cross-community bridge._
- **Why does `TaskRuntimeInterface` connect `HealthStatus` to `ArmaReforgerServerExecutable`, `RestartPolicy`, `CoreApplication`, `Exception`, `._resolve_parameter`, `TaskBuilderInterface`, `TaskGraph`, `Path`?**
  _High betweenness centrality (0.102) - this node is a cross-community bridge._
- **Are the 20 inferred relationships involving `InstanceContainer` (e.g. with `Application` and `Config`) actually correct?**
  _`InstanceContainer` has 20 INFERRED edges - model-reasoned connections that need verification._
- **Are the 5 inferred relationships involving `ArmaReforgerServerExecutable` (e.g. with `Executable` and `Dictionary`) actually correct?**
  _`ArmaReforgerServerExecutable` has 5 INFERRED edges - model-reasoned connections that need verification._
- **Are the 15 inferred relationships involving `Supervisor` (e.g. with `SupervisorRequestData` and `SupervisorRequestKind`) actually correct?**
  _`Supervisor` has 15 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Mixin adding registered RCON command dispatch to any client that     exposes a ``, `MANDATORY: Local Code Search/Traversal`, `MANDATORY: Use td for Task Management` to the rest of the system?**
  _108 weakly-connected nodes found - possible documentation gaps or missing edges._