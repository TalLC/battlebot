from __future__ import annotations
from typing import TYPE_CHECKING
from business.shapes.ShapeFactory import ShapeFactory, Shape
from business.gameobjects.tiles.objects.TileObject import TileObject


if TYPE_CHECKING:
    from business.gameobjects.tiles.Tile import Tile


class Wall(TileObject):
    _NAME = 'Wall'
    _HEALTH_MAX: int = 100000

    # Collision Shape
    _shape_name = "SQUARE"
    _shape_size = 0.9

    @property
    def shape_name(self) -> str:
        return self._shape_name

    @property
    def shape_size(self) -> float:
        return self._shape_size

    def __init__(self, parent_tile: Tile, x: float = 0.0, z: float = 0.0):
        super().__init__(
            parent_tile=parent_tile, name=self._NAME, object_type="wall", x=x, z=z, health=self._HEALTH_MAX,
            has_collision=True,
            shape=ShapeFactory().create_shape(shape=Shape.SQUARE, o=(self.x, self.z), width=self._shape_size)
        )
