from dataclasses import dataclass


@dataclass
class GameConfig:
    is_debug: bool
    map_id: str
    max_players: int
    plugins_spawn: list
