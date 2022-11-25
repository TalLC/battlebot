import json
from pathlib import Path
from conf.models.RestConfig import RestConfig
from conf.models.MQTTConfig import MQTTConfig
from conf.models.STOMPConfig import STOMPConfig


# Config files
CONFIG_REST = RestConfig(**json.loads(Path('lib_ai', 'conf', 'rest.json').read_text()))
CONFIG_MQTT = MQTTConfig(**json.loads(Path('lib_ai', 'conf', 'mqtt.json').read_text()))
CONFIG_STOMP = STOMPConfig(**json.loads(Path('lib_ai', 'conf', 'stomp.json').read_text()))
