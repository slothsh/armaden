# Graph Report - armaden  (2026-07-12)

## Corpus Check
- 191 files · ~33,729 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1770 nodes · 2991 edges · 319 communities (61 shown, 258 thin omitted)
- Extraction: 81% EXTRACTED · 19% INFERRED · 0% AMBIGUOUS · INFERRED: 572 edges (avg confidence: 0.55)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `07ac42a4`
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
- RconCommandInterface
- .merge
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
- .check_instance
- .disable_ai
- .freeze_check
- Kernel
- .jobsys_short_worker_count
- .keep_crash_files
- .limit_fps
- .list_scenarios
- .log_append
- .log_fs
- .log_scr_checksum
- ConsoleServiceProvider
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
- __init__.py
- __init__.py
- __init__.py
- __init__.py
- __main__.py
- __init__.py
- __init__.py
- __init__.py
- __init__.py
- __init__.py
- __init__.py
- .disable_crash_reporter
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
- SteamCmdExecutableFlag
- .freeze_check
- .freeze_check_mode
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
- .no_throw
- .nwk_resolution
- .player_limits
- .profile
- .language
- .logs_dir
- .server_world
- .single_threaded_update
- .streaming_budget
- .vm_error_mode
- TypedDict
- Executable
- ModuleLoader
- .rpl_encode_as_long_jobs
- Future
- .addon_download_dir
- .script_authorize_all
- .server_id
- .silent_crash_report
- .addons
- .autoshutdown
- .disable_shaders_build
- CommandResponse
- .keep_num_of_logs
- RconCommandInterface
- .log_fs
- .region
- .scenario
- .streaming_budget
- RconCommandRepository
- async_datagram_transport.py
- TaskBuilder
- ._resolve_parameter
- RegisteredRconClient
- .streams_delta
- .log_rdb_checksum
- .single_threaded_update
- Any
- CommandResponse
- Future
- .staggering_budget

## God Nodes (most connected - your core abstractions)
1. `InstanceContainer` - 118 edges
2. `ArmaReforgerServerExecutable` - 86 edges
3. `Supervisor` - 52 edges
4. `Request` - 49 edges
5. `app()` - 41 edges
6. `CoreApplication` - 36 edges
7. `TaskGraph` - 33 edges
8. `BattleEyeRconClient` - 31 edges
9. `Task` - 31 edges
10. `TaskGraphCompiler` - 29 edges

## Surprising Connections (you probably didn't know these)
- `Application` --uses--> `Application`  [INFERRED]
  user/bootstrap/application.py → src/armaden/framework/application.py
- `AppServiceProvider` --uses--> `ServiceProvider`  [INFERRED]
  user/app/providers/app_service_provider.py → src/armaden/framework/classes/service_provider.py
- `TelemetryServiceProvider` --uses--> `ServiceProvider`  [INFERRED]
  user/app/providers/telemetry_service_provider.py → src/armaden/framework/classes/service_provider.py
- `RestartAppService` --uses--> `SupervisorRequestData`  [INFERRED]
  user/app/http/actions/restart_app_service.py → src/armaden/framework/dto/supervisor_request_data.py
- `ShutdownAppService` --uses--> `SupervisorRequestData`  [INFERRED]
  user/app/http/actions/shutdown_app_service.py → src/armaden/framework/dto/supervisor_request_data.py

## Import Cycles
- None detected.

## Communities (319 total, 258 thin omitted)

### Community 0 - "ArmaReforgerServerExecutable"
Cohesion: 0.13
Nodes (7): ArmaReforgerServerExecutable, Bind the server to specific addresses / ports.          Keyword Args:, Configure BattlEye / RCON remote console.          Keyword Args:             add, Force loading a session save even if version mismatched., Skip the initial load request and start a brand-new session., Limit the number of streams opened for a client (1..1000)., Threads for short jobs (capped to CPU count or 16).

### Community 2 - "AuthManager"
Cohesion: 0.18
Nodes (5): GraphTaskRuntime, _result_error(), _run_shutdown(), WorkerPool, Semaphore

### Community 3 - "Protocol"
Cohesion: 0.26
Nodes (3): Lifecycle, Pipeline, TaskInjector

### Community 6 - "BattleEyeRconServer"
Cohesion: 0.17
Nodes (6): BattleEyeRconServer, Client, ClientState, ResponseMessage, LoginStatus, IntEnum

### Community 7 - "lifecycle_controller.py"
Cohesion: 0.06
Nodes (15): HealthStatus, GetAppStatus, Api, Controllers for API routes, LifecycleController, ApiResponseData, HealthResponseData, RestartRequestData (+7 more)

### Community 8 - "TaskThreadingPolicy"
Cohesion: 0.06
Nodes (21): HttpKernel, Middleware, MiddlewarePipeline, json_response(), JSONResponse, response(), ResponseFactory, ApiUser (+13 more)

### Community 9 - "RouteFacade"
Cohesion: 0.12
Nodes (3): CoreApplication, InstanceContainer, SupervisorInterface

### Community 11 - "CoreApplication"
Cohesion: 0.19
Nodes (3): Configurable, _resolve_config_type(), Dictionary

