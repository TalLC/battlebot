from dataclasses import dataclass


@dataclass
class MQTTConfig:
    destination_root: str
    host: str
    port: int
    username: str
    password: str
    connect_timeout: int
