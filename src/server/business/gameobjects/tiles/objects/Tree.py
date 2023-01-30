import logging
from business.shapes.ShapeFactory import ShapeFactory, Shape
from business.gameobjects.tiles.objects.TileObject import TileObject


class Tree(TileObject):
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

    def __init__(self, x: int = 0, z: int = 0):
        super().__init__(
            name=self._NAME, x=x, z=z, health=self._HEALTH_MAX, has_collision=True,
            shape=ShapeFactory().create_shape(Shape.CIRCLE, o=(x, z), radius=self._shape_size, resolution=4)
        )

    def _on_hurt(self) -> None:
        pass
