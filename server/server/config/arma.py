from server.lib import Env


def config():
    return {
        'reforger': {
            'executable': Env.string('ARMA_REFORGER_EXECUTABLE'),
            'installDirectory': Env.string('ARMA_REFORGER_INSTALL_DIR'),

            'startup': {
                'profileDirectory': Env.string('ARMA_REFORGER_PROFILE_DIR'),
                'logsDirectory': Env.string('ARMA_REFORGER_LOGS_DIR'),
                'maxFps': Env.int('ARMA_REFORGER_MAX_FPS', 60),
            },

            'server': {
                'bindAddress': Env.string('ARMA_REFORGER_BIND_ADDRESS', '0.0.0.0'),
                'bindPort': Env.int('ARMA_REFORGER_BIND_PORT', 2001),
                'publicAddress': Env.string('ARMA_REFORGER_PUBLIC_ADDRESS'),
                'publicPort': Env.int('ARMA_REFORGER_PUBLIC_PORT'),
                'a2s': {
                    'address': Env.string('ARMA_REFORGER_A2S_ADDRESS', '0.0.0.0'),
                    'port': Env.int('ARMA_REFORGER_A2S_PORT', 17777),
                },
                'rcon': {
                    'address': Env.string('ARMA_REFORGER_RCON_ADDRESS', '0.0.0.0'),
                    'port': Env.int('ARMA_REFORGER_RCON_PORT', 19999),
                    'password': Env.string('ARMA_REFORGER_RCON_PASSWORD', 'password'),
                    'maxClients': Env.int('ARMA_REFORGER_RCON_MAX_CLIENTS', 16),
                    'permission': Env.string('ARMA_REFORGER_RCON_PERMISSION', 'monitor'),
                    'blacklist': Env.json('ARMA_REFORGER_RCON_BLACKLIST', []),
                    'whitelist': Env.json('ARMA_REFORGER_RCON_WHITELIST', []),
                },
                'game': {
                    'name': Env.string('ARMA_REFORGER_GAME_NAME', 'Arma Reforger Server'),
                    'password': Env.string('ARMA_REFORGER_GAME_PASSWORD', 'password'),
                    'passwordAdmin': Env.string('ARMA_REFORGER_GAME_PASSWORD_ADMIN'),
                    'admins': Env.json('ARMA_REFORGER_GAME_ADMINS', []),
                    'scenarioId': Env.string('ARMA_REFORGER_GAME_SCENARIO_ID', '{ECC61978EDCC2B5A}Missions/23_Campaign.conf'),
                    'maxPlayers': Env.int('ARMA_REFORGER_GAME_MAX_PLAYERS', 64),
                    'visible': Env.bool('ARMA_REFORGER_GAME_VISIBLE', True),
                    'crossPlatform': Env.bool('ARMA_REFORGER_GAME_CROSS_PLATFORM', False),
                    'supportedPlatforms': Env.json('ARMA_REFORGER_GAME_SUPPORTED_PLATFORMS', ['PLATFORM_PC']),
                    'modsRequiredByDefault': Env.bool('ARMA_REFORGER_GAME_MODS_REQUIRED_BY_DEFAULT', True),
                    'mods': Env.json('ARMA_REFORGER_GAME_MODS', []),
                    'gameProperties': {
                        'serverMaxViewDistance': Env.int('ARMA_REFORGER_GAME_PROPERTIES_SERVER_MAX_VIEW_DISTANCE', 5000),
                        'serverMinGrassDistance': Env.int('ARMA_REFORGER_GAME_PROPERTIES_SERVER_MIN_GRASS_DISTANCE', 50),
                        'fastValidation': Env.bool('ARMA_REFORGER_GAME_PROPERTIES_FAST_VALIDATION', True),
                        'networkViewDistance': Env.int('ARMA_REFORGER_GAME_PROPERTIES_NETWORK_VIEW_DISTANCE', 1500),
                        'battlEye': Env.bool('ARMA_REFORGER_GAME_PROPERTIES_BATTLE_EYE', True),
                        'disableThirdPerson': Env.bool('ARMA_REFORGER_GAME_PROPERTIES_DISABLE_THIRD_PERSON', False),
                        'VONDisableUI': Env.bool('ARMA_REFORGER_GAME_PROPERTIES_VON_DISABLE_UI', False),
                        'VONDisableDirectSpeechUI': Env.bool('ARMA_REFORGER_GAME_PROPERTIES_VON_DISABLE_DIRECT_SPEECH_UI', False),
                        'VONCanTransmitCrossFaction': Env.bool('ARMA_REFORGER_GAME_PROPERTIES_VON_CAN_TRANSMIT_CROSS_FACTION', False),
                        'missionHeader': Env.json('ARMA_REFORGER_GAME_PROPERTIES_MISSION_HEADER', {}),
                        'persistence': {
                            'autoSaveInterval': Env.int('ARMA_REFORGER_GAME_PROPERTIES_PERSISTENCE_AUTO_SAVE_INTERVAL', 10),
                            'saveRetention': Env.int('ARMA_REFORGER_GAME_PROPERTIES_PERSISTENCE_SAVE_RETENTION', 10),
                            'loadSessionSave': Env.bool('ARMA_REFORGER_GAME_PROPERTIES_PERSISTENCE_LOAD_SESSION_SAVE', True),
                            'keepSessionSave': Env.bool('ARMA_REFORGER_GAME_PROPERTIES_PERSISTENCE_KEEP_SESSION_SAVE', False),
                            'hiveId': Env.int('ARMA_REFORGER_GAME_PROPERTIES_PERSISTENCE_HIVE_ID', 0),
                            'databases': Env.json('ARMA_REFORGER_GAME_PROPERTIES_PERSISTENCE_DATABASES', {}),
                            'storages': Env.json('ARMA_REFORGER_GAME_PROPERTIES_PERSISTENCE_STORAGES', {}),
                        },
                    },
                },
                'operating': {
                    'lobbyPlayerSynchronise': Env.bool('ARMA_REFORGER_OPERATING_LOBBY_PLAYER_SYNCHRONISE', True),
                    'disableCrashReporter': Env.bool('ARMA_REFORGER_OPERATING_DISABLE_CRASH_REPORTER', False),
                    'disableNavmeshStreaming': Env.optional_json('ARMA_REFORGER_OPERATING_DISABLE_NAVMESH_STREAMING'),
                    'disableServerShutdown': Env.bool('ARMA_REFORGER_OPERATING_DISABLE_SERVER_SHUTDOWN', False),
                    'disableAI': Env.bool('ARMA_REFORGER_OPERATING_DISABLE_AI', False),
                    'playerSaveTime': Env.int('ARMA_REFORGER_OPERATING_PLAYER_SAVE_TIME', 120),
                    'aiLimit': Env.int('ARMA_REFORGER_OPERATING_AI_LIMIT', -1),
                    'slotReservationTimeout': Env.int('ARMA_REFORGER_OPERATING_SLOT_RESERVATION_TIMEOUT', 60),
                    'joinQueue': {
                        'maxSize': Env.int('ARMA_REFORGER_OPERATING_JOIN_QUEUE_MAX_SIZE', 0),
                    },
                },
            },
        },
    }
