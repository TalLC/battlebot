from __future__ import annotations
from typing import TYPE_CHECKING
from business.shapes.ShapeFactory import ShapeFactory, Shape
from business.gameobjects.tiles.objects.TileObject import TileObject


if TYPE_CHECKING:
    from business.gameobjects.tiles.Tile import Tile


class Tree(TileObject):
    _FRIENDLY_NAME: str = "Tree"
    _NAME = 'Tree'
    _HEALTH_MAX: int = 3

    # Collision Shape
    _shape_name = "CIRCLE"
    _shape_size = 0.3

    @property
    def shape_name(self) -> str:
        return self._shape_name

    @property
    def shape_size(self) -> float:
        return self._shape_size

    @property
    def radius(self):
        return self._shape_size

    def __init__(self, parent_tile: Tile, x: float = 0.0, z: float = 0.0):
        super().__init__(
            parent_tile=parent_tile, name=self._NAME, friendly_name=self._FRIENDLY_NAME, object_type="tree",
            x=x, z=z, health=self._HEALTH_MAX, has_collision=True,
            shape=ShapeFactory().create_shape(Shape.CIRCLE, o=(x, z), radius=self._shape_size, resolution=4)
        )
