from __future__ import annotations
from typing import TypedDict


class StartupConfig(TypedDict):
    profileDirectory: str | None
    logsDirectory: str | None
    maxFps: int | None


class A2SConfig(TypedDict):
    address: str | None
    port: int | None


class RconConfig(TypedDict):
    address: str | None
    port: int | None
    password: str | None
    maxClients: int | None
    permission: str | None
    blacklist: list | None
    whitelist: list | None


class GamePropertiesPersistence(TypedDict):
    autoSaveInterval: int | None
    saveRetention: int | None
    loadSessionSave: bool | None
    keepSessionSave: bool | None
    hiveId: int | None
    databases: dict | None
    storages: dict | None


class GamePropertiesConfig(TypedDict):
    serverMaxViewDistance: int | None
    serverMinGrassDistance: int | None
    fastValidation: bool | None
    networkViewDistance: int | None
    battlEye: bool | None
    disableThirdPerson: bool | None
    VONDisableUI: bool | None
    VONDisableDirectSpeechUI: bool | None
    VONCanTransmitCrossFaction: bool | None
    missionHeader: dict | None
    persistence: GamePropertiesPersistence | None


class GameConfig(TypedDict):
    name: str | None
    password: str | None
    passwordAdmin: str | None
    admins: list | None
    scenarioId: str | None
    maxPlayers: int | None
    visible: bool | None
    crossPlatform: bool | None
    supportedPlatforms: list | None
    modsRequiredByDefault: bool | None
    mods: list | None
    gameProperties: GamePropertiesConfig | None


class JoinQueueConfig(TypedDict):
    maxSize: int | None


class OperatingConfig(TypedDict):
    lobbyPlayerSynchronise: bool | None
    disableCrashReporter: bool | None
    disableNavmeshStreaming: list | None
    disableServerShutdown: bool | None
    disableAI: bool | None
    playerSaveTime: int | None
    aiLimit: int | None
    slotReservationTimeout: int | None
    joinQueue: JoinQueueConfig | None


class ServerConfig(TypedDict):
    bindAddress: str | None
    bindPort: int | None
    publicAddress: str | None
    publicPort: int | None
    a2s: A2SConfig | None
    rcon: RconConfig | None
    game: GameConfig | None
    operating: OperatingConfig | None


class Config(TypedDict):
    executable: str | None
    installDirectory: str | None
    steamExecutable: str | None
    steamInstallDirectory: str | None
    startup: StartupConfig | None
    server: ServerConfig | None


DEFAULT_CONFIG: Config = {
    'executable': None,
    'steamExecutable': None,
    'installDirectory': None,
    'steamExecutable': None,
    'steamInstallDirectory': None,
    'startup': {
        'profileDirectory': None,
        'logsDirectory': None,
        'maxFps': 60,
    },
    'server': {
        'bindAddress': '0.0.0.0',
        'bindPort': 2001,
        'publicAddress': None,
        'publicPort': None,
        'a2s': {
            'address': '0.0.0.0',
            'port': 17777,
        },
        'rcon': {
            'address': '0.0.0.0',
            'port': 19999,
            'password': None,
            'maxClients': 16,
            'permission': 'monitor',
            'blacklist': None,
            'whitelist': None,
        },
        'game': {
            'name': 'Arma Reforger Server',
            'password': None,
            'passwordAdmin': None,
            'admins': [],
            'scenarioId': '{ECC61978EDCC2B5A}Missions/23_Campaign.conf',
            'maxPlayers': 64,
            'visible': True,
            'crossPlatform': False,
            'supportedPlatforms': ['PLATFORM_PC'],
            'modsRequiredByDefault': True,
            'mods': [],
            'gameProperties': {
                'serverMaxViewDistance': 5000,
                'serverMinGrassDistance': 50,
                'fastValidation': True,
                'networkViewDistance': 1500,
                'battlEye': True,
                'disableThirdPerson': False,
                'VONDisableUI': False,
                'VONDisableDirectSpeechUI': False,
                'VONCanTransmitCrossFaction': False,
                'missionHeader': {},
                'persistence': {
                    'autoSaveInterval': 10,
                    'saveRetention': 10,
                    'loadSessionSave': True,
                    'keepSessionSave': False,
                    'hiveId': 0,
                    'databases': {},
                    'storages': {},
                },
            },
        },
        'operating': {
            'lobbyPlayerSynchronise': True,
            'disableCrashReporter': False,
            'disableNavmeshStreaming': None,
            'disableServerShutdown': False,
            'disableAI': False,
            'playerSaveTime': 120,
            'aiLimit': -1,
            'slotReservationTimeout': 60,
            'joinQueue': {
                'maxSize': 0,
            },
        },
    },
}
