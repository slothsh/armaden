# Graph Report - armaden  (2026-07-07)

## Corpus Check
- 119 files · ~19,092 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1050 nodes · 2155 edges · 111 communities (42 shown, 69 thin omitted)
- Extraction: 89% EXTRACTED · 11% INFERRED · 0% AMBIGUOUS · INFERRED: 245 edges (avg confidence: 0.54)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `770ac369`
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

## God Nodes (most connected - your core abstractions)
1. `InstanceContainer` - 93 edges
2. `ArmaReforgerServerExecutable` - 87 edges
3. `app()` - 39 edges
4. `CoreApplication` - 38 edges
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
- `ConsoleServiceProvider` --uses--> `ServiceProvider`  [INFERRED]
  src/armaden/framework/runtime/providers/console_service_provider.py → src/armaden/framework/classes/service_provider.py
- `HttpServiceProvider` --uses--> `ServiceProvider`  [INFERRED]
  src/armaden/framework/runtime/providers/http_service_provider.py → src/armaden/framework/classes/service_provider.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Application Bootstrap Entry-Point Flow** — armaden_framework_runtime, bootstrap_application, bootstrap_providers, app_providers_app_service_provider [EXTRACTED 0.95]
- **Task Registration Flow via ServiceProvider** — app_providers_app_service_provider, armaden_framework_classes_task, armaden_framework_facades, armaden_framework_classes_service_provider [EXTRACTED 0.90]

## Communities (111 total, 69 thin omitted)

### Community 0 - "IoC Container Binding"
Cohesion: 0.06
Nodes (5): BindingResolutionException, ContextualBindingBuilder, InstanceContainer, Any, Parameter

### Community 1 - "Supervisor Request Handling"
Cohesion: 0.10
Nodes (21): Future, SupervisorRequestArgs, SupervisorRequestData, SupervisorRequestKind, Any, StrEnum, SupervisorRequestInterface, ProcessInfoData (+13 more)

### Community 2 - "Arma Reforger Server Config"
Cohesion: 0.07
Nodes (14): ArmaReforgerServerExecutable, Bind the server to specific addresses / ports.          Keyword Args:, Configure BattlEye / RCON remote console.          Keyword Args:             add, Cap the server frame rate., Load a server-side addon (mod) by ID.          May be called multiple times to l, Server region tag (used by the server browser)., Skip the initial load request and start a brand-new session., Maximum players per faction (``FactionKey:Number`` pairs). (+6 more)

### Community 3 - "Application Kernel Interface"
Cohesion: 0.06
Nodes (16): Protocol, Application, ErrorInterface, CoreApplicationInterface, KernelInterface, Any, Result, Result (+8 more)

### Community 4 - "App Facade Container"
Cohesion: 0.10
Nodes (9): C, app(), Any, config(), Any, get_application(), Self, Route (+1 more)

### Community 5 - "Executable Argument Builder"
Cohesion: 0.08
Nodes (18): FastAPI, AsyncStreamCallback, Path, Result, TaskRuntimeInterface, DefaultApi, DefaultApiError, Any (+10 more)

### Community 6 - "Task Lifecycle Management"
Cohesion: 0.19
Nodes (4): StatusCallback, TaskCallback, Task, TaskThreadingPolicy

### Community 7 - "Async Datagram Transport"
Cohesion: 0.13
Nodes (10): DatagramProtocol, DatagramTransport, entry(), main(), entry(), main(), AsyncDatagramTransport, Any (+2 more)

### Community 8 - "Bound Method Resolution"
Cohesion: 0.10
Nodes (23): ABC, Exception, BoundMethod, Configurable, _resolve_config_type(), CircularDependencyException, EntryNotFoundException, LogicException (+15 more)

### Community 9 - "Application Health Status"
Cohesion: 0.18
Nodes (15): ArmaReforgerRconClient, A2SConfig, Config, GameConfig, GamePropertiesConfig, GamePropertiesPersistence, JoinQueueConfig, OperatingConfig (+7 more)

### Community 10 - "Core Application Bootstrap"
Cohesion: 0.07
Nodes (18): AbstractEventLoop, callable, InstanceContainer, Any, Result, ServiceProvider, ApplicationError, ApplicationException (+10 more)

### Community 11 - "BattleEye RCON Server"
Cohesion: 0.10
Nodes (13): IntEnum, BattleEyeRconServer, Client, ClientState, AbstractEventLoop, DatagramTransportFactory, datetime, Exception (+5 more)

### Community 12 - "Console Kernel Bootstrap"
Cohesion: 0.15
Nodes (9): set_application(), bootstrap_console(), bootstrap_http(), ConsoleKernel, HttpKernel, Kernel, Any, RuntimeEntry (+1 more)

### Community 13 - "Scaffold File Generator"
Cohesion: 0.14
Nodes (12): Generator, GeneratorResult, Path, _detect_poetry_package_path(), _fmt_list(), main(), _print_result(), Path (+4 more)

### Community 14 - "BattleEye RCON Client"
Cohesion: 0.11
Nodes (8): BattleEyeRconClient, Message, Any, datetime, Exception, # TODO: handle stateful messages (responses to sequenced messages), # TODO: implement event system, Self

### Community 15 - "Arma Server Task Runtime"
Cohesion: 0.09
Nodes (15): Any, ArmaReforgerServerConfig, Result, Self, config(), env(), Any, Facade for reading typed environment variables from the application. (+7 more)

