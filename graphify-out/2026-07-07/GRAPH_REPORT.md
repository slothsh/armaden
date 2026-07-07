# Graph Report - /home/slothsh/Developer/projects/armaden  (2026-07-07)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 1040 nodes · 2254 edges · 88 communities (43 shown, 45 thin omitted)
- Extraction: 85% EXTRACTED · 15% INFERRED · 0% AMBIGUOUS · INFERRED: 329 edges (avg confidence: 0.54)
- Token cost: 2,897 input · 830 output

## Graph Freshness
- Built from commit: `b332b473`
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
- Voting Log Flag
- Error Dialog Suppression
- Server Region Tag
- Replication Encoding Flag
- Script Authorization Flag
- Silent Crash Report Flag
- Single Threaded Update Flag
- Spatial Staggering Budget
- Global Streaming Budget
- Client Stream Delta Limit
- Arma Games Module
- Scaffold CLI Tool
- App Config File
- Environment Variables File
- ArmaDen Core Package
- ArmaDen Documentation

## God Nodes (most connected - your core abstractions)
1. `InstanceContainer` - 100 edges
2. `ArmaReforgerServerExecutable` - 94 edges
3. `CoreApplication` - 47 edges
4. `app()` - 39 edges
5. `BattleEyeRconClient` - 38 edges
6. `TaskRuntimeInterface` - 33 edges
7. `Packet` - 31 edges
8. `BattleEyeRconServer` - 30 edges
9. `SupervisorInterface` - 26 edges
10. `Supervisor` - 26 edges

## Surprising Connections (you probably didn't know these)
- `AppServiceProvider` --uses--> `TaskBuilder`  [INFERRED]
  user/app/providers/app_service_provider.py → src/armaden/framework/classes/task.py
- `AppServiceProvider` --uses--> `Config`  [INFERRED]
  user/app/providers/app_service_provider.py → src/armaden/games/arma_reforger/arma_reforger_server_config.py
- `Build and Release Workflow` --references--> `armaden.framework.runtime`  [INFERRED]
  .github/workflows/build.yml → README.md
- `Application` --uses--> `Application`  [INFERRED]
  user/bootstrap/application.py → src/armaden/framework/application.py
- `AppServiceProvider` --uses--> `ServiceProvider`  [INFERRED]
  user/app/providers/app_service_provider.py → src/armaden/framework/classes/service_provider.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Application Bootstrap Entry-Point Flow** — armaden_framework_runtime, bootstrap_application, bootstrap_providers, app_providers_app_service_provider [EXTRACTED 0.95]
- **Task Registration Flow via ServiceProvider** — app_providers_app_service_provider, armaden_framework_classes_task, armaden_framework_facades, armaden_framework_classes_service_provider [EXTRACTED 0.90]

## Communities (88 total, 45 thin omitted)

### Community 0 - "IoC Container Binding"
Cohesion: 0.06
Nodes (5): BindingResolutionException, ContextualBindingBuilder, InstanceContainer, Any, Parameter

### Community 1 - "Supervisor Request Handling"
Cohesion: 0.06
Nodes (33): Future, SupervisorRequestArgs, SupervisorRequestData, SupervisorRequestKind, GetAppStatus, RestartAppService, ShutdownAppService, Api (+25 more)

### Community 2 - "Arma Reforger Server Config"
Cohesion: 0.03
Nodes (37): ArmaReforgerServerExecutable, Result, Bind the server to specific addresses / ports.          Keyword Args:, Configure A2S query endpoint.          Keyword Args:             address: IP add, Configure BattlEye / RCON remote console.          Keyword Args:             add, Load multiple addons at once.          Args:             mod_ids: Variable-lengt, ID of the scenario to host., Unique server identifier. (+29 more)

### Community 3 - "Application Kernel Interface"
Cohesion: 0.05
Nodes (22): ApplicationBase, Protocol, Application, ErrorInterface, CoreApplicationInterface, KernelInterface, Any, Result (+14 more)

### Community 4 - "App Facade Container"
Cohesion: 0.09
Nodes (10): C, app(), Any, config(), Any, get_application(), Self, Route (+2 more)

### Community 5 - "Executable Argument Builder"
Cohesion: 0.06
Nodes (25): Executable, Path, PushValue, Result, Self, A2SConfig, GameConfig, GamePropertiesConfig (+17 more)

### Community 6 - "Task Lifecycle Management"
Cohesion: 0.08
Nodes (12): Self, StatusCallback, TaskCallback, Task, TaskBuilder, TaskThreadingPolicy, Error, ErrorKindInterface (+4 more)

### Community 7 - "Async Datagram Transport"
Cohesion: 0.07
Nodes (14): DatagramProtocol, DatagramTransport, entry(), main(), entry(), main(), AsyncDatagramTransport, AbstractEventLoop (+6 more)

### Community 8 - "Bound Method Resolution"
Cohesion: 0.11
Nodes (21): ABC, Exception, BoundMethod, CircularDependencyException, EntryNotFoundException, LogicException, SelfBuilding, ApplicationInterface (+13 more)

### Community 9 - "Application Health Status"
Cohesion: 0.14
Nodes (23): Application, HealthStatus, ApplicationError, ApplicationException, ApplicationStatus, DefaultApplication, Result, DefaultApiError (+15 more)

### Community 10 - "Core Application Bootstrap"
Cohesion: 0.14
Nodes (4): CoreApplication, AbstractEventLoop, Any, Result

### Community 11 - "BattleEye RCON Server"
Cohesion: 0.13
Nodes (10): IntEnum, BattleEyeRconServer, Client, ClientState, AbstractEventLoop, DatagramTransportFactory, datetime, Exception (+2 more)

