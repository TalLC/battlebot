import json
from pathlib import Path
from provider.webservices.rest.config.RestConfig import RestConfig
from provider.brokers.config.MQTTConfig import MQTTConfig
from provider.brokers.config.STOMPConfig import STOMPConfig


# Config files
CONFIG_REST = RestConfig(**json.loads(Path('conf', 'rest.json').read_text()))
CONFIG_MQTT = MQTTConfig(**json.loads(Path('conf', 'mqtt.json').read_text()))
CONFIG_STOMP = STOMPConfig(**json.loads(Path('conf', 'stomp.json').read_text()))

# Datetime formatting
DATETIME_STR_FORMAT = '%d/%m/%Y %H:%M:%S'

# Name generation
WORDS_ADJECTIVES_LIST = Path('conf', 'dictionaries', 'english-adjectives.txt')\
    .read_text().replace('\r\n', '\n').split('\n')
WORDS_GERUNDS_LIST = Path('conf', 'dictionaries', 'english-gerunds.txt')\
    .read_text().replace('\r\n', '\n').split('\n')
WORDS_NOUNS_LIST = Path('conf', 'dictionaries', 'english-nouns.txt')\
    .read_text().replace('\r\n', '\n').split('\n')
