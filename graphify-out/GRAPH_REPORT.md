# Graph Report - armaden  (2026-07-07)

## Corpus Check
- 118 files · ~18,993 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1040 nodes · 2200 edges · 80 communities (43 shown, 37 thin omitted)
- Extraction: 87% EXTRACTED · 13% INFERRED · 0% AMBIGUOUS · INFERRED: 282 edges (avg confidence: 0.54)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `36bbc7e9`
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
- Error Dialog Suppression
- Global Streaming Budget
- Arma Games Module
- Scaffold CLI Tool
- App Config File
- Environment Variables File
- ArmaDen Core Package
- ArmaDen Documentation

## God Nodes (most connected - your core abstractions)
1. `ArmaReforgerServerExecutable` - 94 edges
2. `InstanceContainer` - 93 edges
3. `app()` - 39 edges
4. `CoreApplication` - 38 edges
5. `BattleEyeRconClient` - 38 edges
6. `TaskRuntimeInterface` - 33 edges
7. `Packet` - 31 edges
8. `BattleEyeRconServer` - 30 edges
9. `Supervisor` - 25 edges
10. `BattleEyeInvalidPacketException` - 25 edges

## Surprising Connections (you probably didn't know these)
- `AppServiceProvider` --uses--> `ServiceProvider`  [INFERRED]
  user/app/providers/app_service_provider.py → src/armaden/framework/classes/service_provider.py
- `Application` --uses--> `Application`  [INFERRED]
  user/bootstrap/application.py → src/armaden/framework/application.py
- `AppServiceProvider` --uses--> `TaskBuilder`  [INFERRED]
  user/app/providers/app_service_provider.py → src/armaden/framework/classes/task.py
- `AppServiceProvider` --uses--> `Config`  [INFERRED]
  user/app/providers/app_service_provider.py → src/armaden/games/arma_reforger/arma_reforger_server_config.py
- `Build and Release Workflow` --references--> `armaden.framework.runtime`  [INFERRED]
  .github/workflows/build.yml → README.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Application Bootstrap Entry-Point Flow** — armaden_framework_runtime, bootstrap_application, bootstrap_providers, app_providers_app_service_provider [EXTRACTED 0.95]
- **Task Registration Flow via ServiceProvider** — app_providers_app_service_provider, armaden_framework_classes_task, armaden_framework_facades, armaden_framework_classes_service_provider [EXTRACTED 0.90]

## Communities (80 total, 37 thin omitted)

### Community 1 - "Supervisor Request Handling"
Cohesion: 0.10
Nodes (21): Future, SupervisorRequestArgs, SupervisorRequestData, SupervisorRequestKind, Any, StrEnum, SupervisorRequestInterface, ProcessInfoData (+13 more)

### Community 2 - "Arma Reforger Server Config"
Cohesion: 0.02
Nodes (42): ArmaReforgerServerExecutable, Bind the server to specific addresses / ports.          Keyword Args:, Configure A2S query endpoint.          Keyword Args:             address: IP add, Configure BattlEye / RCON remote console.          Keyword Args:             add, Load a server-side addon (mod) by ID.          May be called multiple times to l, Load multiple addons at once.          Args:             mod_ids: Variable-lengt, Auto-restart the server when it crashes (default: ``True``)., Unique server identifier. (+34 more)

### Community 3 - "Application Kernel Interface"
Cohesion: 0.06
Nodes (16): Protocol, Application, ErrorInterface, CoreApplicationInterface, KernelInterface, Any, Result, Result (+8 more)

### Community 4 - "App Facade Container"
Cohesion: 0.09
Nodes (10): C, app(), Any, config(), Any, get_application(), Self, Route (+2 more)

### Community 5 - "Executable Argument Builder"
Cohesion: 0.08
Nodes (20): A2SConfig, GameConfig, GamePropertiesConfig, GamePropertiesPersistence, JoinQueueConfig, OperatingConfig, RconConfig, ServerConfig (+12 more)

### Community 6 - "Task Lifecycle Management"
Cohesion: 0.05
Nodes (17): Executable, Path, PushValue, Result, Self, Self, StatusCallback, TaskCallback (+9 more)

### Community 7 - "Async Datagram Transport"
Cohesion: 0.07
Nodes (14): DatagramProtocol, DatagramTransport, entry(), main(), entry(), main(), AsyncDatagramTransport, AbstractEventLoop (+6 more)

### Community 8 - "Bound Method Resolution"
Cohesion: 0.12
Nodes (17): Exception, BoundMethod, CircularDependencyException, ContextualBindingBuilder, EntryNotFoundException, LogicException, array_wrap(), get_class_for_callable() (+9 more)

### Community 9 - "Application Health Status"
Cohesion: 0.19
Nodes (13): Dictionary, Any, ArmaReforgerRconClient, ArmaReforgerServerError, ArmaReforgerServerException, Config, ArmaReforgerExecutableError, Config (+5 more)

### Community 10 - "Core Application Bootstrap"
Cohesion: 0.08
Nodes (14): AbstractEventLoop, callable, InstanceContainer, Any, Result, ServiceProvider, ApplicationError, ApplicationException (+6 more)

### Community 11 - "BattleEye RCON Server"
Cohesion: 0.13
Nodes (10): IntEnum, BattleEyeRconServer, Client, ClientState, AbstractEventLoop, DatagramTransportFactory, datetime, Exception (+2 more)

### Community 12 - "Console Kernel Bootstrap"
Cohesion: 0.11
Nodes (13): ABC, set_application(), ApplicationInterface, Any, Result, bootstrap_console(), bootstrap_http(), ConsoleKernel (+5 more)