### Community 14 - "app"
Cohesion: 0.07
Nodes (6): config(), get_application(), app(), AppServiceProvider, Repository, T

### Community 15 - "Packet"
Cohesion: 0.14
Nodes (10): Generator, GeneratorResult, _detect_poetry_package_path(), _fmt_list(), main(), _print_result(), # TODO: Register bindings on the service container., # TODO: Build and register tasks with the supervisor. (+2 more)

### Community 16 - "ConsoleKernel"
Cohesion: 0.21
Nodes (7): set_application(), bootstrap_console(), bootstrap_http(), ConsoleKernel, HttpKernel, RuntimeEntry, TypedResult

### Community 17 - ".generate"
Cohesion: 0.16
Nodes (3): KeepAlivePacket, LoginResponsePacket, BattleEyeInvalidPacketException

### Community 20 - "TaskRuntimeInterface"
Cohesion: 0.30
Nodes (11): A2SConfig, Config, GameConfig, GamePropertiesConfig, GamePropertiesPersistence, JoinQueueConfig, OperatingConfig, RconConfig (+3 more)

### Community 21 - "route_compiler.py"
Cohesion: 0.06
Nodes (22): AbstractEventLoop, CommandHeader, CommandResponse, CommandResponsePacket, DatagramTransportFactory, datetime, Future, BattleEyeRconClient (+14 more)

### Community 22 - "BoundMethod"
Cohesion: 0.19
Nodes (3): RequestMessage, ServerMessageResponsePacket, UnknownPacket

### Community 23 - "TaskGraph"
Cohesion: 0.19
Nodes (6): DuplicateTaskNameError, TaskGraphCycleError, UnresolvedDependencyError, TaskGraph, TaskGraphCompiler, _UnresolvedSentinel

### Community 24 - "AsyncDatagramTransport"
Cohesion: 0.13
Nodes (8): DatagramProtocol, DatagramTransport, entry(), main(), entry(), main(), AsyncDatagramTransport, TransportNotConnectedException

### Community 25 - "UrlGenerator"
Cohesion: 0.08
Nodes (8): route(), URL, RequestContext, RouteNotFoundException, RouteParameterMissingException, UrlGenerator, auth(), request()

### Community 28 - "HttpServiceProvider"
Cohesion: 0.29
Nodes (4): Error, ErrorKindInterface, Enforces that any error type object has a code string and message string., Accepts any Enum instance that implements a .message property.

### Community 29 - "TaskRuntime"
Cohesion: 0.15
Nodes (4): Event, ProgressChannel, ProgressUpdate, TaskRuntime

### Community 33 - "WorkerPool"
Cohesion: 0.11
Nodes (7): get_class_for_callable(), get_contextual_attribute_from_dependency(), get_parameter_class_name(), is_parameter_required(), Utility helpers shared between the container and bound-method resolution., Determine the class name associated with a callable for build-stack tracking., unwrap_if_closure()

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

### Community 47 - "SubprocessHandle"
Cohesion: 0.16
Nodes (21): SupervisorRequestData, SupervisorRequestKind, TaskThreadingPolicy, SupervisorRequestInterface, _ExclusiveWorker, ProcessInfoData, RequestInfoData, _SharedWorker (+13 more)

### Community 49 - "TaskInjector"
Cohesion: 0.47
Nodes (3): ArmaReforgerExecutableError, Config, Arma Reforger dedicated server wrapper.  Provides a typed, fluent interface for

### Community 57 - "get_application"
Cohesion: 0.20
Nodes (4): ModuleLoader, ModuleLoaderError, providers(), ModuleType

### Community 59 - "URL"
Cohesion: 0.11
Nodes (5): ErrorInterface, CoreApplicationInterface, KernelInterface, RconPacketInterface, Protocol

### Community 62 - "ArmaDen"
Cohesion: 0.22
Nodes (8): ArmaDen, Build Locally, CLI Entrypoints, Install, Manual Application Setup, Packages, Run with Docker, Scaffold an Application

### Community 63 - "URL"
Cohesion: 0.47
Nodes (3): SteamCmd — Python wrapper for the steamcmd CLI tool., Config, SteamCmdExecutableError

### Community 68 - "AGENTS.md"
Cohesion: 0.25
Nodes (3): Bind, Scoped, Singleton

### Community 69 - "Application"
Cohesion: 0.10
Nodes (16): ArmaReforgerRconClient, ArmaReforgerServerConfig, BattleEyeRconClient, RegisteredRconClient, RegistersRconCommand, Result, Self, SendCommandProtocol (+8 more)

### Community 71 - "LoginResponsePacket"
Cohesion: 0.33
Nodes (3): PlayerResponseData, Parse a single data row from ``players`` output.          Returns ``None``  if t, A connected player returned by the ``players`` command.

### Community 72 - "ServerMessageResponsePacket"
Cohesion: 0.33
Nodes (3): ArmaReforgerExecutableFlag, ArmaReforgerExecutableFlagError, Arma Reforger CLI startup flags.

### Community 73 - ".resolve_primitive"
Cohesion: 0.14
Nodes (9): Exception, BoundMethod, resolve_string_to_class(), BindingResolutionException, CircularDependencyException, EntryNotFoundException, LogicException, MultiImplementation (+1 more)