### Community 12 - "Console Kernel Bootstrap"
Cohesion: 0.14
Nodes (9): set_application(), bootstrap_console(), bootstrap_http(), ConsoleKernel, HttpKernel, Kernel, Any, RuntimeEntry (+1 more)

### Community 13 - "Scaffold File Generator"
Cohesion: 0.14
Nodes (12): Generator, GeneratorResult, Path, _detect_poetry_package_path(), _fmt_list(), main(), _print_result(), Path (+4 more)

### Community 14 - "BattleEye RCON Client"
Cohesion: 0.11
Nodes (6): BattleEyeRconClient, ClientStatus, AbstractEventLoop, Any, DatagramTransportFactory, Exception

### Community 15 - "Arma Server Task Runtime"
Cohesion: 0.20
Nodes (6): TaskRuntimeInterface, ArmaReforgerServer, Any, Result, Self, Result

### Community 16 - "Server Path Configuration"
Cohesion: 0.10
Nodes (11): Path, Path to a server configuration JSON file., Directory for profiles (saves, logs, settings).          The directory is create, Redirect log output to the given directory., Path to a session save to load on startup., Additional directories to search for mods.          Multiple directories can be, Directory where addons are downloaded., Directory for temporary addon data. (+3 more)

### Community 17 - "BattleEye Packet Protocol"
Cohesion: 0.20
Nodes (5): # TODO: handle stateful messages (responses to sequenced messages), # TODO: implement event system, CommandHeader, BattleEyeInvalidPacketException, Packet

### Community 18 - "Framework Service Providers"
Cohesion: 0.18
Nodes (12): AppServiceProvider, armaden.framework, Application (ApplicationBase), ServiceProvider, TaskBuilder, app() facade, armaden.framework.runtime, armaden runtime CLI (+4 more)

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
Cohesion: 0.27
Nodes (4): FastAPI, DefaultApi, Any, Result

### Community 23 - "Module Discovery Loader"
Cohesion: 0.35
Nodes (4): ModuleType, ModuleLoader, Any, Result

### Community 24 - "Service Provider Registry"
Cohesion: 0.27
Nodes (5): Any, Result, ServiceProvider, AppServiceProvider, providers()

### Community 25 - "Console HTTP Providers"
Cohesion: 0.27
Nodes (4): ConsoleServiceProvider, Result, HttpServiceProvider, Result

### Community 30 - "Player Response Parsing"
Cohesion: 0.33
Nodes (4): PlayerResponseData, Self, Parse a single data row from ``players`` output.          Returns ``None``  if t, A connected player returned by the ``players`` command.

### Community 35 - "Async Subprocess Dispatch"
Cohesion: 0.50
Nodes (3): AsyncStreamCallback, Path, Result

## Knowledge Gaps
- **9 isolated node(s):** `@gaodes/pi-graphify`, `armaden`, `ArmaDen README`, `Build and Release Workflow`, `armaden.games` (+4 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **45 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ArmaReforgerServerExecutable` connect `Arma Reforger Server Config` to `Executable Argument Builder`, `Application Health Status`, `Arma Server Task Runtime`, `Server Path Configuration`, `Config Value Management`, `Steam Query Bind Address`, `Server Addon Loader`, `Addon Auto Repair Flag`, `Server Auto Restart Flag`, `Auto Shutdown Flag`, `Local Backend Storage Flag`, `Resource Database Regeneration`, `Debugger Port Setting`, `Force Session Load Flag`, `Freeze Detection Timeout`, `Freeze Behaviour Mode`, `Crash File Retention Flag`, `Log File Retention Limit`, `Session Save Retention Flag`, `Game Language Setting`, `Server FPS Cap`, `List Scenarios Flag`, `Log Append Mode Flag`, `Filesystem Logging Flag`, `Log Verbosity Level`, `Voting Log Flag`, `Error Dialog Suppression`, `Server Region Tag`, `Replication Encoding Flag`, `Script Authorization Flag`, `Silent Crash Report Flag`, `Single Threaded Update Flag`, `Spatial Staggering Budget`, `Global Streaming Budget`, `Client Stream Delta Limit`?**
  _High betweenness centrality (0.255) - this node is a cross-community bridge._
- **Why does `InstanceContainer` connect `IoC Container Binding` to `Application Kernel Interface`, `Bound Method Resolution`, `Application Health Status`, `Core Application Bootstrap`, `Service Provider Registry`?**
  _High betweenness centrality (0.205) - this node is a cross-community bridge._
- **Why does `CoreApplication` connect `Core Application Bootstrap` to `IoC Container Binding`, `Type Discovery Provider`, `App Lifecycle Callbacks`, `Application Kernel Interface`, `Application Health Status`, `Console Kernel Bootstrap`, `Module Discovery Loader`, `Service Provider Registry`, `Console HTTP Providers`?**
  _High betweenness centrality (0.150) - this node is a cross-community bridge._
- **Are the 7 inferred relationships involving `InstanceContainer` (e.g. with `Application` and `BoundMethod`) actually correct?**
  _`InstanceContainer` has 7 INFERRED edges - model-reasoned connections that need verification._
- **Are the 10 inferred relationships involving `ArmaReforgerServerExecutable` (e.g. with `ArmaReforgerServer` and `ArmaReforgerServerError`) actually correct?**
  _`ArmaReforgerServerExecutable` has 10 INFERRED edges - model-reasoned connections that need verification._
- **Are the 10 inferred relationships involving `CoreApplication` (e.g. with `InstanceContainer` and `ServiceProvider`) actually correct?**
  _`CoreApplication` has 10 INFERRED edges - model-reasoned connections that need verification._
- **What connects `@gaodes/pi-graphify`, `armaden`, `Accepts any Enum instance that implements a .message property.` to the rest of the system?**
  _101 weakly-connected nodes found - possible documentation gaps or missing edges._