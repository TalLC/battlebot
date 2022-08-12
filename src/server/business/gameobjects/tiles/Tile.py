from abc import ABC, abstractmethod

from business.gameobjects.tiles.objects.TileObject import TileObject
from business.gameobjects.GameObject import GameObject

"""
    Base class for every tile in the game.
    A tile have a position.
    A tile have a tile object:
        - Air
        - Tree
        - Wall
        - ...
    A tile can or cannot be walked onto.
"""


class Tile(GameObject, ABC):

    @property
    @abstractmethod
    def is_walkable(self) -> bool:
        raise NotImplementedError()

    def __init__(self, x: int, z: int, tile_object: TileObject):
        self.tile_object = tile_object
        super().__init__(x, z)
