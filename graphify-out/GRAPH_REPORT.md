# Graph Report - armaden  (2026-09-03)

## Corpus Check
- 271 files · ~54,633 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1151 nodes · 1635 edges · 305 communities (59 shown, 246 thin omitted)
- Extraction: 86% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 225 edges (avg confidence: 0.56)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `4eadc1f1`
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
- SteamCmdExecutableError
- Executable
- DefaultApi
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
- FilesystemServiceProvider
- DefaultApplication
- .profile
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
- .no_splash
- TaskInjector
- UrlGenerator
- .player_limits
- CacheSerializer
- Error
- SteamCmdExecutableFlag
- .streaming_budget
- .log_voting
- .minidump
- Executable
- .nds
- .no_backend
- Future
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
- .single_threaded_update
- .streaming_budget
- .streams_delta
- .vm_error_mode
- arma_reforger_server_executable.py
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
1. `Container` - 109 edges
2. `ArmaReforgerServerExecutable` - 82 edges
3. `ContainerMethodsProtocol` - 81 edges
4. `BattleEyeRconClient` - 44 edges
5. `Supervisor` - 37 edges
6. `BattleEyeRconServer` - 29 edges
7. `CommandRequestPacket` - 26 edges
8. `AsyncDatagramTransport` - 26 edges
9. `CommandResponsePacket` - 25 edges
10. `ServerMessageRequestPacket` - 24 edges

## Surprising Connections (you probably didn't know these)
- `SupervisorRequestInfoData` --uses--> `SupervisorRequestKind`  [INFERRED]
  src/armaden/framework/runtime/supervisor/dto/request_info_data.py → src/armaden/framework/runtime/supervisor/enums/supervisor_request_kind.py
- `TaskStateData` --uses--> `TaskProtocol`  [INFERRED]
  src/armaden/framework/runtime/supervisor/dto/task_state_data.py → src/armaden/framework/runtime/supervisor/task/protocols/task_protocol.py
- `Container` --uses--> `BoundMethod`  [INFERRED]
  src/armaden/framework/runtime/container/container.py → src/armaden/framework/runtime/container/bound_method.py
- `Container` --uses--> `ContextualAttribute`  [INFERRED]
  src/armaden/framework/runtime/container/container.py → src/armaden/framework/runtime/container/contextual_attribute.py
- `Container` --uses--> `ContextualBindingBuilder`  [INFERRED]
  src/armaden/framework/runtime/container/container.py → src/armaden/framework/runtime/container/contextual_binding_builder.py

## Import Cycles
- None detected.

## Communities (305 total, 246 thin omitted)

### Community 0 - "ArmaReforgerServerExecutable"
Cohesion: 0.07
Nodes (15): Executable, ArmaReforgerServerExecutable, Unique server identifier., Disable storage loads and saves (online and local)., Skip splash screens on startup., Set the Steam Query Protocol bind IP address., Print scenario .conf file paths to the log on startup., Maximum players per faction (``FactionKey:Number`` pairs). (+7 more)

### Community 2 - "AuthManager"
Cohesion: 0.08
Nodes (3): ContainerInstanceProtocol, ContainerProtocol, Container

### Community 7 - "lifecycle_controller.py"
Cohesion: 0.08
Nodes (14): GetAppStatus, RestartAppService, ShutdownAppService, Api, Controllers for API routes, LifecycleController, ApiResponseData, HealthResponseData (+6 more)

### Community 8 - "TaskThreadingPolicy"
Cohesion: 0.09
Nodes (14): Path, Result, TaskRuntimeInterface, Path to a server configuration JSON file., Directory for profiles (saves, logs, settings).          The directory is create, Redirect log output to the given directory., Path to a session save to load on startup., Additional directories to search for mods.          Multiple directories can be (+6 more)

### Community 10 - "Supervisor"
Cohesion: 0.21
Nodes (4): CallbackReference, Parameter, Reflection, TypeGuard

### Community 14 - "app"
Cohesion: 0.13
Nodes (6): TaskThreadingPolicy, Self, TaskBuilderInterface, TaskProtocol, TaskCallback, TaskStatusCallback

