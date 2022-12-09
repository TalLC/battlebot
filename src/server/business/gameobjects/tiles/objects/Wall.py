from business.shapes.ShapeFactory import ShapeFactory
from business.gameobjects.tiles.objects.TileObject import TileObject


class Wall(TileObject):
    _NAME = 'Wall'
    _HEALTH_MAX: int = 100000

    def __init__(self, x: int = 0, z: int = 0):
        super().__init__(name=self._NAME, x=x, z=z, health=self._HEALTH_MAX, has_collision=True,
                         shape=ShapeFactory.create_shape(name='square', o=(self.x, self.z), width=.9))
