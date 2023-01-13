from abc import ABC, abstractmethod

from business.gameobjects.tiles.objects.TileObject import TileObject
from business.gameobjects.GameObject import GameObject
from business.shapes.ShapeFactory import ShapeFactory

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

    def __init__(self, name: str, x: int, z: int, tile_object: TileObject):
        self.tile_object = tile_object
        super().__init__(name, x, z, ShapeFactory.create_shape(name='square', o=(x, z), width=1))

    def __str__(self):
        return f"({self.x};{self.z})[{self.tile_object} on {self.name}] ({self.id})"