### Community 13 - "Scaffold File Generator"
Cohesion: 0.14
Nodes (12): Generator, GeneratorResult, Path, _detect_poetry_package_path(), _fmt_list(), main(), _print_result(), Path (+4 more)

### Community 14 - "BattleEye RCON Client"
Cohesion: 0.11
Nodes (6): BattleEyeRconClient, ClientStatus, AbstractEventLoop, Any, DatagramTransportFactory, Exception

### Community 15 - "Arma Server Task Runtime"
Cohesion: 0.21
Nodes (5): TaskRuntimeInterface, ArmaReforgerServer, Any, Result, Self

### Community 16 - "Server Path Configuration"
Cohesion: 0.09
Nodes (12): Path, Result, Path to a server configuration JSON file., Directory for profiles (saves, logs, settings).          The directory is create, Redirect log output to the given directory., Path to a session save to load on startup., Additional directories to search for mods.          Multiple directories can be, Directory where addons are downloaded. (+4 more)

### Community 17 - "BattleEye Packet Protocol"
Cohesion: 0.20
Nodes (5): # TODO: handle stateful messages (responses to sequenced messages), # TODO: implement event system, CommandHeader, BattleEyeInvalidPacketException, Packet

### Community 18 - "Framework Service Providers"
Cohesion: 0.06
Nodes (30): AppServiceProvider, Application, ApplicationBase, armaden.framework, Application (ApplicationBase), ServiceProvider, TaskBuilder, app() facade (+22 more)

### Community 19 - "Typed Environment Config"
Cohesion: 0.15
Nodes (6): ArmaReforgerServerConfig, config(), env(), Any, Facade for reading typed environment variables from the application., config()

### Community 20 - "Login Packet Processing"
Cohesion: 0.23
Nodes (3): Message, datetime, LoginRequestPacket

### Community 21 - "Datagram Packet Parsing"
Cohesion: 0.23
Nodes (4): RequestMessage, KeepAlivePacket, Self, UnknownPacket

### Community 22 - "FastAPI Default Application"
Cohesion: 0.24
Nodes (5): FastAPI, DefaultApi, DefaultApiError, Any, Result

### Community 23 - "Module Discovery Loader"
Cohesion: 0.12
Nodes (16): HealthStatus, GetAppStatus, RestartAppService, ShutdownAppService, Api, Any, Controllers for API routes, LifecycleController (+8 more)

### Community 24 - "Service Provider Registry"
Cohesion: 0.18
Nodes (3): BindingResolutionException, Parameter, SelfBuilding

### Community 29 - "Config Value Management"
Cohesion: 0.33
Nodes (4): ArmaReforgerExecutableFlag, ArmaReforgerExecutableFlagError, Result, Arma Reforger CLI startup flags.

### Community 30 - "Player Response Parsing"
Cohesion: 0.33
Nodes (4): PlayerResponseData, Self, Parse a single data row from ``players`` output.          Returns ``None``  if t, A connected player returned by the ``players`` command.

### Community 35 - "Async Subprocess Dispatch"
Cohesion: 0.50
Nodes (3): AsyncStreamCallback, Path, Result

## Knowledge Gaps
- **8 isolated node(s):** `armaden`, `ArmaDen README`, `Build and Release Workflow`, `armaden.games`, `config/app.py` (+3 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **37 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ArmaReforgerServerExecutable` connect `Arma Reforger Server Config` to `Executable Argument Builder`, `Task Lifecycle Management`, `Application Health Status`, `Arma Server Task Runtime`, `Server Path Configuration`, `Type Discovery Provider`, `App Lifecycle Callbacks`, `Frontend Dependencies`, `Steam Query Bind Address`, `Server Addon Loader`, `Addon Auto Repair Flag`, `Server Auto Restart Flag`, `Auto Shutdown Flag`, `Local Backend Storage Flag`, `Resource Database Regeneration`, `Debugger Port Setting`, `Force Session Load Flag`, `Freeze Detection Timeout`, `Freeze Behaviour Mode`, `Crash File Retention Flag`, `Log File Retention Limit`, `Game Language Setting`, `Server FPS Cap`, `List Scenarios Flag`, `Log Append Mode Flag`, `Filesystem Logging Flag`, `Log Verbosity Level`, `Error Dialog Suppression`, `Global Streaming Budget`?**
  _High betweenness centrality (0.262) - this node is a cross-community bridge._
- **Why does `InstanceContainer` connect `IoC Container Binding` to `Bound Method Resolution`, `Service Provider Registry`, `Application Kernel Interface`, `Console HTTP Providers`?**
  _High betweenness centrality (0.142) - this node is a cross-community bridge._
- **Why does `TaskRuntimeInterface` connect `Arma Server Task Runtime` to `Arma Reforger Server Config`, `Async Subprocess Dispatch`, `Application Kernel Interface`, `Executable Argument Builder`, `Application Health Status`, `Server Path Configuration`, `FastAPI Default Application`?**
  _High betweenness centrality (0.134) - this node is a cross-community bridge._
- **Are the 10 inferred relationships involving `ArmaReforgerServerExecutable` (e.g. with `ArmaReforgerServer` and `ArmaReforgerServerError`) actually correct?**
  _`ArmaReforgerServerExecutable` has 10 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `InstanceContainer` (e.g. with `Application` and `BoundMethod`) actually correct?**
  _`InstanceContainer` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `armaden`, `Accepts any Enum instance that implements a .message property.`, `Enforces that any error type object has a code string and message string.` to the rest of the system?**
  _100 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `IoC Container Binding` be split into smaller, more focused modules?**
  _Cohesion score 0.08892921960072596 - nodes in this community are weakly interconnected._