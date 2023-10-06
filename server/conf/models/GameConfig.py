from dataclasses import dataclass


@dataclass
class GameConfig:
    is_debug: bool
    max_players: int
    plugins_spawn: list
