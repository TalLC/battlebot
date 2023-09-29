from __future__ import annotations
from typing import TYPE_CHECKING

from business.shapes.ShapesUtils import ShapesUtils
from business.gameobjects.tiles.objects.TileObject import TileObject

if TYPE_CHECKING:
    from business.gameobjects.tiles.Tile import Tile


class TilesGrid:

    @property
    def tiles(self) -> list[Tile]:
        return self._tiles

    def __init__(self, tiles_matrix: [[Tile]]):
        self._tiles = list()

        # Creating Tiles and Tile objects
        for row in tiles_matrix:
            for tile in row:
                self._tiles.append(tile)

    def get_tile_at(self, x: int, z: int) -> Tile | None:
        """
        Retrieves the Tile at specified location.
        """
        found_tiles = [tile for tile in self.tiles if tile.x == x and tile.z == z]
        return found_tiles[0] if len(found_tiles) > 0 else None

    def get_all_tiles(self, non_walkable_only: bool = False) -> list[Tile]:
        """
        Get all tile objects from the map.
        """
        return [tile for tile in self.tiles
                if not non_walkable_only or (non_walkable_only and not tile.is_walkable)]

    def get_tiles_in_radius(self, non_walkable_only: bool = False,
                            origin: tuple = (0.0, 0.0), radius: int = 1) -> list[Tile]:
        """
        Get all tile objects from the map.
        """
        # Filtering on radius
        in_range_tiles = list()
        for tile in self.get_all_tiles(non_walkable_only=non_walkable_only):
            if ShapesUtils.get_2d_distance_between(origin, (tile.x, tile.z)) <= radius:
                in_range_tiles.append(tile)

        return in_range_tiles

    def get_all_tiles_objects(self, collision_only: bool = True) -> list[TileObject]:
        """
        Get all tile objects from the map.
        """
        return [tile.tile_object for tile in self.tiles
                if not collision_only or (collision_only and tile.tile_object.has_collision)]

    def get_tiles_objects_in_radius(self, collision_only: bool = True, origin: tuple = (0.0, 0.0), radius: int = 1):
        """
        Get tiles objects in radius from the map
        """
        # Filtering on radius
        in_range_tile_objects = list()
        for tile_object in self.get_all_tiles_objects(collision_only=collision_only):
            if ShapesUtils.get_2d_distance_between(origin, (tile_object.x, tile_object.z)) <= radius:
                in_range_tile_objects.append(tile_object)

        return in_range_tile_objects

    def json(self) -> list[dict]:
        """
        Dumps the tile list in a serializable format.
        """
        tiles_list = list()
        for tile in self.tiles:
            tiles_list.append({
                "id": tile.id,
                "name": tile.name,
                "x": tile.x,
                "z": tile.z,
                "shape_name": tile.shape_name.lower() if tile.shape_name else str(),
                "shape_size": tile.shape_size,
                "object": {
                    "id": tile.tile_object.id,
                    "name": tile.tile_object.name,
                    "x": tile.tile_object.x,
                    "z": tile.tile_object.z,
                    "ry": tile.tile_object.ry,
                    "shape_name": tile.tile_object.shape_name.lower() if tile.tile_object.shape_name else str(),
                    "shape_size": tile.tile_object.shape_size
                }
            })

        return tiles_list
