from business.shapes.ShapeFactory import ShapeFactory
from business.gameobjects.tiles.objects.TileObject import TileObject


class Tree(TileObject):
    _NAME = 'Tree'
    _HEALTH_MAX: int = 3
    _shape_radius = .3

    def __init__(self, x: int = 0, z: int = 0):
        super().__init__(name=self._NAME, x=x, z=z, health=self._HEALTH_MAX, has_collision=True,
                         shape=ShapeFactory.create_shape(name='circle', o=(x, z), radius=.3, resolution=4))
