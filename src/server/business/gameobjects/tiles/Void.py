from business.gameobjects.tiles.Tile import Tile
from business.gameobjects.tiles.objects.TileObject import TileObject
from business.gameobjects.tiles.objects.Air import Air


class Void(Tile):
    _NAME: str = "Void"

    @property
    def is_walkable(self) -> bool:
        return False

    def __init__(self, x: int, z: int, tile_object: TileObject = None):
        super().__init__(
            name=self._NAME, x=x, z=z, tile_object=Air(parent_tile=self) if tile_object is None else tile_object
        )
