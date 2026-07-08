# Graph Report - armaden  (2026-07-08)

## Corpus Check
- 119 files · ~19,338 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1065 nodes · 2172 edges · 116 communities (45 shown, 71 thin omitted)
- Extraction: 89% EXTRACTED · 11% INFERRED · 0% AMBIGUOUS · INFERRED: 246 edges (avg confidence: 0.54)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `8ac53aca`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- IoC Container Binding
- Supervisor Request Handling
- Arma Reforger Server Config
- Application Kernel Interface
- App Facade Container
- Executable Argument Builder
- Task Lifecycle Management
- Async Datagram Transport
- Bound Method Resolution
- Application Health Status
- Core Application Bootstrap
- BattleEye RCON Server
- Console Kernel Bootstrap
- Scaffold File Generator
- BattleEye RCON Client
- Arma Server Task Runtime
- Server Path Configuration
- BattleEye Packet Protocol
- Framework Service Providers
- Typed Environment Config
- Login Packet Processing
- Datagram Packet Parsing
- FastAPI Default Application
- Module Discovery Loader
- Service Provider Registry
- Console HTTP Providers
- Command Request Packet
- Command Response Packet
- Server Message Packet
- Config Value Management
- Player Response Parsing
- Login Response Packet
- Server Message Response
- Type Discovery Provider
- App Lifecycle Callbacks
- Async Subprocess Dispatch
- Frontend Dependencies
- Steam Query Bind Address
- Server Addon Loader
- Addon Auto Repair Flag
- Server Auto Restart Flag
- Auto Shutdown Flag
- Local Backend Storage Flag
- Resource Database Regeneration
- Debugger Port Setting
- Force Session Load Flag
- Freeze Detection Timeout
- Freeze Behaviour Mode
- Crash File Retention Flag
- Log File Retention Limit
- Session Save Retention Flag
- Game Language Setting
- Server FPS Cap
- List Scenarios Flag
- Log Append Mode Flag
- Filesystem Logging Flag
- Log Verbosity Level
- .autoshutdown
- Error Dialog Suppression
- .backend_disable_storage
- .backend_local_storage
- .custom
- .debugger_port
- .disable_ai
- .disable_crash_reporter
- Global Streaming Budget
- .enable_night_grain
- Arma Games Module
- Scaffold CLI Tool
- App Config File
- Environment Variables File
- ArmaDen Core Package
- ArmaDen Documentation
- .freeze_check
- .jobsys_long_worker_count
- .keep_crash_files
- .keep_session_save
- .log_voting
- .nds
- .no_backend
- .nwk_resolution
- .rpl_encode_as_long_jobs
- .rpl_timeout_ms
- .server_id
- .silent_crash_report
- .single_threaded_update
- .staggering_budget
- .streams_delta
- .vm_error_mode
- Any
- Config
- Self
- WrapperTransportInterface
- ModuleLoader
- TypeDiscoveryServiceProvider
- Result
- Kernel
- .dispatch_subprocess
- InstanceContainer
- Parameter
- Any

## God Nodes (most connected - your core abstractions)
1. `InstanceContainer` - 104 edges
2. `ArmaReforgerServerExecutable` - 87 edges
3. `CoreApplication` - 40 edges
4. `app()` - 39 edges
5. `BattleEyeRconClient` - 38 edges
6. `Packet` - 31 edges
7. `BattleEyeRconServer` - 30 edges
8. `Supervisor` - 25 edges
9. `BattleEyeInvalidPacketException` - 25 edges
10. `AsyncDatagramTransport` - 25 edges

## Surprising Connections (you probably didn't know these)
- `Application` --uses--> `Application`  [INFERRED]
  user/bootstrap/application.py → src/armaden/framework/application.py
- `Build and Release Workflow` --references--> `armaden.framework.runtime`  [INFERRED]
  .github/workflows/build.yml → README.md
- `providers()` --references--> `ServiceProvider`  [EXTRACTED]
  user/bootstrap/providers.py → src/armaden/framework/classes/service_provider.py
- `Application` --uses--> `InstanceContainer`  [INFERRED]
  src/armaden/framework/application.py → src/armaden/framework/classes/instance_container.py
- `DeferrableProvider` --uses--> `InstanceContainer`  [INFERRED]
  src/armaden/framework/classes/service_provider.py → src/armaden/framework/classes/instance_container.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Application Bootstrap Entry-Point Flow** — armaden_framework_runtime, bootstrap_application, bootstrap_providers, app_providers_app_service_provider [EXTRACTED 0.95]
- **Task Registration Flow via ServiceProvider** — app_providers_app_service_provider, armaden_framework_classes_task, armaden_framework_facades, armaden_framework_classes_service_provider [EXTRACTED 0.90]

## Communities (116 total, 71 thin omitted)

### Community 0 - "IoC Container Binding"
Cohesion: 0.05
Nodes (12): Any, Exception, Parameter, BindingResolutionException, CircularDependencyException, ContextualAttribute, ContextualBindingBuilder, EntryNotFoundException (+4 more)

