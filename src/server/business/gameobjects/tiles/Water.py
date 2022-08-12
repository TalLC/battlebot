from business.gameobjects.tiles.Tile import Tile
from business.gameobjects.tiles.objects.TileObject import TileObject
from business.gameobjects.tiles.objects.Air import Air


class Water(Tile):
    _NAME: str = "Water"

    @property
    def is_walkable(self) -> bool:
        return False

    def __init__(self, x: int, z: int, tile_object: TileObject = Air()):
        super().__init__(x, z, tile_object)
