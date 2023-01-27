from business.gameobjects.tiles.Tile import Tile
from business.gameobjects.tiles.objects.TileObject import TileObject
from business.gameobjects.tiles.objects.Air import Air


class Ground(Tile):
    _NAME: str = "Ground"

    @property
    def is_walkable(self) -> bool:
        return True

    def __init__(self, x: int, z: int, tile_object: TileObject = Air()):
        super().__init__(name=self._NAME, x=x, z=z, tile_object=tile_object)