### Community 17 - ".generate"
Cohesion: 0.08
Nodes (10): BanCreateCommand, BanListCommand, BanRemoveCommand, IdCommand, KickCommand, LogoutCommand, PlayersCommand, RestartCommand (+2 more)

### Community 22 - "BoundMethod"
Cohesion: 0.12
Nodes (3): KeepAlivePacket, LoginRequestPacket, BattleEyeInvalidPacketException

### Community 24 - "AsyncDatagramTransport"
Cohesion: 0.14
Nodes (5): ContextualBindingBuilderProtocol, Self, ContextualBindingBuilderProtocol, ContextualBindingBuilder, ContainerProtocol

### Community 28 - "HttpServiceProvider"
Cohesion: 0.08
Nodes (17): Any, ArmaReforgerRconClient, ArmaReforgerServerConfig, CoroutineType, RconCommandInterface, RconCommandRepository, RegistersRconCommand, Result (+9 more)

### Community 31 - "ProcessBuilder"
Cohesion: 0.05
Nodes (27): AbstractEventLoop, Container, Future, GraphTaskRuntime, Semaphore, ProcessInfoData, TaskStateData, ThreadInfoData (+19 more)

### Community 35 - "RestartPolicy"
Cohesion: 0.14
Nodes (8): AppServiceProvider, _emit_banner(), TelemetryServiceProvider, CollectServerTelemetryTask, FormatTelemetryReportTask, TelemetryAlertTask, TelemetryReadinessProbeTask, providers()

### Community 45 - "_BuiltTask"
Cohesion: 0.09
Nodes (3): Exception, DatagramTransportInterface, WrapperTransportInterface

### Community 48 - "._initialize_configs"
Cohesion: 0.15
Nodes (7): DatagramProtocol, DatagramTransport, entry(), main(), entry(), main(), AsyncDatagramTransport

### Community 49 - "Message"
Cohesion: 0.21
Nodes (4): ExclusiveWorker, WorkerPool, SharedWorker, Worker

### Community 50 - "BoundMethod"
Cohesion: 0.25
Nodes (5): BoundMethodProtocol, Signature, BoundMethod, ContainerProtocol, Parameter

### Community 56 - "ContextualAttribute"
Cohesion: 0.33
Nodes (5): ABC, ContextualAttributeProtocol, ContextualAttribute, ContainerProtocol, Parameter

### Community 58 - "AppServiceProvider"
Cohesion: 0.28
Nodes (12): A2SConfig, Config, GameConfig, GamePropertiesConfig, GamePropertiesPersistence, JoinQueueConfig, ModConfig, OperatingConfig (+4 more)

### Community 59 - "URL"
Cohesion: 0.06
Nodes (14): RconPacketInterface, Protocol, ErrorProtocol, BoundMethodProtocol, ContainerDunderProtocol, ContainerInstanceProtocol, ContainerProtocol, ContextualAttributeProtocol (+6 more)

### Community 62 - "ArmaDen"
Cohesion: 0.22
Nodes (8): ArmaDen, Build Locally, CLI Entrypoints, Install, Manual Application Setup, Packages, Run with Docker, Scaffold an Application

### Community 63 - ".instance"
Cohesion: 0.29
Nodes (3): CircularDependencyException, EntryNotFoundException, LogicException

### Community 67 - "StrEnum"
Cohesion: 0.20
Nodes (6): ArmaReforgerExecutableFlag, ArmaReforgerExecutableFlagError, Arma Reforger CLI startup flags., SteamCMD CLI command flags (prefixed with ``+``)., SteamCmdExecutableFlag, StrEnum

### Community 68 - "arma_reforger_server_executable.py"
Cohesion: 0.33
Nodes (3): Config, ArmaReforgerExecutableError, Arma Reforger dedicated server wrapper.  Provides a typed, fluent interface for

### Community 70 - "Config"
Cohesion: 0.47
Nodes (3): SteamCmd — Python wrapper for the steamcmd CLI tool., Config, SteamCmdExecutableError

### Community 71 - "LoginResponsePacket"
Cohesion: 0.33
Nodes (3): PlayerResponseData, Parse a single data row from ``players`` output.          Returns ``None``  if t, A connected player returned by the ``players`` command.