### Community 16 - "Server Path Configuration"
Cohesion: 0.09
Nodes (12): Path, Result, Path to a server configuration JSON file., Directory for profiles (saves, logs, settings).          The directory is create, Redirect log output to the given directory., Path to a session save to load on startup., Additional directories to search for mods.          Multiple directories can be, Directory where addons are downloaded. (+4 more)

### Community 17 - "BattleEye Packet Protocol"
Cohesion: 0.15
Nodes (4): CommandHeader, CommandResponsePacket, BattleEyeInvalidPacketException, Packet

### Community 18 - "Framework Service Providers"
Cohesion: 0.07
Nodes (23): AppServiceProvider, Application, ApplicationBase, armaden.framework, Application (ApplicationBase), ServiceProvider, TaskBuilder, app() facade (+15 more)

### Community 19 - "Typed Environment Config"
Cohesion: 0.14
Nodes (8): Error, ErrorKindInterface, Enforces that any error type object has a code string and message string., Accepts any Enum instance that implements a .message property., GenericError, ModuleLoaderError, Dictionary, Any

### Community 20 - "Login Packet Processing"
Cohesion: 0.20
Nodes (4): ClientStatus, AbstractEventLoop, DatagramTransportFactory, KeepAlivePacket

### Community 22 - "FastAPI Default Application"
Cohesion: 0.21
Nodes (5): Executable, Path, PushValue, Result, Self

### Community 23 - "Module Discovery Loader"
Cohesion: 0.12
Nodes (16): HealthStatus, GetAppStatus, RestartAppService, ShutdownAppService, Api, Any, Controllers for API routes, LifecycleController (+8 more)

### Community 30 - "Player Response Parsing"
Cohesion: 0.33
Nodes (4): PlayerResponseData, Self, Parse a single data row from ``players`` output.          Returns ``None``  if t, A connected player returned by the ``players`` command.

### Community 107 - "WrapperTransportInterface"
Cohesion: 0.13
Nodes (4): AbstractEventLoop, DatagramTransportInterface, Exception, WrapperTransportInterface

### Community 108 - "ModuleLoader"
Cohesion: 0.27
Nodes (6): ModuleType, ModuleLoader, Any, Result, HttpServiceProvider, Result

### Community 109 - "TypeDiscoveryServiceProvider"
Cohesion: 0.43
Nodes (3): Result, TypeDiscoveryError, TypeDiscoveryServiceProvider

## Knowledge Gaps
- **8 isolated node(s):** `armaden`, `ArmaDen README`, `Build and Release Workflow`, `armaden.games`, `config/app.py` (+3 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **69 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ArmaReforgerServerExecutable` connect `Arma Reforger Server Config` to `Executable Argument Builder`, `Application Health Status`, `Server Path Configuration`, `Typed Environment Config`, `FastAPI Default Application`, `Console HTTP Providers`, `Command Response Packet`, `Config Value Management`, `Server Message Response`, `Type Discovery Provider`, `App Lifecycle Callbacks`, `Async Subprocess Dispatch`, `Frontend Dependencies`, `Steam Query Bind Address`, `Server Addon Loader`, `Addon Auto Repair Flag`, `Server Auto Restart Flag`, `Auto Shutdown Flag`, `Local Backend Storage Flag`, `Resource Database Regeneration`, `Debugger Port Setting`, `Force Session Load Flag`, `Freeze Detection Timeout`, `Freeze Behaviour Mode`, `Crash File Retention Flag`, `Log File Retention Limit`, `Game Language Setting`, `Server FPS Cap`, `List Scenarios Flag`, `Log Append Mode Flag`, `Filesystem Logging Flag`, `Log Verbosity Level`, `.autoshutdown`, `Error Dialog Suppression`, `.backend_disable_storage`, `.backend_local_storage`, `.custom`, `.debugger_port`, `.disable_ai`, `.disable_crash_reporter`, `Global Streaming Budget`, `.enable_night_grain`, `.freeze_check`, `.jobsys_long_worker_count`, `.keep_crash_files`, `.keep_session_save`, `.log_voting`, `.nds`, `.no_backend`, `.nwk_resolution`, `.rpl_encode_as_long_jobs`, `.rpl_timeout_ms`, `.server_id`, `.silent_crash_report`, `.single_threaded_update`, `.staggering_budget`, `.streams_delta`, `.vm_error_mode`?**
  _High betweenness centrality (0.290) - this node is a cross-community bridge._
- **Why does `InstanceContainer` connect `IoC Container Binding` to `Bound Method Resolution`, `Application Kernel Interface`?**
  _High betweenness centrality (0.149) - this node is a cross-community bridge._
- **Why does `Executable` connect `FastAPI Default Application` to `Arma Reforger Server Config`, `Executable Argument Builder`, `Bound Method Resolution`, `Application Health Status`, `Typed Environment Config`?**
  _High betweenness centrality (0.148) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `InstanceContainer` (e.g. with `Application` and `BoundMethod`) actually correct?**
  _`InstanceContainer` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Are the 5 inferred relationships involving `ArmaReforgerServerExecutable` (e.g. with `Executable` and `TaskRuntimeInterface`) actually correct?**
  _`ArmaReforgerServerExecutable` has 5 INFERRED edges - model-reasoned connections that need verification._
- **What connects `armaden`, `Accepts any Enum instance that implements a .message property.`, `Enforces that any error type object has a code string and message string.` to the rest of the system?**
  _100 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `IoC Container Binding` be split into smaller, more focused modules?**
  _Cohesion score 0.06315789473684211 - nodes in this community are weakly interconnected._