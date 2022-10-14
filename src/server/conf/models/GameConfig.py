from dataclasses import dataclass


@dataclass
class GameConfig:
    map_id: str
    max_players: int
