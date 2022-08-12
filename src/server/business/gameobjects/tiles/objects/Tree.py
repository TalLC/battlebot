from business.gameobjects.tiles.objects.TileObject import TileObject


class Tree(TileObject):
    _HEALTH_MAX: int = 3

    def __init__(self, x: int = 0, z: int = 0):
        super().__init__(x=x, z=z, health=self._HEALTH_MAX, has_collision=True)
