from dataclasses import dataclass


@dataclass
class STOMPConfig:
    destination_root: str
    host: str
    port: int
    username: str
    password: str
