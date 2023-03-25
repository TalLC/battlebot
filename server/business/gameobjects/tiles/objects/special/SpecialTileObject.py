from abc import abstractmethod
from typing import Any

from business.gameobjects.tiles.objects.TileObject import TileObject


class SpecialTileObject(TileObject):

    def __init__(self, x: int, z: int, heading: float = 0.0, health: int = 0, has_collision: bool = False):
        super().__init__(x, z, heading, health, has_collision)

    @abstractmethod
    def callback(self, bot) -> Any:
        raise NotImplementedError()
