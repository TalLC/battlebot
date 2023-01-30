import logging
from business.shapes.ShapeFactory import ShapeFactory, Shape
from business.gameobjects.tiles.objects.TileObject import TileObject


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

    def __init__(self, x: int = 0, z: int = 0):
        super().__init__(
            name=self._NAME, x=x, z=z, health=self._HEALTH_MAX, has_collision=True,
            shape=ShapeFactory().create_shape(shape=Shape.SQUARE, o=(self.x, self.z), width=self._shape_size)
        )

    def _on_hurt(self) -> None:
        pass
