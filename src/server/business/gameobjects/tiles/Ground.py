from business.gameobjects.tiles.Tile import Tile
from business.gameobjects.tiles.objects.TileObject import TileObject
from business.gameobjects.tiles.objects.Air import Air


class Ground(Tile):
    _NAME: str = "Ground"

    @property
    def is_walkable(self) -> bool:
        return not self.tile_object.has_collision

    def __init__(self, x: int, z: int, tile_object: TileObject = Air()):
        super().__init__(x, z, tile_object)