### Community 1 - "Supervisor Request Handling"
Cohesion: 0.11
Nodes (18): Future, SupervisorRequestArgs, SupervisorRequestData, SupervisorRequestKind, ProcessInfoData, AbstractEventLoop, Any, AsyncStreamCallback (+10 more)

### Community 2 - "Arma Reforger Server Config"
Cohesion: 0.07
Nodes (14): ArmaReforgerServerExecutable, Bind the server to specific addresses / ports.          Keyword Args:, Configure BattlEye / RCON remote console.          Keyword Args:             add, Cap the server frame rate., Load a server-side addon (mod) by ID.          May be called multiple times to l, Server region tag (used by the server browser)., Skip the initial load request and start a brand-new session., Maximum players per faction (``FactionKey:Number`` pairs). (+6 more)

### Community 3 - "Application Kernel Interface"
Cohesion: 0.06
Nodes (19): Protocol, Application, ErrorInterface, CoreApplicationInterface, KernelInterface, Any, Result, Result (+11 more)

### Community 4 - "App Facade Container"
Cohesion: 0.10
Nodes (9): C, app(), Any, config(), Any, get_application(), Self, Route (+1 more)

### Community 5 - "Executable Argument Builder"
Cohesion: 0.19
Nodes (4): Path, PushValue, Result, SteamCmdExecutable

### Community 6 - "Task Lifecycle Management"
Cohesion: 0.12
Nodes (6): Self, StatusCallback, TaskCallback, Task, TaskBuilder, TaskThreadingPolicy

### Community 7 - "Async Datagram Transport"
Cohesion: 0.13
Nodes (10): DatagramProtocol, DatagramTransport, entry(), main(), entry(), main(), AsyncDatagramTransport, Any (+2 more)

### Community 8 - "Bound Method Resolution"
Cohesion: 0.13
Nodes (4): AbstractEventLoop, DatagramTransportInterface, Exception, WrapperTransportInterface

### Community 9 - "Application Health Status"
Cohesion: 0.30
Nodes (11): A2SConfig, Config, GameConfig, GamePropertiesConfig, GamePropertiesPersistence, JoinQueueConfig, OperatingConfig, RconConfig (+3 more)

### Community 10 - "Core Application Bootstrap"
Cohesion: 0.11
Nodes (6): AbstractEventLoop, callable, CoreApplication, Any, Result, SupervisorInterface

### Community 11 - "BattleEye RCON Server"
Cohesion: 0.10
Nodes (13): IntEnum, BattleEyeRconServer, Client, ClientState, AbstractEventLoop, DatagramTransportFactory, datetime, Exception (+5 more)

### Community 12 - "Console Kernel Bootstrap"
Cohesion: 0.19
Nodes (7): set_application(), bootstrap_console(), bootstrap_http(), ConsoleKernel, HttpKernel, RuntimeEntry, TypedResult

### Community 13 - "Scaffold File Generator"
Cohesion: 0.14
Nodes (12): Generator, GeneratorResult, Path, _detect_poetry_package_path(), _fmt_list(), main(), _print_result(), Path (+4 more)

### Community 14 - "BattleEye RCON Client"
Cohesion: 0.11
Nodes (8): BattleEyeRconClient, Message, Any, datetime, Exception, # TODO: handle stateful messages (responses to sequenced messages), # TODO: implement event system, Self

### Community 15 - "Arma Server Task Runtime"
Cohesion: 0.09
Nodes (14): ArmaReforgerServerConfig, Result, Self, config(), env(), Any, Facade for reading typed environment variables from the application., ArmaReforgerServer (+6 more)

### Community 16 - "Server Path Configuration"
Cohesion: 0.09
Nodes (12): Path, Result, Path to a server configuration JSON file., Directory for profiles (saves, logs, settings).          The directory is create, Redirect log output to the given directory., Path to a session save to load on startup., Additional directories to search for mods.          Multiple directories can be, Directory where addons are downloaded. (+4 more)

### Community 17 - "BattleEye Packet Protocol"
Cohesion: 0.15
Nodes (4): CommandHeader, CommandResponsePacket, BattleEyeInvalidPacketException, Packet

### Community 18 - "Framework Service Providers"
Cohesion: 0.05
Nodes (31): AppServiceProvider, Application, ApplicationBase, armaden.framework, Application (ApplicationBase), ServiceProvider, TaskBuilder, armaden.framework.runtime (+23 more)

### Community 19 - "Typed Environment Config"
Cohesion: 0.05
Nodes (27): BoundMethod, Executable, Path, PushValue, Result, Self, Error, ErrorKindInterface (+19 more)

### Community 20 - "Login Packet Processing"
Cohesion: 0.20
Nodes (4): ClientStatus, AbstractEventLoop, DatagramTransportFactory, KeepAlivePacket

### Community 22 - "FastAPI Default Application"
Cohesion: 0.19
Nodes (4): DeferrableProvider, Any, Result, ServiceProvider

### Community 23 - "Module Discovery Loader"
Cohesion: 0.11
Nodes (17): app() facade, HealthStatus, GetAppStatus, RestartAppService, ShutdownAppService, Api, Any, Controllers for API routes (+9 more)

