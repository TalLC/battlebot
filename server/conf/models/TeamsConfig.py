from dataclasses import dataclass, field


@dataclass
class TeamsConfig:
    size: int
    name: str
    color: str
    id: str = field(default=None)