### Community 72 - "SupervisorRequestKind"
Cohesion: 0.47
Nodes (4): SupervisorRequestArgs, SupervisorRequestData, SupervisorRequestInfoData, SupervisorRequestKind

### Community 75 - ".addon"
Cohesion: 0.14
Nodes (7): BattleEyeRconServer, Client, ClientState, ResponseMessage, LoginStatus, LoginResponsePacket, IntEnum

### Community 86 - "SteamCmdExecutableError"
Cohesion: 0.20
Nodes (8): ClientStatus, CommandResponse, Message, _PendingCommand, ServerMessage, CommandHeader, CommandResponsePacket, TransportNotConnectedException

### Community 92 - "Executable"
Cohesion: 0.19
Nodes (3): RequestMessage, ServerMessageResponsePacket, UnknownPacket

### Community 125 - "AbstractEventLoop"
Cohesion: 0.33
Nodes (5): MANDATORY: Code Comment Conventions, MANDATORY: Git Rules, MANDATORY: Local Code Search/Traversal, MANDATORY: Use td for Task Management, MANDATORY: Worktree Management

## Knowledge Gaps
- **26 isolated node(s):** `TaskRecordData`, `MultiImplementationTag`, `armaden`, `IdCommand`, `LoginCommand` (+21 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **246 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ArmaReforgerServerExecutable` connect `ArmaReforgerServerExecutable` to `.language`, `TaskThreadingPolicy`, `.log_rdb_checksum`, `.nwk_resolution`, `.rpl_encode_as_long_jobs`, `.scenario`, `.server_id`, `.streams_delta`, `.world`, `ABC`, `UrlGenerator`, `Error`, `SteamCmdExecutableFlag`, `.log_voting`, `.minidump`, `FilesystemServiceProvider`, `.nds`, `.profile`, `.no_backend`, `.keep_num_of_logs`, `DatabaseServiceProvider`, `.no_throw`, `.nwk_resolution`, `.region`, `.rpl_encode_as_long_jobs`, `.scenario`, `.single_threaded_update`, `.streaming_budget`, `.streams_delta`, `.vm_error_mode`, `.a2s`, `.addons_repair`, `.addons_verify`, `arma_reforger_server_executable.py`, `.backend_fresh_session`, `.debugger_port`, `.disable_ai`, `.custom`, `.disable_crash_reporter`, `.disable_shaders_build`, `.force_session_load`, `.freeze_check`, `.freeze_check_mode`, `.keep_num_of_logs`, `.limit_fps`, `.log_scr_checksum`, `.log_stats`, `.no_sound`, `.rcon`, `.rpl_timeout_ms`, `.staggering_budget`, `.force_session_load`, `.jobsys_short_worker_count`, `.keep_session_save`, `.log_rdb_checksum`?**
  _High betweenness centrality (0.184) - this node is a cross-community bridge._
- **Why does `Container` connect `AuthManager` to `.fire_after_resolving_callbacks`, `SelfBuildingTag`, `ServiceProvider`, `BoundMethod`, `.get_alias`, `.bound`, `.resolve`, `.make`, `AsyncDatagramTransport`, `ContextualAttribute`, `.instance`?**
  _High betweenness centrality (0.144) - this node is a cross-community bridge._
- **Why does `ArmaReforgerExecutableError` connect `arma_reforger_server_executable.py` to `StrEnum`?**
  _High betweenness centrality (0.126) - this node is a cross-community bridge._
- **Are the 9 inferred relationships involving `Container` (e.g. with `BoundMethod` and `ContextualAttribute`) actually correct?**
  _`Container` has 9 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `ContainerMethodsProtocol` (e.g. with `ContextualBindingBuilderProtocol` and `ContainerProtocol`) actually correct?**
  _`ContainerMethodsProtocol` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Are the 12 inferred relationships involving `BattleEyeRconClient` (e.g. with `CommandRequestPacket` and `CommandHeader`) actually correct?**
  _`BattleEyeRconClient` has 12 INFERRED edges - model-reasoned connections that need verification._
- **What connects `TaskRecordData`, `MultiImplementationTag`, `armaden` to the rest of the system?**
  _109 weakly-connected nodes found - possible documentation gaps or missing edges._