### Community 79 - ".backend_disable_storage"
Cohesion: 0.25
Nodes (4): APIRouter, RouteCompiler, RouteParameter, HttpKernel

### Community 81 - ".check_instance"
Cohesion: 0.24
Nodes (4): Any, RconCommandInterface, SendCommandProtocol, RegistersRconCommand

### Community 86 - ".keep_crash_files"
Cohesion: 0.24
Nodes (4): DiscoveryHook, Result, TypeDiscoveryError, TypeDiscoveryServiceProvider

### Community 96 - ".region"
Cohesion: 0.27
Nodes (4): RconCommandRepository, InstanceContainer, RconDiscoveryHook, Result

### Community 165 - "__init__.py"
Cohesion: 0.38
Nodes (5): ServiceProvider, ApplicationError, ApplicationException, ApplicationStatus, RconServiceProvider

### Community 310 - "RegisteredRconClient"
Cohesion: 0.10
Nodes (16): RconCommandInterface, BanCreateCommand, Any, BanListCommand, Any, BanRemoveCommand, Any, IdCommand (+8 more)

## Knowledge Gaps
- **15 isolated node(s):** `MANDATORY: Local Code Search/Traversal`, `MANDATORY: Use td for Task Management`, `MANDATORY: Worktree Management`, `MANDATORY: Code Comment Conventions`, `MANDATORY: Git Rules` (+10 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **258 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ArmaReforgerServerExecutable` connect `ArmaReforgerServerExecutable` to `SteamCmdExecutable`, `.freeze_check`, `.freeze_check_mode`, `.generate_shaders`, `CoreApplication`, `HealthStatus`, `.keep_session_save`, `.limit_fps`, `.load_session_save`, `.log_level`, `.log_scr_checksum`, `.log_stats`, `.log_time`, `.nds`, `.no_sound`, `.no_splash`, `.no_throw`, `.nwk_resolution`, `.language`, `.logs_dir`, `.profile`, `.single_threaded_update`, `.server_world`, `Exception`, `__init__.py`, `__init__.py`, `ModuleLoader`, `__init__.py`, `__main__.py`, `__init__.py`, `.addon_download_dir`, `__init__.py`, `__init__.py`, `.addons`, `__init__.py`, `__init__.py`, `.disable_crash_reporter`, `.autoshutdown`, `.disable_shaders_build`, `CommandResponse`, `.keep_num_of_logs`, `.log_fs`, `TaskInjector`, `.region`, `.scenario`, `.rpl_encode_as_long_jobs`, `TypedDict`, `.streaming_budget`, `.streams_delta`, `.log_rdb_checksum`, `.single_threaded_update`, `.staggering_budget`, `.vm_error_mode`, `.script_authorize_all`, `__init__.py`, `.server_id`, `.kind`, `.silent_crash_report`, `.ai_limit`, `.backend_local_storage`, `.disable_ai`, `.freeze_check`, `.jobsys_short_worker_count`, `.log_append`, `.log_scr_checksum`, `.minidump`, `.no_splash`, `.player_limits`, `.scenario`, `.server_id`, `.silent_crash_report`, `.single_threaded_update`, `.vm_error_mode`, `.disable_navmesh_streaming`?**
  _High betweenness centrality (0.147) - this node is a cross-community bridge._
- **Why does `InstanceContainer` connect `InstanceContainer` to `WorkerPool`, `AuthManager`, `.get_alias`, `ContextualAttribute`, `SupervisorInterface`, `.resolve_primitive`, `BattleEyeRconClient`, `SubprocessHandle`, `.resolve`, `TypedDict`, `._handle_multi_packet_response`?**
  _High betweenness centrality (0.107) - this node is a cross-community bridge._
- **Why does `TaskRuntimeInterface` connect `HealthStatus` to `ArmaReforgerServerExecutable`, `Protocol`, `RestartPolicy`, `lifecycle_controller.py`, `TaskInjector`, `TaskBuilderInterface`, `TaskGraph`, `Path`, `URL`?**
  _High betweenness centrality (0.101) - this node is a cross-community bridge._
- **Are the 20 inferred relationships involving `InstanceContainer` (e.g. with `Application` and `Config`) actually correct?**
  _`InstanceContainer` has 20 INFERRED edges - model-reasoned connections that need verification._
- **Are the 5 inferred relationships involving `ArmaReforgerServerExecutable` (e.g. with `Executable` and `Dictionary`) actually correct?**
  _`ArmaReforgerServerExecutable` has 5 INFERRED edges - model-reasoned connections that need verification._
- **Are the 15 inferred relationships involving `Supervisor` (e.g. with `SupervisorRequestData` and `SupervisorRequestKind`) actually correct?**
  _`Supervisor` has 15 INFERRED edges - model-reasoned connections that need verification._
- **What connects `MANDATORY: Local Code Search/Traversal`, `MANDATORY: Use td for Task Management`, `MANDATORY: Worktree Management` to the rest of the system?**
  _108 weakly-connected nodes found - possible documentation gaps or missing edges._