from __future__ import annotations
from typing import TYPE_CHECKING

from business.gameobjects.tiles.objects.Air import Air
from business.gameobjects.tiles.objects.Rock import Rock
from business.gameobjects.tiles.objects.Tree import Tree
from business.gameobjects.tiles.objects.Wall import Wall

if TYPE_CHECKING:
    from business.gameobjects.tiles.Tile import Tile
    from business.gameobjects.tiles.objects.TileObject import TileObject


class TileObjectFactory:

    @staticmethod
    def create_tile_object(parent_tile: Tile, tile_object_name: str, x: float, z: float) -> TileObject:
        if tile_object_name.lower() == "air":
            return Air(parent_tile=parent_tile, x=x, z=z)
        elif tile_object_name.lower() == "rock":
            return Rock(parent_tile=parent_tile, x=x, z=z)
        elif tile_object_name.lower() == "tree":
            return Tree(parent_tile=parent_tile, x=x, z=z)
        elif tile_object_name.lower() == "wall":
            return Wall(parent_tile=parent_tile, x=x, z=z)
