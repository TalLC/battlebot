import json
from pathlib import Path
from conf.models.GameConfig import GameConfig
from conf.models.TeamsConfig import TeamsConfig
from conf.models.RestConfig import RestConfig
from conf.models.MQTTConfig import MQTTConfig
from conf.models.STOMPConfig import STOMPConfig

# Datetime formatting
DATETIME_STR_FORMAT = '%d/%m/%Y %H:%M:%S'

# Config files
CONFIG_GAME: GameConfig
CONFIG_TEAMS: [TeamsConfig]
CONFIG_REST: RestConfig
CONFIG_MQTT: MQTTConfig
CONFIG_STOMP: STOMPConfig

# Name generation
WORDS_ADJECTIVES_LIST: [str]
WORDS_NOUNS_LIST: [str]
WORDS_GERUNDS_LIST: [str]
WORDS_COLORS_LIST: [str]
WORDS_ANIMALS_LIST: [str]


def refresh_config():
    """
    Loads all config files and fill the variables.
    """
    # Config files
    global CONFIG_GAME
    CONFIG_GAME = GameConfig(**json.loads(Path('conf', 'game.json').read_text()))
    print(CONFIG_GAME)
    global CONFIG_TEAMS
    CONFIG_TEAMS = list()
    __teams = json.loads(Path('conf', 'teams.json').read_text())
    for team in __teams:
        CONFIG_TEAMS.append(TeamsConfig(**team))

    global CONFIG_REST
    CONFIG_REST = RestConfig(**json.loads(Path('conf', 'rest.json').read_text()))
    global CONFIG_MQTT
    CONFIG_MQTT = MQTTConfig(**json.loads(Path('conf', 'mqtt.json').read_text()))
    global CONFIG_STOMP
    CONFIG_STOMP = STOMPConfig(**json.loads(Path('conf', 'stomp.json').read_text()))

    # Name generation
    global WORDS_ADJECTIVES_LIST
    WORDS_ADJECTIVES_LIST = Path('conf', 'dictionaries', 'english-adjectives.txt') \
        .read_text().replace('\r\n', '\n').split('\n')
    global WORDS_NOUNS_LIST
    WORDS_NOUNS_LIST = Path('conf', 'dictionaries', 'english-nouns.txt') \
        .read_text().replace('\r\n', '\n').split('\n')
    global WORDS_GERUNDS_LIST
    WORDS_GERUNDS_LIST = Path('conf', 'dictionaries', 'english-gerunds.txt') \
        .read_text().replace('\r\n', '\n').split('\n')
    global WORDS_COLORS_LIST
    WORDS_COLORS_LIST = Path('conf', 'dictionaries', 'english-colors.txt') \
        .read_text().replace('\r\n', '\n').split('\n')
    global WORDS_ANIMALS_LIST
    WORDS_ANIMALS_LIST = Path('conf', 'dictionaries', 'english-animals.txt') \
        .read_text().replace('\r\n', '\n').split('\n')


# Reading config files
refresh_config()