### Community 24 - "Service Provider Registry"
Cohesion: 0.25
Nodes (6): ABC, Configurable, _resolve_config_type(), ApplicationInterface, Any, Result

### Community 25 - "Console HTTP Providers"
Cohesion: 0.23
Nodes (6): FastAPI, TaskRuntimeInterface, DefaultApi, DefaultApiError, Any, Result

### Community 30 - "Player Response Parsing"
Cohesion: 0.33
Nodes (4): PlayerResponseData, Self, Parse a single data row from ``players`` output.          Returns ``None``  if t, A connected player returned by the ``players`` command.

### Community 107 - "WrapperTransportInterface"
Cohesion: 0.24
Nodes (7): ApplicationError, ApplicationStatus, ArmaReforgerExecutableFlag, ArmaReforgerExecutableFlagError, Result, Arma Reforger CLI startup flags., StrEnum

### Community 108 - "ModuleLoader"
Cohesion: 0.31
Nodes (5): SteamCMD CLI command flags (prefixed with ``+``)., SteamCmdExecutableFlag, SteamCmd — Python wrapper for the steamcmd CLI tool., Config, SteamCmdExecutableError

### Community 109 - "TypeDiscoveryServiceProvider"
Cohesion: 0.43
Nodes (4): ArmaReforgerRconClient, ArmaReforgerExecutableError, Config, Arma Reforger dedicated server wrapper.  Provides a typed, fluent interface for

### Community 112 - ".dispatch_subprocess"
Cohesion: 0.50
Nodes (3): AsyncStreamCallback, Path, Result

## Knowledge Gaps
- **8 isolated node(s):** `armaden`, `ArmaDen README`, `Build and Release Workflow`, `armaden.games`, `config/app.py` (+3 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **71 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ArmaReforgerServerExecutable` connect `Arma Reforger Server Config` to `Executable Argument Builder`, `Server Path Configuration`, `Typed Environment Config`, `Console HTTP Providers`, `Command Response Packet`, `Config Value Management`, `Server Message Response`, `Type Discovery Provider`, `App Lifecycle Callbacks`, `Async Subprocess Dispatch`, `Frontend Dependencies`, `Steam Query Bind Address`, `Server Addon Loader`, `Addon Auto Repair Flag`, `Server Auto Restart Flag`, `Auto Shutdown Flag`, `Local Backend Storage Flag`, `Resource Database Regeneration`, `Debugger Port Setting`, `Force Session Load Flag`, `Freeze Detection Timeout`, `Freeze Behaviour Mode`, `Crash File Retention Flag`, `Log File Retention Limit`, `Game Language Setting`, `Server FPS Cap`, `List Scenarios Flag`, `Log Append Mode Flag`, `Filesystem Logging Flag`, `Log Verbosity Level`, `.autoshutdown`, `Error Dialog Suppression`, `.backend_disable_storage`, `.backend_local_storage`, `.custom`, `.debugger_port`, `.disable_ai`, `.disable_crash_reporter`, `Global Streaming Budget`, `.enable_night_grain`, `.freeze_check`, `.jobsys_long_worker_count`, `.keep_crash_files`, `.keep_session_save`, `.log_voting`, `.nds`, `.no_backend`, `.nwk_resolution`, `.rpl_encode_as_long_jobs`, `.rpl_timeout_ms`, `.server_id`, `.silent_crash_report`, `.single_threaded_update`, `.staggering_budget`, `.streams_delta`, `.vm_error_mode`, `TypeDiscoveryServiceProvider`?**
  _High betweenness centrality (0.286) - this node is a cross-community bridge._
- **Why does `InstanceContainer` connect `IoC Container Binding` to `WrapperTransportInterface`, `Core Application Bootstrap`, `Application Kernel Interface`, `FastAPI Default Application`?**
  _High betweenness centrality (0.160) - this node is a cross-community bridge._
- **Why does `ServiceProvider` connect `FastAPI Default Application` to `IoC Container Binding`, `Core Application Bootstrap`, `WrapperTransportInterface`, `Framework Service Providers`, `Service Provider Registry`?**
  _High betweenness centrality (0.154) - this node is a cross-community bridge._
- **Are the 7 inferred relationships involving `InstanceContainer` (e.g. with `Application` and `DeferrableProvider`) actually correct?**
  _`InstanceContainer` has 7 INFERRED edges - model-reasoned connections that need verification._
- **Are the 5 inferred relationships involving `ArmaReforgerServerExecutable` (e.g. with `Executable` and `TaskRuntimeInterface`) actually correct?**
  _`ArmaReforgerServerExecutable` has 5 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `CoreApplication` (e.g. with `InstanceContainer` and `ServiceProvider`) actually correct?**
  _`CoreApplication` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `armaden`, `Accepts any Enum instance that implements a .message property.`, `Enforces that any error type object has a code string and message string.` to the rest of the system?**
  _100 weakly-connected nodes found - possible documentation gaps or missing edges._