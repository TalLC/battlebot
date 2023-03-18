import json
from pathlib import Path
from conf.models.GameConfig import GameConfig
from conf.models.TeamsConfig import TeamsConfig
from conf.models.NetworkSecurityConfig import NetworkSecurityConfig
from conf.models.RestConfig import RestConfig
from conf.models.MQTTConfig import MQTTConfig
from conf.models.STOMPConfig import STOMPConfig


# Config files
CONFIG_GAME = GameConfig(**json.loads(Path('conf', 'game.json').read_text()))

CONFIG_TEAMS = list()
__teams = json.loads(Path('conf', 'teams.json').read_text())
for team in __teams:
    CONFIG_TEAMS.append(TeamsConfig(**team))

CONFIG_NETWORK_SECURITY = NetworkSecurityConfig(**json.loads(Path('conf', 'ban_config.json').read_text()))
CONFIG_REST = RestConfig(**json.loads(Path('conf', 'rest.json').read_text()))
CONFIG_MQTT = MQTTConfig(**json.loads(Path('conf', 'mqtt.json').read_text()))
CONFIG_STOMP = STOMPConfig(**json.loads(Path('conf', 'stomp.json').read_text()))

# Datetime formatting
DATETIME_STR_FORMAT = '%d/%m/%Y %H:%M:%S'

# Name generation
WORDS_ADJECTIVES_LIST = Path('conf', 'dictionaries', 'english-adjectives.txt')\
    .read_text().replace('\r\n', '\n').split('\n')
WORDS_NOUNS_LIST = Path('conf', 'dictionaries', 'english-nouns.txt')\
    .read_text().replace('\r\n', '\n').split('\n')
WORDS_GERUNDS_LIST = Path('conf', 'dictionaries', 'english-gerunds.txt')\
    .read_text().replace('\r\n', '\n').split('\n')
WORDS_COLORS_LIST = Path('conf', 'dictionaries', 'english-colors.txt')\
    .read_text().replace('\r\n', '\n').split('\n')
WORDS_ANIMALS_LIST = Path('conf', 'dictionaries', 'english-animals.txt')\
    .read_text().replace('\r\n', '\n').split('\n')