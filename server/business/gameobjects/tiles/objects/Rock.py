from __future__ import annotations
from typing import TYPE_CHECKING
from business.shapes.ShapeFactory import ShapeFactory, Shape
from business.gameobjects.tiles.objects.TileObject import TileObject


if TYPE_CHECKING:
    from business.gameobjects.tiles.Tile import Tile


class Rock(TileObject):
    _FRIENDLY_NAME: str = "Rock"
    _NAME = 'Rock'
    _HEALTH_MAX: int = 15

    # Collision Shape
    _shape_name = "CIRCLE"
    _shape_size = 0.4

    @property
    def shape_name(self) -> str:
        return self._shape_name

    @property
    def shape_size(self) -> float:
        return self._shape_size

    @property
    def radius(self):
        return self._shape_size

    def __init__(self, parent_tile: Tile, model_name: str = str(), x: float = 0.0, z: float = 0.0):
        self._NAME = model_name
        super().__init__(
            parent_tile=parent_tile, name=self._NAME, friendly_name=self._FRIENDLY_NAME, object_type="rock",
            x=x, z=z, health=self._HEALTH_MAX, has_collision=True,
            shape=ShapeFactory().create_shape(Shape.CIRCLE, o=(x, z), radius=self._shape_size, resolution=6)
        )
